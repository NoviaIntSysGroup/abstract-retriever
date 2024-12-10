from fasthtml.common import *
#from utils.ai import *
from utils.paper import filter_by_title, get_sorted_list_of_papers, get_reranked_list_of_papers
from urllib.parse import quote, unquote
from hashlib import md5
from utils.paper import get_category_from_embeddings
from utils.umap import visualize_embeddings
from utils.paper import df
from uuid import uuid4
from utils.user_cache import user_cache


from fasthtml.common import *
from fh_frankenui.core import *
from fasthtml.svg import *
from fh_matplotlib import matplotlib2fasthtml
import numpy as np
import matplotlib.pylab as plt


description = "This application provides a user interface for visualizing and analyzing research papers, including features such as filtering, sorting, and reranking papers based on various criteria."
hdrs = (
    #picolink, Script(src="https://cdn.tailwindcss.com"),
    #Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"),
    #Link(picolink),
    Theme.slate.headers(),
    Title("SAARI - Scholarly Abstract Analysis & Review Interface"),
    Meta(charset='UTF-8'),
    Meta(name='viewport', content='width=device-width, initial-scale=1.0, maximum-scale=1.0'),
    Meta(name='description', content=description),
    *Favicon('/public/assets/favicon.svg', '/public/assets/saari_text.svg'),
    *Socials(title='SAARI - Scholarly Abstract Analysis & Review Interface ',
        description=description,
        site_name='saari.ai',
        image=f'/public/assets/og-sq.png',
        url=''),
    # surrsrc,    
    Link(rel="stylesheet", href="/public/src/style.css"),
    Script(src="/public/src/scripts.js")
)

#app = FastHTML(hdrs=hdrs, live=True)
app, rt = fast_app(
    hdrs=hdrs  # Use frankenui theme headers
)
rt = app.route

#app, rt = fast_app(live=True, hdrs=(
#))


def InfoCard(title, value, change):
    return Div(Card(
             Div(H3(value),
                P(change, cls=TextFont.muted_sm)),
             header=H4(title)))

rev = InfoCard("Total Revenue", "$45,231.89", "+20.1% from last month")
sub = InfoCard("Subscriptions", "+2350", "+180.1% from last month")
sal = InfoCard("Sales", "+12,234", "+19% from last month")
act = InfoCard("Active Now", "+573", "+201 since last hour")

top_info_row = Grid(rev,sub,sal,act,cols=4)

def title_to_id_attr(name):
    # Convert name to lowercase, replace spaces and underscores with '-', and remove non-latin characters
    return re.sub(r'[^a-z0-9\-]', '', 
                  name.lower()
                  .replace('å', 'a')
                  .replace('ä', 'a')
                  .replace('ö', 'o')
                  .replace(' ', '-')
                  .replace('_', '-'))

def ArticleItem(paper, search):
    if search is None:
        text = paper["title"]   
    else:
        text = higlight(paper["title"], search)

    return Div(cls="flex items-top mb-4 article_item", id=title_to_id_attr(paper["title"]))(
        #DiceBearAvatar(paper["title"], 9,9),
        UkIcon("file-text", height=30, width=20),

        Div(cls="ml-4 space-y-0")(
            P(text, cls=TextFont.bold_sm),
            P(str(paper["journal"]),", ", str(paper["year"]).split(".")[0], cls=TextFont.muted_sm)),
        Div("123", cls="ml-auto font-medium"),
    )

def list_papers(papers, search=None):
    return Div(*[ArticleItem(paper, search) for paper in (papers)], id="results")

"""
                                ),
                                header=Div(
                                    H3("Articles", id="result_title"),                    
                                    P("Showing 265 from this study.", cls=TextFont.muted_sm, id="result_desc")
                                ),



    if search is None:
        return Ul(*[Li(p["title"], id=title_to_id_attr(p["title"])) for p in papers])   
    else:
        return Ul(*[Li(higlight(p["title"], search), id=title_to_id_attr(p["title"])) for p in papers])

"""


@matplotlib2fasthtml
def generate_chart(num_points):
    plotdata = [np.random.exponential(1) for _ in range(num_points)]
    plt.plot(range(len(plotdata)), plotdata)


opt_hdrs = ["Personal", "Team", ""]

team_dropdown = UkSelect(
    Optgroup(label="Litterature studies")(
        Option(A("Virtual Sea Trial"))),
    )

hotkeys = [('Profile','⇧⌘P'),('Billing','⌘B'),('Settings','⌘S'),('New Team', ''), ('Logout', '')]

