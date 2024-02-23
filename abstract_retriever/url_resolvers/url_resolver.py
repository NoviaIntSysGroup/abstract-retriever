import requests
from bs4 import BeautifulSoup

# Name the subclassess like so
# Filename: example_reolver.py
# Class: ExampleResolver
class UrlResolver:
    URL_PREFIX = "https://example.com/"

    def __init__(self, url):
        self.url = url

    @classmethod
    def supports_url(cls, url):
        return url.startswith(cls.URL_PREFIX)

    def get_final_url(self, html_content = None):
        response = requests.head(self.url, allow_redirects=True)
        return response.url
    