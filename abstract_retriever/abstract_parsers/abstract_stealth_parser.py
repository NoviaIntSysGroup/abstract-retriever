import requests, random, os
from bs4 import BeautifulSoup
from time import sleep
import warnings
from abstract_retriever.abstract_parsers.abstract_parser import AbstractParser

import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth

# Name the subclassess like so
# Filename: example_parser.py
# Class: ExampleParser
class AbstractStealthParser(AbstractParser):
    URL_PREFIX = "https://bad.example.com/"

    async def goto(self, url=None):
        url = url if url is not None else self.url

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

        await page.goto(url)
        return page, browser
    
    async def get(self, url=None, headers=None):
        page, browser = await self.goto(url)
        content = page.content()
        await browser.close()
        return content

        
    def _get_final_url(self, html_content = None):
        response = requests.head(self.url, allow_redirects=True)
        return response.headers.get('Location', self.url)
    
