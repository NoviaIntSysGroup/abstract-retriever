from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class MdpiParser(AbstractParser):
    URL_PREFIX = "https://www.mdpi.com/"
    ABSTRACT_SELECTOR = "#html-abstract .html-p"
