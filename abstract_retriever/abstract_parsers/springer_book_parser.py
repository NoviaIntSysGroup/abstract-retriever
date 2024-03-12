from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
from bs4 import BeautifulSoup

class SpringerBookParser(AbstractParser):
    URL_PREFIX = "https://link.springer.com/book/"
    ABSTRACT_SELECTOR = ".c-book-section p"
    IS_MULTIPLE = True