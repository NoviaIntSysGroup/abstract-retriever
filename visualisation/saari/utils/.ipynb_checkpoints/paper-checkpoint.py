import pandas as pd
import re

"""
import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32
import numpy as np

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

vec_version, = db.execute("select vec_version()").fetchone()
print(f"vec_version={vec_version}")

n_feats= 400
db.execute(f"CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[{n_feats}])")
result = db.execute('SELECT name from sqlite_master').fetchall()
print(result)

embedding = [0.1, 0.2, 0.3, 0.4]
result = db.execute('select vec_length(?)', [serialize_float32(embedding)])

print(result.fetchone()[0]) # 4

embedding = np.array([0.1, 0.2, 0.3, 0.4])

db.execute(
    "SELECT vec_length(?)", [embedding.astype(np.float32)]
) # 4"""

data_path = '/Users/toffe/dev/ai/novia/lib/serach-comparison/data/search_results.csv'
df = pd.read_csv(data_path)

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

def search_by_title(title):
    """
    Searches the dataframe for rows where the 'title' column matches the given title.

    Parameters:
    - df (pandas.DataFrame): The dataframe to search in.
    - title (str): The title to search for.

    Returns:
    - list: A list of dictionaries containing the rows where the 'title' column matches the given title, ordered by relevance.
    """
    
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
