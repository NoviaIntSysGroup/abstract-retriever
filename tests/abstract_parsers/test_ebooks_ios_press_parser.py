import pytest
import abstract_retriever
from abstract_retriever.cache import FileCache
############################### Change these... ##########################################
#                                               also this                   and this
from abstract_retriever.abstract_parsers.ebooks_ios_press_parser import EbooksIosPressParser
example_class = EbooksIosPressParser
example_url = "https://ebooks.iospress.nl/publication/49529"
example_doi = "10.3233/978-1-61499-864-8-391"
example_abstracts_start = "Concern for the structural longevity of ship, offshore and"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__
cache = FileCache("cache-test3")

def test_parser_is_created():
    parser = example_class(example_url)
    assert parser is not None, f"{parser_name} is none"
    assert parser.url == example_url, f"{parser_name} does not have a URL"
    
def test_parser_returns_html(capsys):
    with capsys.disabled():
        parser = example_class(example_url)
        html_content = parser.fetch_html()
        assert html_content is not None, f"{parser_name} does not fetch HTML"

def test_that_it_returns_something(capsys):
    with capsys.disabled():
        parser = example_class(example_url, None, True)
        html_content = parser.fetch_html()
        abstract = parser.get_abstract()
        print(abstract)

        assert abstract is not None, f"{parser_name} does not get an abstract"

def test_get_abstract_from_url():
    abstract = abstract_retriever.get_abstract(example_url)
    assert abstract.startswith(example_abstracts_start), f"abstract is: ({abstract})"

def test_get_abstract_from_doi():
    abstract = abstract_retriever.get_abstract_from_doi(example_doi, cache=cache, verbose=True)
    assert abstract is not None, f"{parser_name} has None as DOI abstract."
    assert abstract.startswith(example_abstracts_start), f"{parser_name} does not get a DOI abstract."
