import importlib.util
import os, urllib, requests
from .cache import read_cached_abstract, cache_abstract

def load_resolvers():
    # Dynamically load all resolver modules in the url_resolvers package
    resolver_modules = []
    folder = os.path.join(os.path.dirname(__file__), "url_resolvers")
    for filename in os.listdir(folder):
        if filename.endswith("_resolver.py"):
            spec = importlib.util.spec_from_file_location(
                filename[:-3], os.path.join(folder, filename)
            )
            resolver_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(resolver_module)
            resolver_modules.append(resolver_module)
    return resolver_modules

RESOLVERS = load_resolvers()

def get_final_url(url):
    for resolver_module in RESOLVERS:
        resolver_class_name = ''.join(word.capitalize() for word in resolver_module.__name__.split('_')[:-1]) + "Resolver"
        resolver_class = getattr(resolver_module, resolver_class_name)
        if resolver_class and resolver_class.supports_url(url):
            resolver = resolver_class(url)
            final_url = resolver.get_final_url()
            # Handle multiple redoirections of different kinds.
            # such as doi -> elsevier hub -> sciencedirect
            if (final_url != url):
                return get_final_url(final_url)
    return url

def load_parsers():
    # Dynamically load all parser modules in the abstract_parsers package
    parser_modules = []
    folder = os.path.join(os.path.dirname(__file__), "abstract_parsers")
    for filename in os.listdir(folder):
        if filename.endswith("_parser.py"):
            spec = importlib.util.spec_from_file_location(
                filename[:-3], os.path.join(folder, filename)
            )
            parser_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(parser_module)
            parser_modules.append(parser_module)
    return parser_modules

PARSERS = load_parsers()

def get_abstract(url, verbose=False):
    url = get_final_url(url)
    for parser_module in PARSERS:
        parser_class_name = ''.join(word.capitalize() for word in parser_module.__name__.split('_')[:-1]) + "Parser"

        parser_class = getattr(parser_module, parser_class_name)
        if parser_class and parser_class.supports_url(url):
            parser = parser_class(url, verbose)
            return parser.get_abstract()
    raise ValueError("No parser available for the provided URL")

def get_abstract_from_doi(doi, cache=False, verbose=False):
    if cache:
        abstract = read_cached_abstract(doi)
        if abstract:
            return abstract
    
    safedoi = urllib.parse.quote(doi, safe="/").replace("%2F", "/")
    url = f"https://doi.org/{safedoi}"

    abstract = get_abstract(url, verbose=verbose)
    if cache:
        cache_abstract(doi, abstract)
    return abstract
