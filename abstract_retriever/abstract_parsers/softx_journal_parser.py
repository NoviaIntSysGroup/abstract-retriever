from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class SoftxJournalParser(AbstractParser):
    URL_PREFIX = "https://www.softxjournal.com/article/"
    ABSTRACT_SELECTOR = ".article__body .article__sections .section-paragraph .section-paragraph"