def NavSpacedLi(t,s): return NavCloseLi(A(DivFullySpaced(P(t),P(s,cls=TextFont.muted_sm))))

avatar_dropdown = Div(
      DiceBearAvatar('Alicia Koch',8,8),
      DropDownNavContainer(
          NavHeaderLi('sveltecult',NavSubtitle("leader@sveltecult.com")),
          *[NavSpacedLi(*hk) for hk in hotkeys],))

def logo():
    # Wrap the SVG content in a Div with specific styles
    return Div(NotStr("<style>.uk-h1 {display:none;}</style>"),Img(src="/public/assets/saari_text.svg"), style="width: 110px; height: 130px; overflow: hidden; display: inline-block; position:absolute;")


top_nav = NavBarContainer(
            NavBarLSide(
                NavBarNav(
                   team_dropdown, 
                   #Li(A("Oves...rview")), 
                   #Li(A("Customers")), 
                   #Li(A("Products")), 
                   Li(A("Create new study")),

                cls='flex items-center'
                )),
            NavBarRSide(


                   
            )
        )

def MusicSidebarLi(icon, text): 
    return Li(A(DivLAligned(UkIcon("file-search"), P(text), cls='space-x-2')))

sidebar = NavContainer(

    NavHeaderLi(H3("Virtual Sea Trial Litterature Review")),
    LabelInput("New Search", cls="px-4"),
    *[MusicSidebarLi(*o) for o in [("home", "Maritime ship, digital twin"), ("users", "C...ustomers"), ("box", "Products"), ("cog", "Settings")]],

    cls=(NavT.primary, 'space-y-3', 'pl-8'),
)

FlexBlockCentered = (FlexT.block,FlexT.center)

"""
def render_papers(papers, search=None):
    print("rendering...")
    return list_papers(papers,search), H3(f"Articles [{search}]", id="result_title"), P("Foo bar", id="result_desc")
"""

spinner = NotStr("<div uk-spinner></div>")

def render_papers(papers, data=None, search=None):
    print("data in cluster_info")
    print(data)
    if data is not None:        
        return Card(
                spinner,
                H4(data["headline"], id="result_title"),  # Updated key
                P(cls=TextFont.muted_sm, id="result_desc")(data["description"]),
                Div(cls=('flex','gap-x-4',TextFont.muted_sm), id="result_tags")(
                    *[Div(cls=FlexBlockCentered)(topic) for topic in data["topics"]],  # Updated key
                ),
                list_papers(papers, search),
                id="cluster_info",
                hx_swap_oob='true',
                hx_swap='outerHTML'
            )
    else:
        return  Card(
            spinner,
            Div(cls="space-y-8", id="results")(
                list_papers(papers, search)
            ),
            header=Div(
                H3("Articles", id="result_title"),                    
                P("Showing 265 from this study.", cls=TextFont.muted_sm, id="result_desc")
            ),
            id="cluster_info", hx_swap_oob='true', hx_swap="outerHTML"
        ),         
        return Div(id="cluster_info", hx_swap_oob='true', hx_swap="outerHTML")

def page(session):
    user_id = session.get("user_id", str(uuid4()))
    session["user_id"] = user_id
    papers = df.to_dict(orient='records')
    
    return Div(cls="space-y-4")(
        Div(cls="border-b border-border px-4")(top_nav),
        Grid(sidebar,
            Div(cls="col-span-4 border-l border-border")(
                Div(cls="px-8 py-6")(
                    H2('Search: Maritime ship, digital twin', cls='pb-4'),

                    Div(
                        Form(
                            Grid(
                                LabelInput("Match Text", id="embedding_search"),
                                LabelRange(label='Clusters', min="1", step="1", max="20", value="1", id="cluster_amount"),
                                LabelInput("Filter", id="search"),

                                #Input(type="range", min="0", step="0.01", max="1", value="1", id="distance_filter"),
                                #Group(Label("Clusters "),Input(type="range", min="1", step="1", max="20", value="1", id="cluster_amount")),

                                #Input(id="search", placeholder="Filter Abstracts (Based on Title)"),
                                cols=3, gap=4,
                            ),
                            hx_trigger="input", hx_post="/search", hx_target="#results", hx_swap="innerHTML"
                        ),
                        cls="mb-4"
                    ),
                    Grid(
                        Div(
                            Card( 
                                Div(render_umap(papers), id="umap"),
                                Form(
                                    Input(id="selected", value="", type="hidden"),
                                    #hx_trigger="ihavelassoedstuff",
                                    hx_post="/select",
                                    hx_target="#cluster_info",
                                    hx_swap="outerHTML",
                                    id="selectedform"
                                ),                          
                                #generate_chart(10),
                            ),
                            cls='col-span-4'
                        ),
                        Div(
                            render_papers(papers),     
                            cls='col-span-3  overflow-y-scroll h-[500px]'
                        ),
                        

                            gap=4, cols=7), 
                        
                        ),
                    ),
                        Div(logo(), cls="px-4"),  # Use the styled SVG wrapper here

            cols=5))



