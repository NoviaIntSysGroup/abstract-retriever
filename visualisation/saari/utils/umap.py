#from .paper_old import db, df_emb
from .paper import df as df_emb
import pandas as pd
import plotly.express as px
from umap import UMAP
from sklearn.cluster import KMeans
import ast
import numpy as np
from .decorators import timed, timing
from .user_cache import user_cache
from .paper import df

@timed
def update_umap(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine'):
    umap = UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components, metric=metric, random_state=42)
    X_tfm = df_emb['embedding'].apply(eval).tolist()
    umap_embeddings = umap.fit_transform(X_tfm)
    df_emb['umap_x'] = umap_embeddings[:, 0]
    df_emb['umap_y'] = umap_embeddings[:, 1]
    return df_emb

#umap_embeddings = update_umap(n_neighbors=30, min_dist=0 )

def get_labels(n_clusters):

    if df[f'labels_{n_clusters}'] is None:
        kmeans = KMeans(n_clusters=int(n_clusters), random_state=0).fit(embeddings)
        
        labels = kmeans.labels_

    df[f'labels_{n_clusters}'] = labels


@timed
def visualize_embeddings(papers, distance_filter: float = 1, n_clusters=1, u_emb=None):
    # Convert papers list to DataFrame
    with timing("papers_df = pd.DataFrame(papers)"):
        papers_df = pd.DataFrame(papers)
        
    #print(papers_df.iloc[0].to_dict())  # Print all columns and data as dict for the first row
    
    # Ensure 'distance' column exists in papers_df
    if 'distance' not in papers_df.columns:
        papers_df['distance'] = 1  # Add distance column with default value 1


    #print(papers_df.columns)

    # Normalize the distance values in papers_df to be between 0 and 1
    max_distance = papers_df['distance'].max()
    min_distance = papers_df['distance'].min()
    if max_distance != min_distance:
        papers_df['distance'] = (papers_df['distance'] - min_distance) / (max_distance - min_distance)
    else:
        papers_df['distance'] = 1  # Set to 1 if all distances are the same

    #print(papers_df.columns)

    # Filter df_emb to only include the ones from df_emb that share the title with papers
    df_emb_filtered = df_emb[df_emb['title'].isin(papers_df['title'])]
    #print(df_emb_filtered.columns)
    #print("Before merge, df_emb size:", df_emb.shape)
    #print("Before merge, papers_df size:", papers_df.shape)
    #print("Before merge, df_emb titles:", df_emb['title'].unique()[0:10])
    #print("Before merge, papers_df titles:", papers_df['title'].unique()[0:10])
    
    with timing("df_emb_filtered = df_emb_filtered.merge"):
        df_emb_filtered = df_emb_filtered.merge(
            papers_df[['title', 'distance']], 
            on='title', 
            suffixes=('_emb', '_papers')
        )
    #print("After merge, df_emb_filtered size:", df_emb_filtered.shape)
    
    with timing("A"):
        
        # Convert string embeddings to list using ast.literal_eval
        def safe_literal_eval(val):
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                return None
    with timing(".apply(safe_literal_eval)"):
        embeddings = np.array(df_emb_filtered['embedding'].tolist())

        #df_emb_filtered['embedding'] = df_emb_filtered['embedding'].apply(safe_literal_eval)
    with timing("B1"):

        # Drop any rows where conversion failed
        df_emb_filtered = df_emb_filtered.dropna(subset=['embedding'])
    with timing("B2"):
    
        # Ensure all embeddings are lists of numbers
        embeddings = np.array(df_emb_filtered['embedding'].tolist())
        
        # Fit KMeans
        #print(f"clustering with {n_clusters} clusters")
        
        label_col = f"labels_{n_clusters}"
    with timing("C"):
        df_emb_filtered = df_emb_filtered[df_emb_filtered['distance'] <= distance_filter]
        #print("After distance filter, df_emb_filtered size:", df_emb_filtered.shape)
        # Normalize the distance values to be between 0 and 1 for opacity
        df_emb_filtered['opacity'] = (df_emb_filtered['distance'] - df_emb_filtered['distance'].min()) / (df_emb_filtered['distance'].max() - df_emb_filtered['distance'].min())
        
        # Replace NaN values in 'opacity' with 1
        df_emb_filtered['opacity'] = df_emb_filtered['opacity'].fillna(1)
        
    # Create a scatter plot with additional customizations
    with timing("fig = px.scatter"):
        #print(df_emb_filtered.size)
        fig = px.scatter(
            df_emb_filtered,
            x='umap_x',
            y='umap_y',
            hover_data=['title'],
            size_max=10,
            color=label_col,
            opacity=df_emb_filtered['opacity'],
            color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
        )

    with timing("fig.update_layout"):
        # Update the layout to remove axis labels, ticks, reduce margins, and enable lasso by default
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),  # Adjust the margins to reduce space
            xaxis=dict(visible=False),  # Hide the x-axis
            yaxis=dict(visible=False),  # Hide the y-axis
            
            coloraxis_showscale=False,  # Hide the color scale
            dragmode="lasso",  # Set lasso select as the default interaction mode
        )
        
        # Remove unnecessary modebar buttons, keeping only lasso select
        fig.update_traces(marker=dict(size=7), selector=dict(mode='markers'))
        fig.update_layout(
            modebar_remove=[
                'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 
                'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'
            ],
            modebar_add=['lasso2d']  # Ensure only lasso select is available
        )
    with timing("fig.to_html"):

        # Convert the plot to HTML
        html_plot = fig.to_html()

    return html_plot
