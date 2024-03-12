import requests
from bs4 import BeautifulSoup
from abstract_retriever.url_resolvers.url_resolver import UrlResolver
from abstract_retriever.abstract_parsers.taylor_and_francis_parser import TaylorAndFrancisParser

# Name the subclassess like so
# Filename: example_reolver.py
# Class: ExampleResolver
class TaylorFrancisResolver(UrlResolver):
    URL_PREFIX = "https://www.taylorfrancis.com/books/9781003216582/chapters/"

    def get_final_url(self, html_content=None):
        print("Finding " + self.url)
        parser = TaylorAndFrancisParser(self.url)
        url = parser.get_canonical()
        print(f"The chosen url is {url}")
        return url
    