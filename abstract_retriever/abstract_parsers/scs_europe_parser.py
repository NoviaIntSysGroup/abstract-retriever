from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
from bs4 import BeautifulSoup

class ScsEuropeParser(AbstractParser):
    URL_PREFIX = "https://www.scs-europe.net/dlib"
    ABSTRACT_SELECTOR = "td p"


    def parse_abstract(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all paragraphs
            paragraphs = soup.find_all('p')

            # Initialize abstract text
            abstract_text = ""
            found = False
            # Loop through paragraphs to find the one containing Abstract:
            for p in paragraphs:
                if found:
                   abstract_text = p.get_text()
                   return abstract_text
                 
                if "Abstract:" in p.get_text():
                    found = True # the next p is our target.                 

            else:
                return None
        except Exception as e:
            return None