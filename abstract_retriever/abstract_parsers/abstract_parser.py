import requests, random, os
from bs4 import BeautifulSoup
from time import sleep
import warnings

# Name the subclassess like so
# Filename: example_parser.py
# Class: ExampleParser
class AbstractParser:
    URL_PREFIX = "https://example.com/"
    ABSTRACT_SELECTOR = "p.abstract"
    TITLE_SELECTOR = "h1"
    REFERENCES_SELECTOR = "#preview-section-references ul li.bib-reference"
    IS_MULTIPLE = False

    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        #"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
        #"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
        #"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edge/18.19582"
    ]
    chromedriver_path = None

    def __init__(self, url, cache=None, verbose=False):
        self.verbose = verbose
        self.url = url
        self.cache = cache

        self.chromedriver_path = os.getenv('CHROMEDRIVER_PATH')  # Get driver path from environment variable



    @classmethod
    def supports_url(cls, url):
        return url.startswith(cls.URL_PREFIX)

    def get_canonical(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            canonical_element = soup.select_one('link[rel="canonical"]')
            return canonical_element.get('href').strip()
        
        except Exception as e:
            return self.url

    def d(self, message):
        if self.verbose:
            print("\n")
            print(message)
            print("\n")

    def get(self, url=None, headers=None):
        url = url if url is not None else self.url
        if headers is None:
            headers = {
                'User-Agent': random.choice(self.USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                #'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
        try:
            self.d(f"Sending request to {url}")
            response = requests.get(url, headers=headers, allow_redirects=True)
            response.raise_for_status()  # Raise an error for non-2xx status codes
            return response.text
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                print("permission denied")
            else:
                self.d(f"error is {e.response.status_code}")
                self.d(e.response.text)
                return None  # Re-raise other HTTP errors

    def fetch_html(self):
        try:
            key = "url2html:" + self.url
            if self.cache and self.cache.exists(key):
                return self.cache.get(key)
            
            key2 = "url2http:" + self.url
            self.d(f"getting stuff... {self.url}");
            html_content = self.get(self.url)

            if self.cache:
                self.cache.set(key, html_content)

            return html_content

        except Exception as e:
            self.d(e)
            return None

    def get_abstract(self):
        html_content = self.fetch_html()
        if html_content:
            return self.parse_abstract(html_content)
        else:
            return None

    def extract_abstract(self, abstract_element):
        return abstract_element.get_text().strip()

    def parse_abstract(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            if self.IS_MULTIPLE:
                abstract_texts = []
                for abstract_element in soup.select(self.ABSTRACT_SELECTOR):
                    abstract_texts.append(self.extract_abstract(abstract_element))
                return ". ".join(abstract_texts)
            else:
                abstract_element = soup.select_one(self.ABSTRACT_SELECTOR)
                return self.extract_abstract(abstract_element)
        except Exception as e:
            return None

    def _get_final_url(self, html_content = None):
        response = requests.head(self.url, allow_redirects=True)
        return response.headers.get('Location', self.url)
    
    def get_references(self, html_content = None):
        return []
    
    def get_title(self):
        html_content = self.fetch_html()
        if html_content:
            return self.parse_title(html_content)
        else:
            return None


    def parse_title(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_element = soup.select_one(self.TITLE_SELECTOR)
            if title_element:
                return title_element.get_text().strip()
            else:
                return None
        except Exception as e:
            return None

    def get_all(self):
        html_content = self.fetch_html()
        abstract = self.parse_abstract(html_content)
        references = self.get_references(html_content)
        title = self.parse_title(html_content)

        return {
            "url": self.url,
            "title": title,
            "abstract": abstract,
            "references": references
        }
