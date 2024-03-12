import requests
from bs4 import BeautifulSoup
from abstract_retriever.url_resolvers.url_resolver import UrlResolver

# Name the subclassess like so
# Filename: example_reolver.py
# Class: ExampleResolver
class MedraAliasResolver(UrlResolver):
    URL_PREFIX = "https://www.medra.org/servlet/aliasResolver"

    def get_final_url(self, html_content=None):
        print("Finding " + self.url)
        response = requests.get(self.url, allow_redirects=True)
        if response.url != self.url:
            self.url = response.url
            return self.get_final_url().replace(":443" ,"")
        else:
            print("URLs are the same: " + self.url)
        return response.url
    