import pytest
from abstract_retriever import get_final_url

def test_elsevier_hub_linkg_gets_redirected():
    url = "https://linkinghub.elsevier.com/retrieve/pii/S1005030224000446"
    final_url = get_final_url(url)
    expected_url = "https://www.sciencedirect.com/science/article/abs/pii/S1005030224000446"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"

def test_doi_via_elsevier_gets_redirected():
    url = "https://doi.org/10.1016/j.jmst.2023.12.007"
    final_url = get_final_url(url)
    expected_url = "https://www.sciencedirect.com/science/article/abs/pii/S1005030224000446"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"


    