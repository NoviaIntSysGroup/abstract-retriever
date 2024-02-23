from bs4 import BeautifulSoup
import urllib.parse
import requests
from abstract_retriever.url_resolvers.url_resolver import UrlResolver

class DoiResolver(UrlResolver):
    URL_PREFIX = "https://doi.org/"
