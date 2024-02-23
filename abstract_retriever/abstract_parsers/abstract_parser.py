import requests
from bs4 import BeautifulSoup

# Name the subclassess like so
# Filename: example_parser.py
# Class: ExampleParser
class AbstractParser:
    URL_PREFIX = "https://example.com/"
    ABSTRACT_SELECTOR = "p.abstract"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    def __init__(self, url, verbose=False):
        self.verbose = verbose
        self.url = url

    @classmethod
    def supports_url(cls, url):
        return url.startswith(cls.URL_PREFIX)

    def d(self, message):
        if self.verbose:
            print(message)

    def fetch_html(self):
        try:
            response = requests.get(self.url, headers=self.HEADERS, allow_redirects=True)
            self.d(f"Status code: {response.status_code}")
            if response.status_code == 403:
                self.d(f"It seems we are not allowed to fetch {self.url}")
                self.d(response)
                return None
            if response.status_code == 200 or response.status_code == 418:
                return response.text
            else:
                self.d(f"No content it seems..., but status code is {response.status_code}")
                return None
        except Exception as e:
            self.d(e)
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