@rt("/")
def get(session):
    
    return Titled("Saari", page(session))

    user_id = session.get("user_id", str(uuid4()))
    session["user_id"] = user_id
    papers = df.to_dict(orient='records')
    
    return Titled("SAARI - Scholarly Abstract Analysis & Research Insights", 
                
                Grid(
                    Div(
                        Form(
                            Group(
                                Textarea(id="embedding_search", placeholder="Order results based on relevance to this text. You can describe your research questions, approach or project description."),

                            ),
                            #Input(type="range", min="0", step="0.01", max="1", value="1", id="distance_filter"),
                            Group(Label("Clusters "),Input(type="range", min="1", step="1", max="20", value="1", id="cluster_amount")),

                            Input(id="search", placeholder="Filter Abstracts (Based on Title)"),
                            hx_trigger="input", hx_post="/search", hx_target="#results", hx_swap="innerHTML"
                        ),

                        Hr(),
                        Div(render_umap(papers), id="umap"),
                        Form(
                            Input(id="selected", value="", type="hidden"),
                            #hx_trigger="ihavelassoedstuff",
                            hx_post="/select",
                            hx_target="#category",
                            hx_swap="innerHTML",
                            id="selectedform"
                        ),
                        Div(id="category")
                    ),
                    Div(H1("Papers"), Div(list_papers(papers), id="results")),
                    id="app"
                )
                

            )
"""def list_papers(papers, search=None):
    if search is None:
        return Ul(*[Li(p["title"], id=title_to_id_attr(p["title"])) for p in papers])   
    else:
        return Ul(*[Li(higlight(p["title"], search), id=title_to_id_attr(p["title"])) for p in papers])
"""

def higlight(text: str, words: str):
    w = [word.strip() for word in re.split(r'[ ,]+', words)]
    for word in w:
        if len(word) > 1:
            text = re.sub(word, f"<u><b>{word}</b></u>", text, flags=re.IGNORECASE)
    return NotStr(text)

import re




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

    return render_papers(papers, data)


@rt("/search")
def post(session, embedding_search: str, search: str, cluster_amount: int):
    #def post(session, embedding_search: str, search: str, distance_filter: float, labeling: str, cluster_amount: int):
    print("searching....", embedding_search)
    global user_cache
    user_id = session.get("user_id")
    cluster_amount = int(cluster_amount)
    
    # Retrieve the user's cache
    user_id = session.get('user_id', 'default_user')  # Use a unique identifier for each user
    user_cache.setdefault(user_id, {'last_embedding_search': None, 'cached_sorted_papers': None})
    
    # Check if the current embedding search is the same as the last one for this user
    #if embedding_search == user_cache[user_id]['last_embedding_search']:
    #    df2 = user_cache[user_id]['cached_sorted_papers']
    #else:
    
    # Print the title of the first paper in df
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
    
    return (render_papers(papers, data=None, search=search), render_umap(papers, distance_filter=1, cluster_amount=cluster_amount))


def render_umap(papers, cluster_amount: int = 1, distance_filter: float = 1):
    # Debugging: Check if papers is empty
    if not papers:
        raise ValueError("No papers provided for visualization.")

    # Debugging: Print the contents of papers
    #print("Papers for visualization:", papers)

    # Check for valid embeddings
    if not any(p.get('embedding') for p in papers):
        return Div("No valid embeddings found for visualization.", id="umap", hx_swap_oob='true')

    return Div(
        NotStr(visualize_embeddings(papers, distance_filter, n_clusters=cluster_amount)),        
        id="umap", hx_swap_oob='true')


serve(port=5013)

"""Group(
    Select(
        Option("Proximity to Embedding", value="proximity"),
        Option("Automatically Clustering", value="clustered"),
        Option("Named Clusters", value="custom"),
        id="labeling"
    ),
    Select(
        *[Option(i, value=i) for i in range(1,30)],
        id="amount_of_clusters"
    ),
),



#Hr(),
Grid(
    Div("Tag cloud"),
    Div("Excluded categories")
),"""