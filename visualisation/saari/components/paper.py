from saari.utils.paper import title_to_id_attr
import saari.components as c
from fasthtml.common import *
from fh_frankenui.core import *
import re

def ArticleItem(paper, search):
    if search is None:
        text = paper["title"]   
    else:
        text = higlight(paper["title"], search)

    return Div(cls="flex items-top mb-4 article_item", id=title_to_id_attr(paper.get("title", "")))(
        #DiceBearAvatar(paper["title"], 9,9),
        UkIcon("file-text", height=30, width=20),

        Div(cls="ml-4 space-y-0")(
            P(text, cls=TextFont.bold_sm),
            P(str(paper["journal"]),", ", str(paper["year"]).split(".")[0], cls=TextFont.muted_sm)),
        Div("123", cls="ml-auto font-medium"),
    )

def list_papers(papers, search_query=None):
    return Div(*[ArticleItem(paper, search_query) for paper in (papers)], id="results")


def higlight(text: str, words: str):
    w = [word.strip() for word in re.split(r'[ ,]+', words)]
    for word in w:
        if len(word) > 1:
            text = re.sub(word, f"<u><b>{word}</b></u>", text, flags=re.IGNORECASE)
    return NotStr(text)

def render_papers(papers, data=None, search_query=None, study=None, search=None):
    print("data in cluster_info")
    print(data)
    if data is not None:        
        return Card(
                c.general_ui.spinner,
                H4(data["headline"], id="result_title"),  # Updated key
                P(cls=TextFont.muted_sm, id="result_desc")(data["description"]),
                Div(cls=('flex','gap-x-4',TextFont.muted_sm), id="result_tags")(
                    *[Div(cls=c.general_ui.FlexBlockCentered)(topic) for topic in data["topics"]],  # Updated key
                ),
                list_papers(papers, search_query),
                id="cluster_info",
                hx_swap_oob='true',
                hx_swap='outerHTML'
            )
    else:
        return  Card(
            c.general_ui.spinner,
            Div(cls="space-y-8", id="results")(
                list_papers(papers, search_query)
            ),
            header=Div(
                H3("Articles", id="result_title"),                    
                P(f"Showing {len(papers)} from this study.", cls=TextFont.muted_sm, id="result_desc")
            ),
            id="cluster_info", hx_swap_oob='true', hx_swap="outerHTML"
        ),         
        return Div(id="cluster_info", hx_swap_oob='true', hx_swap="outerHTML")

def showPapers(study_id:str, search_id:str, match_text:str=None, filter_text:str= None):
    return ""
    return Table(
        Tr(Td("Study"), Td(study_id)),
        Tr(Td("Search"), Td(search_id)),
        Tr(Td("Match Text"), Td(match_text)),
        Tr(Td("Filter Text"), Td(filter_text)
    )

)
