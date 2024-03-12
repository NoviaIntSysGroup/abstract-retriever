from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser

class TaylorAndFrancisOnlineParser(AbstractStealthParser):
    URL_PREFIX = "https://www.tandfonline.com/doi/"
    ABSTRACT_SELECTOR = "article .hlFld-Abstract p"