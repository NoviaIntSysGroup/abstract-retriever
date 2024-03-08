from abstract_retriever.abstract_parsers.springer_generic_parser import SpringerGenericParser
import re

class SpringerOpenParser(SpringerGenericParser):
    URL_PREFIX = "https://*.springeropen.com/articles/"

    @classmethod
    def supports_url(cls, url):
        pattern = re.compile(cls.URL_PREFIX.replace('*', '.*'))
        return bool(pattern.match(url))