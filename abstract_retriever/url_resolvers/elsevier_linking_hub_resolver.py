import requests
from bs4 import BeautifulSoup
import urllib.parse

from abstract_retriever.url_resolvers.url_resolver import UrlResolver

class ElsevierLinkingHubResolver(UrlResolver):
    URL_PREFIX = "https://linkinghub.elsevier.com/retrieve/pii/"

    def _fetch_html(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            return None      

    def get_final_url(self):

        html_content = self._fetch_html()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the <meta> tag with http-equiv="REFRESH"
        meta_refresh_tag = soup.find('meta', attrs={'http-equiv': 'REFRESH'})
        if meta_refresh_tag:
            # Extract the content attribute, which contains the redirect URL
            content = meta_refresh_tag.get('content')
            if content:
                # Parse the Redirect parameter and URL decode it
                redirect_url = content.split('Redirect=')[1].strip("'")
                redirect_url_decoded = urllib.parse.unquote(redirect_url)
                redirect_url_decoded = redirect_url_decoded.split('?')[0]
                return redirect_url_decoded.replace("/article/pii/", "/article/abs/pii/")
