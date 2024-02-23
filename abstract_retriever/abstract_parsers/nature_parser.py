from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class NatureParser(AbstractParser):
    URL_PREFIX = "https://www.nature.com/articles/"
    ABSTRACT_SELECTOR = "div.c-article-section__content#Abs1-content p"