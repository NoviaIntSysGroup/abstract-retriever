from fasthtml.common import *
import pandas as pd
import re, os
from openai import AzureOpenAI
from rerankers import Reranker

from scipy import spatial
from dotenv import load_dotenv  # for loading environment variables from a .env file
load_dotenv()  # load environment variables from .env file


client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_API_BASE"),
                api_version=os.getenv("AZURE_API_VERSION"),
                api_key=os.getenv("AZURE_API_KEY")
        )


import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import ast
from .decorators import timed, timing
from typing import List, Optional
import json



df = pd.read_csv("data/papers_with_umap.csv")

@timed
def get_embeddings_and_labels(limit=1000):
    # return tuple with "title" and "embedding" from df
    embeddings_and_labels = []
    for index, row in df.iterrows():
        if index >= limit:
            break
        title = row['title']
        embedding = row['embedding']
        embeddings_and_labels.append((title, embedding))
    return embeddings_and_labels



@timed
def get_reranked_list_of_papers(q: str="foo", limit=1000, df=df) -> Optional[pd.DataFrame]:
    #ranker = Reranker(f"azure/gpt-4o", model_type="rankgpt", api_key = os.environ['AZURE_API_KEY'])
    ranker = Reranker('cross-encoder', verbose=0)
    df = df.fillna({'title': '', 'abstract': ''})
    docs = [title for title in df['title']]
    ranked_results = ranker.rank(query=q, docs=docs)

    # Extract text, rank, and score from ranked results
    ranked_data = [
        {'title': result.document.text, 'rank': result.rank, 'score': result.score if result.score is not None else 0}
        for result in ranked_results.results
    ]

    # Create a DataFrame from the ranked data
    ranked_df = pd.DataFrame(ranked_data)
    print("ranked_df\n", ranked_df.head())
    merged_df = df.merge(ranked_df, on='title', how='left', suffixes=('', '_ranked'))
    merged_df['score_ranked'] = merged_df['score_ranked'].fillna(float('-inf'))
    print("merged_df\n", merged_df.head())

    # Sort the merged DataFrame by score_ranked in descending order
    sorted_df = merged_df.sort_values(by='score_ranked', ascending=False)
    print("sorted_df\n", sorted_df.head())
    return sorted_df

@timed
def get_sorted_list_of_papers(q: str="foo", limit=1000, df=df) -> Optional[pd.DataFrame]:
    with timing("slop A"):
        # Calculate the query embedding
        batch = [str(q)]
        EMBEDDING_MODEL = "text-embedding-3-small"
        BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

        try:
            response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
            for i, be in enumerate(response.data):
                assert i == be.index  # double check embeddings are in same order as input
            e = [e.embedding for e in response.data]
            query_embedding = e[0]
        except Exception as e:
            #raise e
            return
    with timing("slop B"):

        # Define distance metrics
        distance_metrics = {
            "cosine": spatial.distance.cosine,
            "L1": spatial.distance.cityblock,
            "L2": spatial.distance.euclidean,
            "Linf": spatial.distance.chebyshev,
        }

        # Ensure embeddings are 1-D and numeric
        query_embedding = np.array(query_embedding, dtype=np.float64).flatten()
    with timing("slop C"):

        # Convert all embeddings in the DataFrame to a 2D NumPy array
        embeddings_list = [ast.literal_eval(embedding) for embedding in df['embedding']]
        embeddings_array = np.array(embeddings_list, dtype=np.float64)

        # Ensure all embeddings are the same size as the query embedding
        valid_mask = np.array([len(embedding) == query_embedding.size for embedding in embeddings_list])
        valid_embeddings = embeddings_array[valid_mask]

        # Check if valid_embeddings is empty
        if valid_embeddings.size == 0:
            distances = np.array([])  # No valid embeddings to compare
        else:
            # Calculate cosine distances using vectorized operations
            distances = spatial.distance.cdist([query_embedding], valid_embeddings, 'cosine')[0]

        # Assign a large distance for invalid embeddings
        distances_full = np.full(df.shape[0], float('inf'))
        distances_full[valid_mask] = distances
    with timing("slop D"):

        # Add distances to the DataFrame
        df2 = df.assign(distance=distances_full)

        # Normalize distances
        min_distance = df2['distance'].min()
        max_distance = df2['distance'].max()
    with timing("slop E"):

        # Check for zero denominator
        if max_distance != min_distance:
            df2['distance'] = (df2['distance'] - min_distance) / (max_distance - min_distance)
        else:
            df2['distance'] = 0  # or handle it in another way, e.g., set to a constant
    with timing("slop F"):
        # Sort the DataFrame by distance
        sorted_df = df2.sort_values(by='distance')

    # Debugging: Check if sorted_df is empty
    if sorted_df.empty:
        print("Warning: sorted_df is empty. Check the input DataFrame and query.")

    return sorted_df if not sorted_df.empty else None  # Ensure a DataFrame is returned


