from fasthtml.common import *
from fasthtml.svg import *
import saari
from saari.db import *
from fh_frankenui.core import *


def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth or auth not in users:
        return saari.components.login.login_redir
    studies.xtra(user=auth)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', '/login'])
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))

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
    before=bware,
    exception_handlers={404: _not_found},
    hdrs=hdrs  # Use frankenui theme headers
)
rt = app.route