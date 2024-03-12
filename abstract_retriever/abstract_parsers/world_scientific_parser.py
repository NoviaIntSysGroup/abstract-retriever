from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser

class WorldScientificParser(AbstractStealthParser):
    URL_PREFIX = "https://www.worldscientific.com/doi/"
    ABSTRACT_SELECTOR = ".abstractInFull p"