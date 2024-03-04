from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class KnsCnkiParser(AbstractParser):
    URL_PREFIX = "http://kns.cnki.net/kcms/detail/detail.aspx?doi="
    ABSTRACT_SELECTOR = "span.abstract-text"
