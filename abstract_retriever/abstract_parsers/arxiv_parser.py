from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class ArxivParser(AbstractParser):
    URL_PREFIX = "https://arxiv.org/abs/"
    ABSTRACT_SELECTOR = "blockquote.abstract"

    def get_abstract(self):
        html_content = self.fetch_html()
        self.d(self.url)
        if html_content:
            return self.parse_abstract(html_content)
        else:
            return None
        
    def get_abstract(self):
        html_content = self.fetch_html()
        if html_content:
            return self.parse_abstract(html_content).replace("Abstract:", "")
        else:
            return None
