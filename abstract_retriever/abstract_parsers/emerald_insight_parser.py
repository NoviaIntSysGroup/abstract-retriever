from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class EmeraldInsightParser(AbstractParser):
    URL_PREFIX = "https://www.emerald.com/insight/content/doi/"
    ABSTRACT_SELECTOR = ".Abstract__block"
    IS_MULTIPLE = True