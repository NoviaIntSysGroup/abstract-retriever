from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
from bs4 import BeautifulSoup

class FrontiersInEnergyParser(AbstractParser):
    URL_PREFIX = "https://www.frontiersin.org/articles/"
    ABSTRACT_SELECTOR = ".JournalAbstract p.mb15"

    def parse_abstract(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            abstract_texts = []
            for abstract_element in soup.select(self.ABSTRACT_SELECTOR):
                abstract_texts.append(self.extract_abstract(abstract_element))
            return ". ".join(abstract_texts)
        except Exception as e:
            return None