@timed
def filter_by_title(df2, title):
    if df2 is None:
        raise ValueError("The DataFrame is None. Ensure get_sorted_list_of_papers returns a valid DataFrame.")
    """
    Searches the dataframe for rows where the 'title' column matches the given title.

    Parameters:
    - df (pandas.DataFrame): The dataframe to search in.
    - title (str): The title to search for.

    Returns:
    - list: A list of dictionaries containing the rows where the 'title' column matches the given title, ordered by relevance.
    """

    if title == "":
        # Return the entire DataFrame as a list of dictionaries if title is empty
        return df2.to_dict(orient='records')

    # Split the title into words by space or comma
    words = [word.strip() for word in re.split(r'[ ,]+', title)]
    if words is None:
        words = []

    # Initialize filtered_df with the first word
    if len(words) > 0:
        filtered_df = df2[df2['title'].str.contains(words[0], case=False)]
    else:
        filtered_df = df2

    # Filter by subsequent words
    for word in words[1:]:
        filtered_df = filtered_df[filtered_df['title'].str.contains(word, case=False)]

    # Convert to list of dictionaries
    return filtered_df.to_dict(orient='records')

@timed
def get_category_from_embeddings(titles: List, cluster_amount=None, current_cluster_nr=None, previous_level=None):
    # Filter df so that it only includes the ones where the title is in titles list
    filtered_df = df[df['title'].isin(titles)]

    

    # Ensure the embedding column is evaluated to a list
    filtered_df['embedding'] = filtered_df['embedding'].apply(ast.literal_eval)

    # Calculate the centroid of the embeddings
    centroid = np.mean(filtered_df['embedding'].tolist(), axis=0)

    # Calculate the cosine distance between each embedding and the centroid
    filtered_df['distance_to_centroid'] = cosine_distances(filtered_df['embedding'].tolist(), [centroid]).flatten()

    # Sort the DataFrame by distance to the centroid
    sorted_df = filtered_df.sort_values(by='distance_to_centroid')

    top_papers = sorted_df[['title', 'abstract']].head(20).to_dict(orient='records')

    # Prepare the prompt for OpenAI GPT-4
    prompt = "Based on the following titles and abstracts (that are sorted by distance to the centroid of their text embeddings on text+abstract), what is the common topic?\n\n"
    if previous_level is not None and cluster_amount is not None  and current_cluster_nr is not None:
        prompt = f"We are now processing one cluster out of {cluster_amount}, I will show you what clusters were called when all papers were split into different amount of clusters. Since what we are processing now might be a subset of something, this clusters nameing will probably be 'narrower' and not broader. Make it specific, and bear in mind that the user will see the oter clusters simoultaneously when this data is used, so avoid adding words that will be repeated in all clusters." + prompt

    for paper in top_papers:
        title = paper['title']
        abstract = paper['abstract']
        prompt += f"Title: {title}\nAbstract: {abstract}\n\n"




    # Call OpenAI GPT-4 to get the topic
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=10000,
        messages = [
            {"role": "system", "content" : "You are a text analyser and can read the abstract text of research papers that have been clustered to gether based on text embedding similarity and you are able to extract what the texts are about, why were they clustered together. You provide this service as part of a tool for litterature review analysis where researchers see bunch of papers clustered together and they select a cluster and you tell them what that part of the umap embedding visualisation is about. This allows the researchers to detect topics in papers. "},
            {"role": "user", "content": prompt}
        ],
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "extracted_data",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "headline": {
                            "type": "string",
                            "description": "Headline or name for this cluster",
                        },
                        "description": {
                            "type": "string",
                            "description": "A text describing what this cluster of abastracts is about",
                        },
                        "topics": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A key topic or keyword extracted from abstracts in this cluster",
                            }
                        },                        
                    },
                    "required": ["headline", "description", "topics"],
                    "additionalProperties": False
                }
            }
        },
        n=1,
        stop=None,
        temperature=0
    )
    # Extract the topic from the response
    topic_json = response.choices[0].message.content
    data = json.loads(topic_json)  # Convert JSON string to a dictionary
    return data;

    # Convert the filtered DataFrame to a list of titles

    #return NotStr("<br>".join(filtered_titles))


def title_to_id_attr(name:str):
    # Convert name to lowercase, replace spaces and underscores with '-', and remove non-latin characters
    return re.sub(r'[^a-z0-9\-]', '', 
                  name.lower()
                  .replace('å', 'a')
                  .replace('ä', 'a')
                  .replace('ö', 'o')
                  .replace(' ', '-')
                  .replace('_', '-'))

