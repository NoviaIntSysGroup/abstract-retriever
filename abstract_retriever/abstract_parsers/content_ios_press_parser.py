from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
import re
from bs4 import BeautifulSoup

class ContentIosPressParser(AbstractParser):
    URL_PREFIX = "https://content.iospress.com/articles/"
    ABSTRACT_SELECTOR = "header.article-header h1"

    def parse_abstract(self, html_content=None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            abstract_element = soup.select_one(self.ABSTRACT_SELECTOR)
            if abstract_element:
                return abstract_element.get('data-abstract').strip()
            else:
                return None
        except Exception as e:
            return None
