from saari.common import *
from saari.utils.paper import df

import saari.components as c


def logo():
    # Wrap the SVG content in a Div with specific styles
    return Div(Img(src="/public/assets/saari_text.svg"), style="width: 110px; height: 130px; overflow: hidden; display: inline-block; position:absolute;")


def top_nav(session):
    study_id = session.get("study")
    return NavBarContainer(
            NavBarLSide(
                H1("Saari"),
                NavBarNav(
                   c.study.study_dropdown(study_id), 
                   #Li(A("Oves...rview")), 
                   #Li(A("Customers")), 
                   #Li(A("Products")), 
                   Button('+',cls=(ButtonT.primary, TextFont.bold_sm), uk_toggle="target: #StudyForm"),
                   #Li(A("Create new study")),

                cls='flex items-center'
                )),
            NavBarRSide(


                   
            )
        )

def NavSpacedLi(t,s): return NavCloseLi(A(DivFullySpaced(P(t),P(s,cls=TextFont.muted_sm))))


def page(session, study=None, search=None):
    user_id = session.get("user_id", str(uuid4()))
    session["user_id"] = user_id
    study_id = session.get("study", None)
    if search is None:
        papers = df.to_dict(orient='records')
    else:
        papers = []
        """search_results.xtra()
        def renderPapers(entries):
            return [ArticleItem({
                "title": entry.get("dc:title"),
                "journal": entry.get("prism:publicationName"),
                "author": entry.get("dc:creator"),
                "year": entry.get("prism:coverDate").split("-")[0]
            }, search="") for entry in search_results()]

        papers = search_results()"""

    if study_id is None:
        return Div(cls="space-y-4")(
        Div(cls="border-b border-border px-4")(c.layout.top_nav(session)), c.study.CreateStudyModal())

    if search is None:
        title = study.title + ": Combined view"
        search_id = None
    else:
        title = search.title + ": " + search.query
        search_id = search.id

    return Div(cls="space-y-4")(
        Div(cls="border-b border-border px-4")(c.layout.top_nav(session)),
        Grid(c.sidebar.sidebar(session),
            Div(cls="col-span-4 border-l border-border")(
                Div(cls="px-8 py-6")(
                    H2(title, cls='pb-4'),

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
                                Div(c.umap.render_umap(papers), id="umap"),
                                Form(
                                    Input(id="selected", value="", type="hidden"),
                                    #hx_trigger="ihavelassoedstuff",
                                    hx_post="/select",
                                    hx_target="#cluster_info",
                                    hx_swap="outerHTML",
                                    id="selectedform"
                                ),                          
                            ),
                            cls='col-span-4'
                        ),
                        Div(
                            c.paper.showPapers(study_id, search_id),
                            c.paper.render_papers(papers, study=study, search=search),     
                            cls='col-span-3  overflow-y-scroll h-[500px]'
                        ),
                        

                            gap=4, cols=7), 
                        
                        ),
                    ),
                        Div(logo(), cls="px-4"),  # Use the styled SVG wrapper here

            cols=5), c.study.CreateStudyModal(), c.search.CreateSearchModal())
