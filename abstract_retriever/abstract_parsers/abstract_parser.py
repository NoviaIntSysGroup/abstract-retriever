import requests
from bs4 import BeautifulSoup

# Name the subclassess like so
# Filename: example_parser.py
# Class: ExampleParser
class AbstractParser:
    URL_PREFIX = "https://example.com/"
    ABSTRACT_SELECTOR = "p.abstract"

    def __init__(self, url):
        self.url = url

    @classmethod
    def supports_url(cls, url):
        return url.startswith(cls.URL_PREFIX)

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            return None

    def get_abstract(self):
        html_content = self.fetch_html()
        if html_content:
            return self.parse_abstract(html_content)
        else:
            return None


    def parse_abstract(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            abstract_element = soup.select_one(self.ABSTRACT_SELECTOR)
            if abstract_element:
                return abstract_element.get_text().strip()
            else:
                return None
        except Exception as e:
            return None
        
    def _get_final_url(self, html_content = None):
        response = requests.head(self.url, allow_redirects=True)
        return response.headers.get('Location', self.url)