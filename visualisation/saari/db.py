from fasthtml.common import database
from datetime import datetime
import uuid

db = database('data/db/saari.db')

class User:
    name:str; 
    pwd:str;

class Paper:
    id: str
    title: str
    doi: str
    abstract: str
    year: str
    authors: str  # Authors as a delimited string, e.g., "Author1; Author2"
    publication: str
    issn: str  # International Standard Serial Number
    volume: str  # Volume of the journal
    issue: str  # Issue number
    page_range: str  # Page range, if applicable
    cover_date: str  # Date of publication in string format, e.g., "YYYY-MM-DD"
    cited_by_count: int  # Number of citations
    affiliation_name: str  # Name of the main affiliation
    affiliation_city: str  # City of the affiliation
    affiliation_country: str  # Country of the affiliation
    indexed_keywords: str  # Indexed keywords as a delimited string
    author_keywords: str  # Author-provided keywords as a delimited string
    open_access: bool  # Open access flag
    subtype: str  # Subtype of the paper, e.g., "ar" for article
    subtype_description: str  # Description of the subtype

class Study:
    id: str
    user: str
    title: str
    goal: str
    lastupdated: datetime
    dirty: bool

class Search:
    id: str
    query: str
    study: str
    title: str
    lastupdated: datetime

class SearchResult:
    search: str
    paper: str
    order: int


users = db.create(User, pk='name')
studies = db.create(Study, pk='id', foreign_keys=['user'])
searches = db.create(Search, pk='id', foreign_keys=['study'])
papers = db.create(Paper, pk='id')
search_results = db.create(SearchResult, pk=['search', 'paper'], foreign_keys=['search', 'paper'])

