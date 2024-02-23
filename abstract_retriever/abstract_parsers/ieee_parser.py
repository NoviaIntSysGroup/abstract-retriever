from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class IeeeParser(AbstractParser):
    URL_PREFIX = "https://ieeexplore.ieee.org/document/"
    ABSTRACT_SELECTOR = "p.abstract"
