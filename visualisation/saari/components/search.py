from saari.common import *
from saari.utils.paper import *
from saari.utils.elsevier import *

from saari.app import rt
# Route / new_search
@rt("/new_search")
def post(title:str, query:str, session):
    study_id = session.get("study")
    search = Search(id=uuid4(), study=study_id, query="query", title=title, lastupdated=0)
    search = searches.insert(search)
    return RedirectResponse(f"/study/{study_id}/search/{search.id}")


@rt("/generate_query")
def post(search_description: str):
    name, query, goal = transform_to_scopus_query(search_description)
    return scopusSearchForm(name, query, goal)    

@rt
def article_search(action:str, title:str, query: str, start:int=0):
    print("action",action)
    print("title",title)
    print("query",query)
    if action=="search":
        amount = 10
        found_papers = search_elsevier_api(query, api_key=os.getenv("ELSEVIER_API_KEY"), max_results=amount, start=start)
        loadmore = loadmoreform({"action":action, "title":title, "query":query, "start": start+amount})
        print(found_papers)
        if found_papers is None or len(found_papers) == 0:
            return Div("... that's all i found ...")
        if start == 0:
            return Div(
                Div(
                    *renderPapers(found_papers),
                    loadmore,
                    id="result-papers"
                ),
                id="search-results"
            )
        elif start < 30:
            return (*renderPapers(found_papers),
                    loadmore)
        else:
            return Div(".. thats plenty enough ...")
        
    elif action=="save":
        print("oke hten..")
        search = Search(id=uuid4(), query=query, title=title, lastupdated=0)
        search = searches.insert(search)
        print(search)
        start = 0
        amount = 10
        cont = True
        order = 1;

        while cont:
            results = search_elsevier_api(query, api_key=os.getenv("ELSEVIER_API_KEY"), max_results=amount, start=start)
            if results is None:
                cont = False
                results = []
                break
            
            for entry in results:
                print("Getting for", entry)
                for link in entry.get("link", []):
                    if link.get("@ref") == "scopus":
                        url = link.get("@href")
                        content = load_scopus_url(url)
                        with open("data/scopusdata.html", 'w') as file:
                            file.write(content)
                        
                        if 'sc-page-title pageTitle="Welcome to Scopus Preview"' not in content:
                            data = parse_scopus_html(content)
                            print(data)
                            paper = combine_scopus_data(entry, data)
                            paper = papers.upsert(paper)
                            search_results.insert(search=search.id, paper = paper.id, order=order)
                            
                        else:
                            print("somekind of wall...")
                #break
                order += 1
            cont = False
                
            
            
                
            start = start + amount


def CreateSearchModal():
    return Modal(
        Div(cls='p-6')(
            ModalTitle('Create new Search'),
            P('Fill out the information below to create a new search', cls=TextFont.muted_sm),
            Br(),
            Grid(

                Textarea(
                    label='Search Description', 
                    name="search_description", 
                    placeholder='Describe what kind of papers you are trying to find, then AI will help you fill in the rest.',
                    cls="uk-textarea col-span-12",
                    hx_post="/generate_query", 
                    hx_trigger="keyup changed delay:500ms",  # Trigger after typing stops for 500ms
                    hx_target="#search-form",
                    hx_swap="innerHTML"
                ),
                cols=12, gap=4, 

            ),
            Div(cls='space-y-4')(
                Br(),
                DividerSplit("Or fill in manually", text_cls = (TextT.small, TextT.muted)),
                Br(), # ugly yes. time shortage...
            ),
            scopusSearchForm(),
        ),
        Div("", id="search-results"),
        id='SearchForm',
    )
    


def scopusSearchForm(name:str = "", query:str = "", goal:str = ""):
    return Form(id="search-form", hx_post=article_search, hx_target="#search-results", method="post", cls='space-y-6')(
                Grid(
                    Input(label='Name', name="title", placeholder='Name', value=name, cls="col-span-4"),
                    Input(label='Goal', name="goal", placeholder='Goal', value=goal, cls="col-span-5"),
                    cols=12, gap=4,
                ),
                Grid(
                    Input(label='Query', name="query", value=query, placeholder='The Search Query (Scopus)', cls="col-span-9"),
                    Button(UkIcon("file-search", cls="pr-2"), Span("Try the Search on Scopus"), cls=("col-span-3", ButtonT.secondary), name="action", value="search"),
                    Button('Include this search in the study', cls=("col-span-3", ButtonT.primary), name="action", value="save", **{"uk-toggle": "target: #SearchForm"}),
                    ModalCloseButton('Cancel', cls=("col-span-1", ButtonT.ghost)),
                    cols=12, gap=4,
                ),
            ),




    





def loadmoreform(data:dict):
    print("laodmore", data)
    return Form(  id="loadmoreform",
        hx_trigger="load",
        hx_swap="outerHTML",
        hx_post=article_search)(
        *[Hidden(name=name, value=value) for name, value in data.items()]
    )

def renderPapers(entries):
    if entries is not None:
        return [ArticleItem({
            "title": entry.get("dc:title"),
            "journal": entry.get("prism:publicationName"),
            "author": entry.get("dc:creator"),
            "year": entry.get("prism:coverDate", "").split("-")[0]
        }, search="") for entry in entries]
    else:
        return []