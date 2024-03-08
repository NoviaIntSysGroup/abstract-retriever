import gradio as gr

import requests
import os
import json

from abstract_retriever import get_abstract_from_doi, get_final_doi_url, get_references_from_doi, get_all_from_doi
from abstract_retriever.cache import FileCache
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELSEVIER_API_KEY = os.getenv('ELSEVIER_API_KEY')

MAX_REFERENCES_TO_LOAD = 3


cache = FileCache("gradio-example-cache", True)

def make_link(data):
    return f"<a href='{data['url']}' title='{data['abstract']}'>{data['title']}</a>"

def entries2html(entries, max_ref_fetch = MAX_REFERENCES_TO_LOAD):
    html = ""
    for entry in entries:
        
        html += "<hr><div class='article'>"
        html += f"<b>{entry['published']} <a href='{entry['link']}' target='_blank'>{entry['title']}</a>"
        if "pdf_link" in entry:
            html += f" [<a href='{entry['pdf_link']}' target='_blank'>pdf</a>]"
        html += "</b>"
        
        html += f"<p class'published'>{', '.join(entry['authors'])}</p>"
        html += f"Cited by: {entry['citations']}"
        html += f"<p>{entry['abstract']}</p>"
        counter = 0
        if 'references' in entry and len(entry['references']) > 0:
            html += '<br><b>References:</b><ul>'
            for doi in entry['references']:
                if counter < max_ref_fetch:
                    d = get_all_from_doi(doi, cache)
                    if d is not None:
                        html += '<li>' + make_link(d) + '</li>'
                    else:
                        html += '<li>' + doi + '</li>'

                    counter += 1
                else:
                    html += '<li>' + doi + '</li>'
            html += '</ul>'
        html += "</div>"
        
    return html

def search_elsevier_api(query, api_key, max_results=1,start=0):
    end = start + max_results
    key = "search-" + str(max_results) + ":" + query + f"--items({start}-{end})"

    if cache and cache.exists(key):
        print("cache hit")
        return json.loads(cache.get(key))

    q = urllib.parse.quote(query)

    # Check parameters at https://dev.elsevier.com/guides/Scopus%20API%20Guide_V1_20230907.pdf from page 47 onwards
    url = f"https://api.elsevier.com/content/search/scopus?query={q}&apiKey={api_key}&count={max_results}&sort=citedby-count&start={start}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cache.set(key, json.dumps(data))
        return data
    else:
        print("Error:", response.status_code)
        return None

def search_and_fetch_abstracts(query, api_key, openai_api_key, max_results=10):
    cursor = 0
    page_size = 10
    all_results = []
    while cursor < max_results:
        search_results = search_elsevier_api(query, api_key, page_size, cursor)
        if not "entry" in search_results["search-results"]:
            break
        cursor = cursor + page_size
        all_results = all_results + search_results["search-results"]["entry"]

    results = []
    if all_results:        
        entries_with_abstracts = []
        for entry in all_results:
            doi = entry.get("prism:doi", "")
            try:                
                abstract = get_abstract_from_doi(doi, cache, True)
                references = get_references_from_doi(doi, cache, True)
            except:
                url = get_final_doi_url(doi, cache, True)
                abstract = f"<p>No abstract for:<ul><li>doi: {doi}</li><li>url: {url}</li></p>"
                references = []
            
            #entry["abstract"] = abstract
            entries_with_abstracts.append({
                "title": entry.get("dc:title", ""),
                "authors": (entry.get("creator", "").split(',')),
                "abstract": abstract,
                "references": references,
                "doi": "https://doi.org/" + doi,
                "publication": entry.get("prism:publicationName", ""),
                "citations": entry.get("citedby-count", ""),
                "link": "https://doi.org/" + doi,
                "published": entry.get("prism:coverDate", ""),
            })
            #entries_with_abstracts.append(entry)
            sample_entry = entry
        return entries_with_abstracts
    else:
        return []

def search(api_key, openai_api_key, term):
    abstracts = search_and_fetch_abstracts(term, api_key, openai_api_key, 100)
    return entries2html(abstracts)

with gr.Blocks() as demo:
    gr.Markdown("# Abstract Search")
    elsevier_api_key = gr.Textbox(label="Elsevier API key", placeholder="Elsevier API key", value=ELSEVIER_API_KEY, type="password")
    openai_api_key = gr.Textbox(label="OpenAI API key", placeholder="OpenAI API key", value=OPENAI_API_KEY, type="password")
    # https://schema.elsevier.com/dtds/document/bkapi/search/SCOPUSSearchTips.htm
    search_term = gr.Textbox(label="Search Term", placeholder='TITLE-ABS-KEY("digital twin" maritime ship)', value='TITLE-ABS-KEY("digital twin" maritime ship)')
    html = gr.HTML("For more information on how to search, check out <a href='https://schema.elsevier.com/dtds/document/bkapi/search/SCOPUSSearchTips.htm' target=_blank>this pdf</a>")

    submit = gr.Button(value="search")
    results = gr.HTML()

    submit.click(fn=search,
               inputs=[elsevier_api_key, openai_api_key, search_term],
               outputs=results)

if __name__ == "__main__":
    demo.launch()