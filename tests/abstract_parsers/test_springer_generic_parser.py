import pytest
import abstract_retriever

############################### Change these... ##########################################
#                                               also this                   and this
from abstract_retriever.abstract_parsers.springer_link_parser import SpringerLinkParser
example_class = SpringerLinkParser
example_url = "https://link.springer.com/article/10.1007/s40948-023-00721-1"
example_doi = "10.1007/s40948-023-00721-1"
example_abstracts_start = "A semi-analytical and a finite-difference scheme are presented"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__
"""
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
        parser = example_class(example_url)
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
"""
def test_get_references_returns_something(capsys):
    with capsys.disabled():
        parser = example_class(example_url, verbose=True)
        references = parser.get_references()
        assert references is not None, "references should not be None"
        assert isinstance(references, list), "references should be a list"
        assert len(references) > 0, "references should not be empty"
