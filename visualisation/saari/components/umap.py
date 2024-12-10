from saari.common import *
from saari.utils.umap import *

def render_umap(papers, cluster_amount: int = 1, distance_filter: float = 1):
    # Debugging: Check if papers is empty
    if not papers:
        return Div("...")
        raise ValueError("No papers provided for visualization.")

    # Debugging: Print the contents of papers
    #print("Papers for visualization:", papers)

    # Check for valid embeddings
    if not any(p.get('embedding') for p in papers):
        return Div("No valid embeddings found for visualization.", id="umap", hx_swap_oob='true')

    return Div(
        NotStr(visualize_embeddings(papers, distance_filter, n_clusters=cluster_amount)),        
        id="umap", hx_swap_oob='true')
