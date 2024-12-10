from saari.common import *
import saari.components as c
    
def CreateNewSearchForm(session):
    return   Div(cls="flex items-center justify-between m-y-4")(
                        Div(cls="max-w-80")(),
                        Button(cls=ButtonT.primary, uk_toggle="target: #SearchForm")(Span(cls="mr-2 size-4")(UkIcon('circle-plus')),"Add search"))

    return Button('+',cls=(ButtonT.primary, TextFont.bold_sm), uk_toggle="target: #SearchForm"),

    
    return Form(action="/new_search", method="POST")(
        Card(
            H3("Search for Papers"),
            P("This will create a new Scopus search and start fetching abstracts for the papers."),
            Input(label='Name', name="title", placeholder='Title'),
            Input(label='Query', name="query", placeholder='Search Query (Scopus)', cls="col-span-8"),

            Button('New Search',cls=(ButtonT.primary, TextFont.bold_sm), uk_toggle="target: #SearchForm")
        )
    )


def sidebar(session):
    study_id = session.get("study")
    study = c.study.get_study(study_id, True)
    current_search_id = session.get("search", None) 
    try:
        s = searches()
    except:
        s = []

    return Div()(
        SearchSidebarLinkAll(study_id, selected=(current_search_id is None)),
        *[SearchSidebarLink(study_id, search, selected=(current_search_id == search.id)) for search in s],
        CreateNewSearchForm(session)

    )

    return NavContainer(

    NavHeaderLi(
        Form(
            Div(cls="flex justify-between items-center")(
                H3(study.title, cls="flex-grow"),
                UkIcon("trash-2", height=30, width=20, cls="ml-auto")
            ),
            hx_post=f"/delete-study",
            
        )
    ),
    #Li(A(href=f"/study/{study_id}")(DivLAligned(UkIcon("asterisk"), P("All"), cls='space-x-2'))),
    

    CreateNewSearchForm(session),

    cls=(NavT.primary, 'space-y-3', 'pl-8'),
)



def SearchSidebarLi(study_id, search):
    return Li(A(href=f"/study/{study_id}/search/{search.id}")(DivLAligned(UkIcon("file-search"), P(search.title), cls='space-x-2')))
    
def SearchSidebarLink(study_id, search, icon="file-search", selected=False):
    return Div(cls=(*c.general_ui.FlexBlockCentered, 'space-x-4 mb-2 search-row', "selected" if selected else "not-selected"))(
        UkIcon(icon),
        A(cls='flex-1', href=f"/study/{study_id}/search/{search.id}")(
            P(search.title, cls=(TextFont.bold_sm if selected else TextFont.muted_sm)),
            P(search.query, cls=TextFont.muted_sm)),
        A(UkIcon("trash"), cls="search-trash"),
    )

def SearchSidebarLinkAll(study_id, selected=False):
    return Div(cls=(*c.general_ui.FlexBlockCentered, 'space-x-4 mb-2 search-row', "selected" if selected else "not-selected"))(
        UkIcon("asterisk"),
        A(cls='flex-1', href=f"/study/{study_id}")(
            P("All papers", cls=(TextFont.bold_sm if selected else TextFont.muted_sm)),
            P("See All papers in a combined view", cls=TextFont.muted_sm)),
    )
