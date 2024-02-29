from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class JournalsPhysiologyParser(AbstractParser):
    URL_PREFIX = "https://journals_____lets skip this____.physiology.org/doi/"
    ABSTRACT_SELECTOR = ".abstractSection.abstractInFull p"
