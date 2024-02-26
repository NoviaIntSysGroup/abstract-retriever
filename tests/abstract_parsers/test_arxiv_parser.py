import pytest
import abstract_retriever

############################### Change these... ##########################################
#                                          also this            and this
from abstract_retriever.abstract_parsers.arxiv_parser import ArxivParser
example_class = ArxivParser
example_url = "https://arxiv.org/abs/1802.01528"
example_doi = "10.48550/arXiv.1802.01528"
example_abstracts_start = "This paper is an attempt to explain all the matrix calculus you need in order to understand the training of deep neural networks"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__

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

def test_get_abstract_from_url(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract(example_url, verbose=False)
        assert abstract.startswith(example_abstracts_start), f"abstract is: ({abstract})"

def test_get_abstract_from_doi(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract_from_doi(example_doi, cache=False, verbose=False)
        assert abstract is not None, f"get_abstract_from_doi has None as DOI abstract. for {example_doi}"
        assert abstract.startswith(example_abstracts_start), f"get_abstract_from_doi does not get a DOI abstract."
