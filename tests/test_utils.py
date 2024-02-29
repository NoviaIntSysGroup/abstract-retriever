import pytest
from abstract_retriever import get_final_doi_url

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
