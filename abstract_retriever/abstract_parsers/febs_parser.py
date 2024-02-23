from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class FebsParser(AbstractParser):
    URL_PREFIX = "https://febs.onlinelibrary.wiley.com/doi/"
    ABSTRACT_SELECTOR = ".article__body . metis-abstract .article-section__content.main p"
