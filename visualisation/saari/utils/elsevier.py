import urllib.parse
import requests
import os
import json


from dotenv import load_dotenv  # for loading environment variables from a .env file
load_dotenv()  # load environment variables from .env file


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pydantic import BaseModel
from ..db import Paper
from .paper import client

def combine_scopus_data(entry_data, parsed_data):
    combined_data = Paper(
        id=int(entry_data['dc:identifier'].split(':')[-1]),
        title=entry_data.get('dc:title', ''),
        doi=entry_data.get('prism:doi', ''),
        abstract=parsed_data.get('abstract', ''),
        year=entry_data.get('prism:coverDate', '').split('-')[0],
        authors='; '.join(parsed_data.get('authors', [])),
        publication=entry_data.get('prism:publicationName', ''),
        issn=entry_data.get('prism:issn', ''),
        volume=entry_data.get('prism:volume', ''),
        issue=entry_data.get('prism:issueIdentifier', ''),
        page_range=entry_data.get('prism:pageRange', ''),
        cover_date=entry_data.get('prism:coverDate', ''),
        cited_by_count=int(entry_data.get('citedby-count', 0)),
        affiliation_name=entry_data['affiliation'][0].get('affilname', '') if entry_data.get('affiliation') else '',
        affiliation_city=entry_data['affiliation'][0].get('affiliation-city', '') if entry_data.get('affiliation') else '',
        affiliation_country=entry_data['affiliation'][0].get('affiliation-country', '') if entry_data.get('affiliation') else '',
        indexed_keywords='; '.join(parsed_data.get('indexed_keywords', [])),
        author_keywords=parsed_data.get('author_keywords', ''),
        open_access=entry_data.get('openaccessFlag', False),
        subtype=entry_data.get('subtype', ''),
        subtype_description=entry_data.get('subtypeDescription', '')
    )

    return combined_data

def parse_scopus_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_section = soup.find('span', id='noSourceTitleLink')
    title = title_section.text.strip() if title_section else 'Title not found'
    
    # Extract abstract
    abstract_section = soup.find('section', id='abstractSection')
    abstract = abstract_section.find('p').text.strip() if abstract_section else 'Abstract not found'
    
    # Extract author keywords (if available)
    author_keywords_section = soup.find('section', id='authorKeywords')
    author_keywords = [kw.text.strip() for kw in author_keywords_section.find_all('span', class_='badges')] if author_keywords_section else 'Author keywords not found'
    
    # Extract indexed keywords (if available)
    indexed_keywords_section = soup.find('section', id='indexedKeywords')
    indexed_keywords = [kw.text.strip() for kw in indexed_keywords_section.find_all('span', class_='badges')] if indexed_keywords_section else 'Indexed keywords not found'
    
    # Extract authors
    author_section = soup.find('section', id='authorlist')
    authors = [author.text.strip() for author in author_section.find_all('span', class_='previewTxt')] if author_section else 'Authors not found'
    
    return {
        'title': title,
        'abstract': abstract,
        'author_keywords': author_keywords,
        'indexed_keywords': indexed_keywords,
        'authors': authors
    }

# Example usage
#parsed_data = parse_scopus_html(html_content)
#print(parsed_data)


def load_scopus_urls_html(urls):
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Add a user-agent string
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Initialize the WebDriver once
    driver = webdriver.Chrome(options=chrome_options)

    results = []
    try:
        for url in urls:
            try:
                # Load the URL
                driver.get(url)

                # Wait for the page to load completely
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Handle potential JavaScript redirects
                #current_url = driver.current_url
                #WebDriverWait(driver, 10).until(
                #    lambda driver: driver.current_url != current_url
                #)

                # Get the page source
                results.append(driver.page_source)
            except Exception as e:
                print("Error loading URL:", url, "Error:", e)
                results.append(None)
    finally:
        # Close the WebDriver
        driver.quit()

    return results


def load_scopus_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print("Error:", response.status_code)
        return None    


def search_elsevier_api(query, api_key, max_results=1,start=0):
    end = start + max_results
    key = "search-" + str(max_results) + ":" + query + f"--items({start}-{end})"

    q = urllib.parse.quote(query)

    # Check parameters at https://dev.elsevier.com/guides/Scopus%20API%20Guide_V1_20230907.pdf from page 47 onwards
    url = f"https://api.elsevier.com/content/search/scopus?query={q}&apiKey={api_key}&count={max_results}&sort=citedby-count&start={start}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        search_results = response.json()
        if "entry" in search_results["search-results"]:
            return search_results["search-results"]["entry"]
        return None
    else:
        print("Error:", response.status_code)
        print(response.json())
        return None

def search_for_papers(query, api_key, max_results=10):
    cursor = 0
    page_size = 10
    all_results = []
    while cursor < max_results:
        search_results = search_elsevier_api(query, api_key, page_size, cursor)
        if search_results is None:
            break
        cursor = cursor + page_size
        all_results = all_results + search_results



class ScopusSearch(BaseModel):
    title: str
    query: str
    goal: str

# Use a relative path to open 'search_guide.md'
with open(os.path.join(os.path.dirname(__file__), 'search_guide_small.md'), 'r') as file:
    scopus_search_manual_md = file.read()

def transform_to_scopus_query(description: str) -> tuple[str, str]:
    scopus_instructions = """
    Generate a SCOPUS query that searches for topics in the shipbuilding industry,
    specifically digital commissioning. The query should include relevant keywords,
    phrases, and logical operators to refine the search. Provide a meaningful title for the search, but no need to tell it that it is a Scopus search for X, just name it X.
    You will also return a goal, that text is used to sort theretrieved papers (on title and abstract using promximity search and ai rerankers),
    so we will suggest a 'goal' text that helps us get the most relevant papers first.
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Follow the instructions: {scopus_instructions + scopus_search_manual_md}"},
            {"role": "user", "content": description},
        ],
        response_format=ScopusSearch,
    )
    
    parsed_result = completion.choices[0].message.parsed
    return parsed_result.title, parsed_result.query, parsed_result.goal