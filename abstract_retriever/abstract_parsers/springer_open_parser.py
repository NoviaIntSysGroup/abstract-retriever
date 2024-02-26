from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
import re

class SpringerOpenParser(AbstractParser):
    URL_PREFIX = "https://*.springeropen.com/articles/"
    ABSTRACT_SELECTOR = "#Abs1-content p"

    @classmethod
    def supports_url(cls, url):
        pattern = re.compile(cls.URL_PREFIX.replace('*', '.*'))
        return bool(pattern.match(url))