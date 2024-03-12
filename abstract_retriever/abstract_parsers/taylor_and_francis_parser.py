from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser
from bs4 import BeautifulSoup

class TaylorAndFrancisParser(AbstractStealthParser):
    URL_PREFIX = "https://www.taylorfrancis.com/chapters/edit/"
    ABSTRACT_SELECTOR = "meta[name='citation_abstract']"
    #<meta name="citation_abstract" content="The digitalization of large struct...">

    def extract_abstract(self, abstract_element):
        return abstract_element.get('content').strip()
     