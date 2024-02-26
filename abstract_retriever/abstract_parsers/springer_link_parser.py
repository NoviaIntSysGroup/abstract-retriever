from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class SpringerLinkParser(AbstractParser):
    URL_PREFIX = "https://link.springer.com/article/"
    ABSTRACT_SELECTOR = "#Abs1-content p"
