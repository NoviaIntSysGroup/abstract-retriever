from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class IntJournalOfMaritimeEngineeringParser(AbstractParser):
    URL_PREFIX = "https://www.intmaritimeengineering.org/"
    ABSTRACT_SELECTOR = "#summary .article-abstract p"