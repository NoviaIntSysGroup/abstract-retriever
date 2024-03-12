from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class AcmDigitalLibraryParser(AbstractParser):
    URL_PREFIX = "https://dl.acm.org/doi/"
    ABSTRACT_SELECTOR = ".article__abstract > .abstractInFull > .abstractInFull p"