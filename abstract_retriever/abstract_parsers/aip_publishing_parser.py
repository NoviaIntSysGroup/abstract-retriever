from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser

class AipPublishingParser(AbstractStealthParser):
    URL_PREFIX = "https://pubs.aip.org/"
    ABSTRACT_SELECTOR = "section.abstract p"