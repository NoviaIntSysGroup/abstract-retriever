from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

class IgiGlobalParser(AbstractParser):
    URL_PREFIX = "https://www.igi-global.com/gateway/chapter/"
    ABSTRACT_SELECTOR = "#ctl00_ctl00_cphMain_cphSection_lblAbstract"

    def extract_abstract(self, abstract_element):
        return abstract_element.get_text().strip().replace("Abstract", "")