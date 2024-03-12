from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser

class SageJournalsParser(AbstractStealthParser):
    URL_PREFIX = "https://journals.sagepub.com/doi/"
    ABSTRACT_SELECTOR = "#abstract div[role='paragraph']"