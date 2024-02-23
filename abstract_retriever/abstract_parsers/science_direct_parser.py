from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class ScienceDirectParser(AbstractParser):
    URL_PREFIX = "https://www.sciencedirect.com/science/article/abs/pii"
    ABSTRACT_SELECTOR = "div.Abstracts div.abstract.author p"