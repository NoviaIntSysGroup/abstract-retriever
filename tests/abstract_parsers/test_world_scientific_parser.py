import pytest
import abstract_retriever
from abstract_retriever.cache import FileCache

############################### Change these... ##########################################
#                                               also this                   and this
from abstract_retriever.abstract_parsers.world_scientific_parser import WorldScientificParser
example_class = WorldScientificParser
example_url = "https://www.worldscientific.com/doi/abs/10.1142/S2424862219500167"
example_doi = "10.1142/S2424862219500167"
example_abstracts_start = "Industrial information integration engineering (IIIE) is a set"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__
cache = FileCache("world-scientific-test")

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
        assert abstract is not None, f"{parser_name} does not get an abstract"

def test_get_abstract_from_url():
    abstract = abstract_retriever.get_abstract(example_url)
    assert abstract.startswith(example_abstracts_start), f"abstract is: ({abstract})"

def test_get_abstract_from_doi():
    abstract = abstract_retriever.get_abstract_from_doi(example_doi)
    assert abstract is not None, f"{parser_name} has None as DOI abstract."
    assert abstract.startswith(example_abstracts_start), f"{parser_name} does not get a DOI abstract."
