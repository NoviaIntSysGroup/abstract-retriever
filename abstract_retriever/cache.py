import os
import tempfile

LIBRARY_IDENTIFIER = "abstract-retriever"
ABSTRACT_CACHE_FOLDER_NAME = "abstracts"
DEFAULT_CACHE_DIR = os.path.join(tempfile.gettempdir(), LIBRARY_IDENTIFIER)

def create_cache_filepath(doi, cache_dir=DEFAULT_CACHE_DIR):
    return os.path.join(cache_dir, ABSTRACT_CACHE_FOLDER_NAME, doi.replace("/", "_") + ".txt")

def read_cached_abstract(doi, cache_dir=DEFAULT_CACHE_DIR):
    file_path = create_cache_filepath(doi, cache_dir)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    else:
        return None
    
def cache_abstract(doi, abstract, cache_dir=DEFAULT_CACHE_DIR):
    if abstract is None or str(abstract).startswith("No abstract"):
        return False
    
    os.makedirs(os.path.join(cache_dir), exist_ok=True)

    cache_file = create_cache_filepath(doi, cache_dir)
    with open(cache_file, "w") as f:
        f.write(abstract)
    return True
