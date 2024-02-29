import pytest
import abstract_retriever
import requests, os
from abstract_retriever.cache import FileCache

############################### Change these... ##########################################
#                                          also this            and this
from abstract_retriever.abstract_parsers.journals_physiology_parser import JournalsPhysiologyParser
example_class = JournalsPhysiologyParser
example_url = "https://journals.physiology.org/doi/full/10.1152/physrev.00018.2001"
example_doi = "10.1152/physrev.00018.2001"
example_abstracts_start = "At high concentrations, free radicals and radical-derived,"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__

cache = FileCache("cache-test")

def t_est_chromedriver_path_is_not_none():
    parser = example_class(example_url, None, True)
    assert parser.chromedriver_path != None

def t_est_request_to_journal_returnts_status_200(capsys):
    with capsys.disabled():

        parser = example_class(example_url, cache, True)
        content = parser.get(example_url)

        assert content is not None, content

def t_est_parser_is_created():
    parser = example_class(example_url)
    assert parser is not None, f"{parser_name} is none"
    assert parser.url == example_url, f"{parser_name} does not have a URL"
    
def t_est_parser_returns_html(capsys):
    with capsys.disabled():
        parser = example_class(example_url, cache, True)
        html_content = parser.fetch_html()
        print(html_content)
        assert html_content is not None, f"{parser_name} does not fetch HTML"

def t_est_that_it_returns_something(capsys):
    with capsys.disabled():
        parser = example_class(example_url, cache, True)
        html_content = parser.fetch_html()
        abstract = parser.get_abstract()
        assert abstract is not None, f"{parser_name} does not get an abstract"

def t_est_get_abstract_from_url(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract(example_url)
        assert abstract.startswith(example_abstracts_start), f"abstract is: ({abstract})"

def t_est_get_abstract_from_doi(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract_from_doi(example_doi)
        assert abstract is not None, f"{parser_name} has None as DOI abstract."
        assert abstract.startswith(example_abstracts_start), f"{parser_name} does not get a DOI abstract."
