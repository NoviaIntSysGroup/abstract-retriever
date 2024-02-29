from abstract_retriever.abstract_parsers.springer_open_parser import SpringerOpenParser
import re

class BiomedcentralParser(SpringerOpenParser):
    URL_PREFIX = "https://*.biomedcentral.com/articles/"
