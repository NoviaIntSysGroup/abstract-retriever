from abstract_retriever.abstract_parsers.abstract_stealth_parser import AbstractStealthParser
import re

class WileyOnlineLibraryParser(AbstractStealthParser):
    URL_PREFIX = "https://*onlinelibrary.wiley.com/"
    ABSTRACT_SELECTOR = ".article-section__content p"

    @classmethod
    def supports_url(cls, url):
        pattern = re.compile(cls.URL_PREFIX.replace('*', '.*'))
        return bool(pattern.match(url))