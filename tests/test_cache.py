from abstract_retriever.cache import *
from abstract_retriever import get_abstract_from_doi, get_references_from_doi
from abstract_retriever import get_final_doi_url

cache = FileCache("cache-test")


def test_cache_file_is_created_and_has_content(capsys):
    with capsys.disabled():
        doi = "testing/123123123123"
        content = "foo bar baz..."
        key = "test:" + doi

        file_path = CACHE_DIR + "/cache-test/test/testing_123123123123"
        if os.path.exists(file_path):
            os.remove(file_path)

        assert cache.exists(key) == False
        assert not os.path.exists(file_path)

        assert cache.set(key, content)
        assert os.path.exists(file_path)
        assert cache.exists(key) == True
             
        cached_content = cache.get(key)
        assert cached_content == content

def test_get_abstract_from_doi_obeys_cache_flags(capsys):
    with capsys.disabled():
        doi = "10.48550/arXiv.1802.01528"
        key = "doi2abs:" + doi
        file_path = CACHE_DIR + "/cache-test/doi2abs/10.48550_arXiv.1802.01528"
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

        # We start my being sure that there are now such file.
        assert not os.path.exists(file_path)

        assert not cache.exists(key)

        abstract = get_abstract_from_doi(doi, None)
        assert abstract is not None, f"No abstract was fetched when doi cache is False."
        assert not os.path.exists(file_path), f"We should not have created a cache file"

        abstract = get_abstract_from_doi(doi, cache)
        assert abstract is not None, f"No abstract was fetched when doi cache is True."
        assert os.path.exists(file_path), f"We should have created a cache file"

        assert cache.exists(key)


def test_get_references_from_doi():
    references = get_references_from_doi("10.1007/s40948-023-00721-1", cache)
    assert len(references) > 0

    references = get_references_from_doi("10.1007/s00134-012-2769-8", cache)
    assert len(references) > 0

    references = get_references_from_doi("10.1007/s00134-012-2769-8", cache)
    assert len(references) > 1
    


"""
def test_final_doi_url_for_ieee():
    url = get_final_doi_url("10.1109/TASC.2023.3346357", cache)
    assert url == "https://ieeexplore.ieee.org/document/10373057/"

def test_final_doi_url_for_febs():
    url = get_final_doi_url("10.1016/S0014-5793(01)03313-0", cache)
    assert url == "https://febs.onlinelibrary.wiley.com/doi/10.1016/S0014-5793%2801%2903313-0"

def test_final_doi_url_for_science_direct():
    url = get_final_doi_url("10.1016/j.jmst.2023.12.007", cache)
    assert url == "https://www.sciencedirect.com/science/article/abs/pii/S1005030224000446"

def test_final_doi_url_for_nature():
    url = get_final_doi_url("10.1038/s42003-023-05457-y", cache)
    assert url == "https://www.nature.com/articles/s42003-023-05457-y"
"""

#def test_get_abstract_from_doi():
#    doi = "10.1152/physrev.00018.2001"
#    abstract = get_abstract_from_doi(doi, cache)