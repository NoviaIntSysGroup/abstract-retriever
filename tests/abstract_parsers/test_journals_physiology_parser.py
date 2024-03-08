import pytest
import abstract_retriever
import requests, os
from abstract_retriever.cache import FileCache

import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth

############################### Change these... ##########################################
#                                          also this            and this
from abstract_retriever.abstract_parsers.journals_physiology_parser import JournalsPhysiologyParser
example_class = JournalsPhysiologyParser
example_url = "https://journals.physiology.org/doi/full/10.1152/physrev.00018.2001"
example_doi = "10.1152/physrev.00018.2001"
example_abstracts_start = "At high concentrations, free radicals and radical-derived,"
##########################################################################################

###
# You can leave these as is..

parser_name = example_class.__name__




@pytest.mark.asyncio
async def test_if_we_get_blocked_with_puppeteer(capsys):
    with capsys.disabled():

        browser = await launch(headless=True)
        page = await browser.newPage()

        # Apply stealth techniques if using pyppeteer_stealth
        # await stealth(page)
        await stealth(page,   run_on_insecure_origins = False,
            languages = ["en-US", "en"],
            vendor = "Google Inc.",
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale = "en-US,en",
            mask_linux = True,
            webgl_vendor = "Intel Inc.",
            renderer = "Intel Iris OpenGL Engine",
            disabled_evasions = []
        )  # <-- Here

        await page.goto(example_url)
        h1_elements = await page.querySelectorAll("h1.citation__title")

        if h1_elements:
            # Get the property as a JSHandle
            title_property = await h1_elements[0].getProperty("textContent")
            # Resolve the JSHandle to get the actual text
            title = await title_property.jsonValue()
        else:
            title = None

        await browser.close()
        print("\nasas")

        print(title)
        print("123123")
        # Adjust the assertion according to what you're actually expecting to find
        assert title is not None, "Expected to find an <h1> element but didn't."


def t_est_if_we_get_blocked(capsys):
    with capsys.disabled():
        import httpx

        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        result = httpx.get(example_url, headers=HEADERS).text
        print(result)
        assert False

pass
cache = FileCache("cache-test")

def t_est_chromedriver_path_is_not_none():
    parser = example_class(example_url, None, True)
    assert parser.chromedriver_path != None

def t_est_request_to_journal_returnts_status_200(capsys):
    with capsys.disabled():

        parser = example_class(example_url, cache, True)
        content = parser.get(example_url)

        assert content is not None, content

def t_est_parser_is_created():
    parser = example_class(example_url)
    assert parser is not None, f"{parser_name} is none"
    assert parser.url == example_url, f"{parser_name} does not have a URL"
    
def t_est_parser_returns_html(capsys):
    with capsys.disabled():
        parser = example_class(example_url, cache, True)
        html_content = parser.fetch_html()
        print(html_content)
        assert html_content is not None, f"{parser_name} does not fetch HTML"

def t_est_that_it_returns_something(capsys):
    with capsys.disabled():
        parser = example_class(example_url, cache, True)
        html_content = parser.fetch_html()
        abstract = parser.get_abstract()
        assert abstract is not None, f"{parser_name} does not get an abstract"

def t_est_get_abstract_from_url(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract(example_url)
        assert abstract.startswith(example_abstracts_start), f"abstract is: ({abstract})"

def t_est_get_abstract_from_doi(capsys):
    with capsys.disabled():
        abstract = abstract_retriever.get_abstract_from_doi(example_doi)
        assert abstract is not None, f"{parser_name} has None as DOI abstract."
        assert abstract.startswith(example_abstracts_start), f"{parser_name} does not get a DOI abstract."
