from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
import re
from bs4 import BeautifulSoup

class EbooksIosPressParser(AbstractParser):
    URL_PREFIX = "https://ebooks.iospress.nl/publication/"
    ABSTRACT_SELECTOR = ".abstract p"
