from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
from bs4 import BeautifulSoup

class HindawiParser(AbstractParser):
    URL_PREFIX = "https://www.hindawi.com/journals/"
    ABSTRACT_SELECTOR = "h4#abstract"

    def extract_abstract(self, abstract_element):
        return abstract_element.find_next_sibling('p').get_text().strip()
