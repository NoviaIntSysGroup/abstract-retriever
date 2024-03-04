from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class AsmParser(AbstractParser):
    URL_PREFIX = "https://asmedigitalcollection.asme.org/OMAE/"
    ABSTRACT_SELECTOR = "section.abstract p"
