import os
import tempfile

LIBRARY_IDENTIFIER = "abstract-retriever"
ABSTRACT_CACHE_FOLDER_NAME = "abstracts"
DEFAULT_CACHE_DIR = os.path.join(tempfile.gettempdir(), LIBRARY_IDENTIFIER, ABSTRACT_CACHE_FOLDER_NAME)

def read_cached_abstract(doi, cache_dir=DEFAULT_CACHE_DIR):
    cache_file = os.path.join(cache_dir, "abstracts", doi.replace("/", "_") + ".txt")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read()
    else:
        return None
    
def cache_abstract(doi, abstract, cache_dir=DEFAULT_CACHE_DIR):
    if abstract is None or str(abstract).startswith("No abstract"):
        return False
    
    os.makedirs(os.path.join(cache_dir, "abstracts"), exist_ok=True)

    cache_file = os.path.join(cache_dir, "abstracts", doi.replace("/", "_") + ".txt")
    with open(cache_file, "w") as f:
        f.write(abstract)
    return True
