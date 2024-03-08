from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
from bs4 import BeautifulSoup
from urllib.parse import unquote

class SpringerGenericParser(AbstractParser):
    URL_PREFIX = "xxx"
    ABSTRACT_SELECTOR = "#Abs1-content p"
   
    def get_abstract(self):
        html_content = self.fetch_html()
        if html_content:
            return self.parse_abstract(html_content)
        else:
            return None
        

    def get_references(self, html_content = None):
        if not html_content:
            html_content = self.fetch_html()
        if not html_content:
            return []
        
        return self.extract_doi_ids(html_content)
        
    def extract_doi_ids(self, html_content):
        dois = set()
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.select('a[data-track-action="article reference"]')

        for link in links:
            href = link.get('href')
            if href and href.startswith("https://doi.org/"):
                doi = href.split('https://doi.org/')[-1]
                dois.add(unquote(doi))
        return list(dois)