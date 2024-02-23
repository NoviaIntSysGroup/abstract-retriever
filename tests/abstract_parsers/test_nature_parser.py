import pytest
import abstract_retriever

def test_get_abstract_from_doi():
    doi = "10.1038/s42003-023-05457-y"
    abstract = abstract_retriever.get_abstract_from_doi(doi)
    assert abstract.startswith("High-resolution 3D imaging of species with exoskeletons such as shell-bearing mollusks typically involves destructive steps."), f"abstract is: ({abstract})"

def test_get_abstract_from_url():
    url = "https://www.nature.com/articles/s42003-023-05457-y"

    abstract = abstract_retriever.get_abstract(url)
    assert (str(abstract).startswith("High-resolution 3D imaging of species with exoskeletons such as shell-bearing mollusks typically involves destructive steps.")), f"abstract is: ({abstract})"
