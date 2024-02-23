from abstract_retriever.cache import *
from abstract_retriever import get_abstract_from_doi

def test_cache_filename_is_created():
    path = create_cache_filepath("fooo/bar", "baz")
    assert path == "baz/abstracts/fooo_bar.txt"

def test_cache_file_is_created_and_has_content(capsys):
    with capsys.disabled():
        doi = "testing/123123123123"
        content = "foo bar baz..."
        file_path = create_cache_filepath(doi)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        assert not os.path.exists(file_path)
        cache_abstract(doi, content)
        assert os.path.exists(file_path) == True
        cached_content = read_cached_abstract(doi)
        assert cached_content == content

def test_get_abstract_from_doi_obeys_cache_flags(capsys):
    with capsys.disabled():
        doi = "10.48550/arXiv.1802.01528"
        file_path = create_cache_filepath(doi)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        # We start my being sure that there are now such file.
        assert not os.path.exists(file_path)

        abstract = get_abstract_from_doi(doi, cache=False)
        assert abstract is not None, f"No abstract was fetched when doi cache is False."
        assert not os.path.exists(file_path), f"We should not have created a cache file"

        abstract = get_abstract_from_doi(doi, cache=True)
        assert abstract is not None, f"No abstract was fetched when doi cache is True."
        assert os.path.exists(file_path), f"We should have created a cache file"

        cache_abstract(doi, "Fooo")
        abstract = get_abstract_from_doi(doi, cache=True)
        assert abstract == "Fooo"

