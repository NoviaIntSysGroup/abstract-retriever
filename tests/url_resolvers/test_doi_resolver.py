import pytest
from abstract_retriever import get_final_url

def test_it_gets_redirected():
    url = "https://doi.org/10.1038/s42003-023-05457-y"
    final_url = get_final_url(url)
    expected_url = "https://www.nature.com/articles/s42003-023-05457-y"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"
