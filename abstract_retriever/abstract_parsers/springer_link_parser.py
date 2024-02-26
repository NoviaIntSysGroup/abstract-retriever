from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class SpringerLinkParser(AbstractParser):
    URL_PREFIX = "https://link.springer.com/article/10.1007/s40948-023-00721-1"
    ABSTRACT_SELECTOR = "#Abs1-content p"
