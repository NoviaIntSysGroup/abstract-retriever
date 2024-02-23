from abstract_retriever.cache import *

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
