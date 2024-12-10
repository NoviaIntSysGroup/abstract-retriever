from saari.common import *
from saari.app import rt

@dataclass
class Login: name:str; pwd:str




##ROUTES

login_redir = RedirectResponse('/login', status_code=303)

@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    try: u = users[login.name]
    except NotFoundError: u = users.insert(login)
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    sess['auth'] = u.name
    if "study" in sess:
        del sess['study']
    return RedirectResponse('/', status_code=303)


@rt
def login():
    frm = Form(action='/login', method='post')(
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'))
    return Titled("Login", frm)

@rt("/logout")
def logout(sess):
    del sess['auth']
    del sess['study']

    return login_redir
