import requests
from bs4 import BeautifulSoup
from abstract_retriever.url_resolvers.url_resolver import UrlResolver
from abstract_retriever.abstract_parsers.aip_publishing_parser import AipPublishingParser

# Name the subclassess like so
# Filename: example_reolver.py
# Class: ExampleResolver
class AipPublishingResolver(UrlResolver):
    URL_PREFIX = "http://aip.scitation.org/doi/abs/"

    def get_final_url(self, html_content=None):
        print("Finding " + self.url)
        parser = AipPublishingParser(self.url)
        url = parser.get_canonical()
        print(f"The chosen url is {url}")
        return url
    