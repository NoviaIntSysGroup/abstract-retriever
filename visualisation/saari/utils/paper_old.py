import pandas as pd
import re, os

import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32
import numpy as np

from typing import List
import struct

from umap import UMAP
from sentence_transformers import SentenceTransformer



def serialize_f32(vector: List[float]) -> bytes:
    """Serializes a lost of floats into a compact raw bytes format"""
    return struct.pack("%sf" % len(vector), *vector)


def init_db(df, db_filename = "data/db/db.sqlite"):
    print("we check if we have a db?")
    db = sqlite3.connect(db_filename, check_same_thread=False)  # Allow access from different threads
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    tfm_base = model = SentenceTransformer('nvidia/NV-Embed-v2', trust_remote_code=True)
    tfm_base.max_seq_length = 32768
    tfm_base.tokenizer.padding_side="right"

    if not db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bin_vec_sents';").fetchone():
        print("i do not have a bin_vec_sents")

        title_list = df['title'].tolist()
        abstract_and_title_list = [str(abstract) + ' ' + title for abstract, title in zip(df['abstract'], df['title'])]

        X_tfm = tfm_base.encode(abstract_and_title_list)
        n_feats = X_tfm.shape[1]

        db.execute(f"CREATE VIRTUAL TABLE bin_vec_sents USING vec0(embedding bit[{n_feats}])")

        # Create 2D UMAP embeddings
        umap = UMAP(n_neighbors=15, min_dist=0.1, metric='cosine')
        umap_embeddings = umap.fit_transform(X_tfm)

        # Create a separate table for UMAP embeddings
        db.execute("CREATE TABLE umap_embeddings (rowid INTEGER PRIMARY KEY, x REAL, y REAL)")
        with db:
            for i, (x, y) in enumerate(umap_embeddings):
                db.execute("INSERT INTO umap_embeddings (rowid, x, y) VALUES (?, ?, ?)", [i, x, y])

        with db:
            for i, item in enumerate([{"vector": x} for i, x in enumerate(X_tfm)]):
                db.execute(
                    "INSERT INTO bin_vec_sents(rowid, embedding) VALUES (?, vec_quantize_binary(?))",
                    [i, serialize_f32(item["vector"])]
                )
    return db, tfm_base


data_path = '/Users/toffe/dev/ai/novia/lib/serach-comparison/data/search_results.csv'
df = pd.read_csv(data_path)

db, tfm_base = init_db(df)

def get_embeddings_and_labels(limit=1000):
    """
    Retrieves tuples of titles and embeddings from the database.

    Parameters:
    - limit (int): The maximum number of tuples to retrieve. Defaults to 1000.

    Returns:
    - List[Tuple]: A list of tuples containing titles and embeddings.
    """
    rows_bin = db.execute(
        """
        SELECT
            rowid,
            embedding
        FROM bin_vec_sents
        LIMIT ?
        """,
        [limit]
    ).fetchall()

    # Convert rows_bin to a list of tuples containing titles and embeddings
    title_embeddings = []
    for row in rows_bin:
        title = df.loc[row[0], 'title']
        embedding = row[1]
        title_embeddings.append((title, embedding))
    return title_embeddings

def get_titles_and_umap_embeddings(limit=1000):
    """
    Retrieves a DataFrame containing paper titles and their corresponding UMAP embeddings.

    Parameters:
    - limit (int): The maximum number of rows to retrieve. Defaults to 1000.

    Returns:
    - pandas.DataFrame: A DataFrame containing paper titles and their corresponding UMAP embeddings.
    """
    rows_umap = db.execute(
        """
        SELECT
            rowid,
            x,
            y
        FROM umap_embeddings
        LIMIT ?
        """,
        [limit]
    ).fetchall()

    # Convert rows_umap to a list of tuples containing titles and UMAP embeddings
    title_umap_embeddings = []
    for row in rows_umap:
        title = df.loc[row[0], 'title']
        x = struct.unpack('f', row[1])[0]
        y = struct.unpack('f', row[2])[0]
        title_umap_embeddings.append((title, x, y))

    # Convert the list to a DataFrame
    result_df = pd.DataFrame(title_umap_embeddings, columns=['title', 'x', 'y'])

    # Return the resulting DataFrame
    return result_df




def get_sorted_list_of_papers(text: str, limit=1000):
    query = tfm_base.encode([text])[0]

    rows_bin = db.execute(
        f"""
            SELECT
                rowid,
                distance,
                embedding
            FROM bin_vec_sents
            WHERE embedding MATCH vec_quantize_binary(?)
            ORDER BY distance
            LIMIT {limit}
        """,
        [serialize_f32(query)]
    ).fetchall()

    # Check if rows_bin is empty
    if not rows_bin:
        raise ValueError("No valid embeddings found in the database for the given query.")

    # Convert rows_bin to a list of row IDs, distances, and embeddings
    row_ids = [row[0] for row in rows_bin]
    distances = [row[1] for row in rows_bin]  # Get distances
    embeddings = [row[2] for row in rows_bin]  # Get embeddings
    sorted_df = df.iloc[row_ids].copy()  # Create a copy to avoid SettingWithCopyWarning
    
    # Add distances and embeddings as new columns to the DataFrame
    sorted_df.loc[:, 'distance'] = distances  # Use .loc to avoid warning
    sorted_df.loc[:, 'embedding'] = embeddings  # Use .loc to avoid warning
    return sorted_df



def get_first_rows_of_csv(num_rows=10):
    global df
    """
    Reads the first 'num_rows' rows from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.
    - num_rows (int): The number of rows to read from the CSV file. Defaults to 10.

    Returns:
    - pandas.DataFrame: A DataFrame containing the first 'num_rows' rows of the CSV file.
    """
    return df.head()

def search_by_title(sortingtext: str, title):
    """
    Searches the dataframe for rows where the 'title' column matches the given title.

    Parameters:
    - df (pandas.DataFrame): The dataframe to search in.
    - title (str): The title to search for.

    Returns:
    - list: A list of dictionaries containing the rows where the 'title' column matches the given title, ordered by relevance.
    """
    
    df = get_sorted_list_of_papers(sortingtext)

    # Split the title into words by space or comma
    words = [word.strip() for word in re.split(r'[ ,]+', title)]
    
    # Initialize filtered_df with the first word
    filtered_df = df[df['title'].str.contains(words[0], case=False)]
    
    # Filter by subsequent words
    for word in words[1:]:
        filtered_df = filtered_df[filtered_df['title'].str.contains(word, case=False)]
    
    # Convert to list of dictionaries
    return filtered_df.to_dict(orient='records')
    for word in words[1:]:
        filtered_df = filtered_df[filtered_df['title'].str.contains(word, case=False)]
    
    # Convert to list of dictionaries
    return filtered_df.to_dict(orient='records')

df_emb = get_titles_and_umap_embeddings()
