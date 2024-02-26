import gradio as gr

import requests
import os
import json

from abstract_retriever import get_abstract_from_doi, get_final_doi_url
from abstract_retriever.cache import DEFAULT_CACHE_DIR

CACHE_DIR = DEFAULT_CACHE_DIR
SEARCH_CACHE_DIR = os.path.join(CACHE_DIR, "scopus_search")
ABSTRACT_CACHE_DIR = os.path.join(CACHE_DIR, "abstracts")

def entries2html(entries):
    html = ""
    for entry in entries:
        
        html += "<hr><div class='article'>"
        html += f"<b>{entry['published']} <a href='{entry['link']}' target='_blank'>{entry['title']}</a>"
        if "pdf_link" in entry:
            html += f" [<a href='{entry['pdf_link']}' target='_blank'>pdf</a>]"
        html += "</b>"
        
        html += f"<p class'published'>{', '.join(entry['authors'])}</p>"
        html += f"<p>{entry['abstract']}</p>"
        html += "</div>"
        
    return html

def search_elsevier_api(query, api_key, max_results=10):
    url = f"https://api.elsevier.com/content/search/scopus?query={query}&apiKey={api_key}&count={max_results}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def cache_search_results(query, search_results):
    cache_dir = os.path.join(SEARCH_CACHE_DIR, query.replace(" ", "_"))
    os.makedirs(cache_dir, exist_ok=True)
    with open(os.path.join(cache_dir, "page1.json"), "w") as f:
        json.dump(search_results, f)

def search_and_fetch_abstracts(query, api_key, max_results=10):
    search_results = search_elsevier_api(query, api_key, max_results)
    #print(search_results)
    results = []
    if search_results:
        cache_search_results(query, search_results)
        entries_with_abstracts = []
        for entry in search_results["search-results"]["entry"]:
            doi = entry.get("prism:doi", "")
            try:                
                abstract = get_abstract_from_doi(doi)
            except:
                url = get_final_doi_url(doi)
                abstract = f"No abstract for url {url}"
            
            #entry["abstract"] = abstract
            entries_with_abstracts.append({
                "title": entry.get("dc:title", ""),
                "authors": (entry.get("creator", "").split(',')),
                "abstract": abstract,
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

def search(api_key, term):
    abstracts = search_and_fetch_abstracts(term, api_key, 10)
    return entries2html(abstracts)

with gr.Blocks() as demo:
    gr.Markdown("# Abstract Search")
    api_key = gr.Textbox(label="Elsevier API key", placeholder="API key")
    search_term = gr.Textbox(label="Search Term", placeholder="Virtual AND Sea Commissioning")
    submit = gr.Button(value="search")
    results = gr.HTML()

    submit.click(fn=search,
               inputs=[api_key,search_term],
               outputs=results)

if __name__ == "__main__":
    demo.launch()