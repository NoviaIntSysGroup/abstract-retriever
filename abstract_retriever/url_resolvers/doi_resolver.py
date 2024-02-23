from bs4 import BeautifulSoup
import urllib.parse
import requests
from abstract_retriever.url_resolvers.url_resolver import UrlResolver

class DoiResolver(UrlResolver):
    URL_PREFIX = "https://doi.org/"

    def __init__(self, url):
        url = url.replace("https://doi.org/10.48550/arXiv.", "https://arxiv.org/abs/")
        self.url = url
