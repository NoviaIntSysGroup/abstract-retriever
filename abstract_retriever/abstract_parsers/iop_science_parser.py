from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser

class IopScienceParser(AbstractStealthParser):
    URL_PREFIX = "https://iopscience.iop.org/article/"
    ABSTRACT_SELECTOR = ".article-text.wd-jnl-art-abstrac p"