from saari.common import *
from saari.app import rt

@rt
def create_study(study:Study):
    study.id = uuid4()
    new_study = studies.insert(study)
    return select_study(new_study.id)

@rt
def select_study(study_id:int):
    try:
        study = studies[study_id]
        searches.xtra(study=study_id)
        return RedirectResponse(f'/study/{study_id}', status_code=303)
    except:
        print("Study not foudn")





def get_study(study_id, create_dummy=False):
    try:
        return studies[study_id]
    except:
        if create_dummy:
            if len(studies()) > 0:
                return Study(title="Select Study")
            else:
                return Study(title="No Study Created")
        return None


def study_dropdown(study_id):
    study = get_study(study_id, True)

    
    return Div(
        Button(study.title, UkIcon("chevron-down")),
        DropDownNavContainer(
            *[Li(A(study.title, href=f"/study/{study.id}")) for study in studies()]
        )
    )
    
    return Form(hx_post="/submit", hx_target="#result", hx_trigger="input delay:200ms", cls='space-y-6')(
        Select(
            *[Option(study.title, value=study.id, selected=(study_id==study.id)) for study in studies()],
            name="study_id",
        )
    )



#We are left shifting testing to be able to do virtual commissioning and virtual siea trial byu creating a digital twin of the sihip in order to be able to simulate compoinents that does not yet exist.
def CreateStudyModal():
    return Modal(
        Div(cls='p-6')(
            ModalTitle('Create Study'),
            P('Fill out the information below to create a new study', cls=TextFont.muted_sm),
            Br(),
            Form(action="/create_study", method="post", cls='space-y-6')(
                Input(label='Name', name="title", placeholder='Name of the Litterature review'),
                TextArea(label='Goal', name="goal", placeholder='Describe the overall, research problem you are addressing. AI will rank papers higher that fit this description.'),
                DivRAligned(
                    Button("Send"),
                    ModalCloseButton('Cancel', cls=ButtonT.ghost),
                    ModalCloseButton('Submit', cls=ButtonT.primary),
                    cls='space-x-5',
                )
            ),
        ),
        id='StudyForm',
    )