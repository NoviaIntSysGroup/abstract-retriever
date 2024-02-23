from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser
import re
import json

class IeeeParser(AbstractParser):
    URL_PREFIX = "https://ieeexplore.ieee.org/document/"
    ABSTRACT_SELECTOR = "div.abstract-desktop-div div.abstract-text > div > div > div"

    def parse_abstract(self, html_content=None):
        try:
            match = re.search(r'xplGlobal\.document\.metadata\s*=\s*({.*?});', html_content, re.DOTALL)
            if match:
                metadata_str = match.group(1)
                metadata_obj = json.loads(metadata_str);
                return metadata_obj["abstract"]
            else:
                return None
        except:
            return None