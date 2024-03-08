import pytest
from abstract_retriever import get_final_doi_url, get_references_from_doi, get_all_from_doi
"""

def test_final_doi_url_for_ieee():
    url = get_final_doi_url("10.1109/TASC.2023.3346357")
    assert url == "https://ieeexplore.ieee.org/document/10373057/"

def test_final_doi_url_for_febs():
    url = get_final_doi_url("10.1016/S0014-5793(01)03313-0")
    assert url == "https://febs.onlinelibrary.wiley.com/doi/10.1016/S0014-5793%2801%2903313-0"

def test_final_doi_url_for_science_direct():
    url = get_final_doi_url("10.1016/j.jmst.2023.12.007")
    assert url == "https://www.sciencedirect.com/science/article/abs/pii/S1005030224000446"

def test_final_doi_url_for_nature():
    url = get_final_doi_url("10.1038/s42003-023-05457-y")
    assert url == "https://www.nature.com/articles/s42003-023-05457-y"

def test_get_references_from_doi():
    references = get_references_from_doi("10.1007/s40948-023-00721-1")
    assert len(references) > 0

    references = get_references_from_doi("10.1007/s00134-012-2769-8")
    assert len(references) > 0

    references = get_references_from_doi("10.1007/s00134-012-2769-8")
    assert len(references) > 1
"""
def test_get_all_from_doi():

    data = get_all_from_doi("10.1007/s00134-012-2769-8")
    assert "references" in data and len(data["references"]) > 1

    assert "abstract" in data and data["abstract"] != None

    assert "title" in data and data["title"] != None
