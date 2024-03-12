import pytest
from abstract_retriever import get_final_url

def test_medra_redirected(capsys):
    with capsys.disabled():
        url = "https://www.medra.org/servlet/aliasResolver?alias=iospress&doi=10.3233/JIFS-201885"
        final_url = get_final_url(url)
        expected_url = "https://content.iospress.com/articles/journal-of-intelligent-and-fuzzy-systems/ifs201885"

        assert final_url == expected_url, f"{final_url} is not {expected_url}"

def test_medra_doi_redirected():
    url = "https://doi.org/10.3233/JIFS-201885"
    final_url = get_final_url(url)
    expected_url = "https://content.iospress.com/articles/journal-of-intelligent-and-fuzzy-systems/ifs201885"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"

def test_medra_redirected2():
    url = "https://www.medra.org/servlet/aliasResolver?alias=iospressISBN&isbn=978-1-61499-863-1&spage=391&doi=10.3233/978-1-61499-864-8-391"
    final_url = get_final_url(url)
    expected_url = "https://ebooks.iospress.nl/publication/49529"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"

def test_medra_doi_redirected2():
    url = "https://doi.org/10.3233/978-1-61499-864-8-391"
    final_url = get_final_url(url)
    expected_url = "https://ebooks.iospress.nl/publication/49529"

    assert final_url == expected_url, f"{final_url} is not {expected_url}"
