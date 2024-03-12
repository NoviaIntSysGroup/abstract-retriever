from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class OnePetroParser(AbstractParser):
    URL_PREFIX = "https://onepetro.org/"
    ABSTRACT_SELECTOR = "#ContentTab section.abstract p"