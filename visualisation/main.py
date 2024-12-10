from saari.common import *

from saari.utils.paper import title_to_id_attr, get_category_from_embeddings, filter_by_title, get_sorted_list_of_papers, get_reranked_list_of_papers, df
from saari.utils.umap import visualize_embeddings
from saari.utils.user_cache import user_cache
from saari.utils.elsevier import *

import saari.components as c
from saari.app import app, rt

@rt("/")
def get(session):
    study_id = session.get("study", None)
    if  study_id == None:
        return Titled("Saari", c.laoyout.page(session, None, None))

    try:
        study = studies[study_id]
        return RedirectResponse(f"/study/{study_id}")
    except:
        session['study'] = None # probably som old value
        searches.xtra(study = None)
        return Titled("Saari", c.layouy.page(session, study, None))


    
@rt("/study/{study_id}/search/{search_id}")
def get(study_id:str, search_id:str, session):
    user_id = session.get("user_id", str(uuid4()))
    session["user_id"] = user_id
    study = c.study.get_study(study_id)
    if study is None:
        return RedirectResponse("/")

    
    searches.xtra(study=study_id)
    search = searches[search_id]
    session["search"] = search_id
    return Titled("Saari", c.layout.page(session, study, search))


@rt("/study/{study_id}")
def get(study_id:str, session):

    searches.xtra(study=study_id)
    session['study'] = study_id
    if "search" in session:
        del session["search"]

    try:
        study = studies[study_id]
    except:
        return Title("Error")
    
    return Titled("Saari", c.layout.page(session, study=study))



@rt("/select")
def post(selected:str):
    titles = selected.split(";;;")
    print("titles is")
    print(titles)
    if (len(titles) == 1 and titles[0] == '') or len(titles) == 0:
        papers = df.to_dict(orient='records')
        data = None
    else:
        print("selecting...")
        data = get_category_from_embeddings(titles)
        #return cluster_info(data)
        
        titles_set = set(titles)
        
        papers = df.to_dict(orient='records')
        ps = [paper for paper in papers if paper["title"] in titles_set]

        papers = df.to_dict(orient='records')
        
        # Filter papers to only include those with titles in titles_set
        papers = [paper for paper in papers if paper["title"] in titles_set]

    return c.paper.render_papers(papers, data)


@rt("/search")
def post(session, embedding_search: str, search: str, cluster_amount: int):

    print("searching....", embedding_search)
    global user_cache
    user_id = session.get("user_id")
    cluster_amount = int(cluster_amount)
    
    # Retrieve the user's cache
    user_id = session.get('user_id', 'default_user')  # Use a unique identifier for each user
    user_cache.setdefault(user_id, {'last_embedding_search': None, 'cached_sorted_papers': None})
    
    
    if not df.empty:
        print("First title in df:", df.iloc[0]['title'])
    
    if embedding_search is not None and len(embedding_search) > 3:
        df2 = get_reranked_list_of_papers(embedding_search)
    else:
        df2 = df
    
    # Print the title of the first paper in df2
    if not df2.empty:
        print("First title in df2:", df2.iloc[0]['title'])
    
    # Update the user's cache
    user_cache[user_id]['last_embedding_search'] = embedding_search
    user_cache[user_id]['cached_sorted_papers'] = df2

    # Check if df2 is None and handle the error
    if df2 is None:
        raise ValueError("No papers found for the given embedding search.")

    papers = filter_by_title(df2, search)
    
    return (c.paper.render_papers(papers, data=None, search_query=search), c.umap.render_umap(papers, distance_filter=1, cluster_amount=cluster_amount))



serve(port=5013)
