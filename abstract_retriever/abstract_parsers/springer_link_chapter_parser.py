from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class SpringerLinkChapterParser(AbstractParser):
    URL_PREFIX = "https://link.springer.com/chapter/"
    ABSTRACT_SELECTOR = "#Abs1-content p"
