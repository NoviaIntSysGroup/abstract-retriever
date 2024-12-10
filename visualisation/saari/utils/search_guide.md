Scopus Search Guide

# Search Language

SCOPUS Search API supports a Boolean syntax, which is a type of **search** allowing users to combine keywords with operators such as AND, NOT and OR to further produce more relevant results. For example, a **Boolean search** could be "heart" AND "brain". This would limit the **search** results to only those documents containing the two keywords.

# URL encoding

The Boolean search is submitted through the query string parameter ‘query’. As with all other query string parameters, the contents of the submitted search must be URL-encoded. It should be noted that the ‘+’ character serves a special purpose as a query string value, functioning as an equivalent to the space character (i.e. %20). In order to submit a literal character ‘+’ it must be properly URL-encoded (i.e. %2B).

| **This search...** | **must be URL-encoded as:** |
| --- | --- |
| KEY(mouse AND NOT cat OR dog) | KEY%28mouse+AND+NOT+cat+OR+dog%29 |
| KEY(cat AND dog AND NOT rodent OR mouse) | KEY%28cat+AND+dog+AND+NOT+rodent+OR+mouse%29 |
| DOI("10.1021/es052595+") | DOI%28%2210.1021%2Fes052595%2B%22%29 |

Example:

http://api.elsevier.com/content/search/scopus?query=DOI%28%2210.1021%2Fes052595%2B%22%29

# Using boolean operators

You can use Boolean operators (AND, OR, AND NOT) in your search. If you use more than one operator in your search, Scopus interprets your search according to the order of precedence. You can also use proximity operators (pre/n, w/n) with Boolean operators.

**AND**

Finds only those documents that contain all of the terms.

Use AND when all the terms must appear and may be far apart from each other. 

|     |     |
| --- | --- |
| **Example** | lesion AND pancreatic |

|     |     |
| --- | --- |
| **Note** | If you are searching for a phrase which contains the word "and," omit the word "and" from your search. For example:profit loss finds the phrase "profit and loss" |

**OR**

Finds documents that contain any of the terms.

Use OR when at least one of the terms must appear (such as synonyms, alternate spellings, or abbreviations).

|     |     |
| --- | --- |
| **Example** | kidney OR renal |

**AND NOT**

Excludes documents that include the specified term from the search.

Use AND NOT to exclude specific terms. This connector must be used at the end of a search. 

|     |     |
| --- | --- |
| **Example** | ganglia OR tumor AND NOT malignant |

|     |     |
| --- | --- |
| Note | ·         If you want to search for the words _or_, _and_, or _and not_ literally, enter them in double quotation marks: "and", "or", "and not".<br><br>·         If you enter more than one word or phrase in the same text box without using an operator, **AND** is assumed. |

# Order of precedence rules

Searches with multiple operators are processed in the following order:

1.     **OR**

2.     **AND**

3.     **AND NOT**

After the precedence rules are applied, the search is read left to right.

| **All these searches...** | **are processed as...** |
| --- | --- |
| KEY (mouse OR rat AND rodent)<br><br>KEY (rodent AND rat OR mouse)<br><br>KEY (rat OR mouse AND rodent) | KEY(mouseOR rat) AND rodent |

| **This search...** | **is processed as...** |
| --- | --- |
| KEY (mouse AND NOT cat OR dog)<br><br>KEY (cat AND dog AND NOT rodent OR mouse) | KEY((mouse) AND NOT (cat OR dog))<br><br>KEY((cat AND dog) AND NOT (rodent OR mouse)) |

|     |     |
| --- | --- |
| **Note** | **AND NOT** can give unexpected results when you have multiple operators. We recommend that you put it at the end of your searches.<br><br>For example, the following searches return a large number of results:<br><br>·         KEY(cold) AND NOT KEY(influenza)<br><br>·         KEY(cold) AND NOT KEY(influenza) AND KEY(rhinovirus)<br><br>·         KEY(cold) AND NOT (KEY(influenza) AND KEY(rhinovirus))<br><br>To exclude influenza from your search, you should use the following search instead:<br><br>KEY(cold) AND KEY(rhinovirus) AND NOT KEY(influenza) |

# Proximity operators

Scopus does not support using the operators (AND or AND NOT) as an argument to a proximity expression.

|     |     |
| --- | --- |
| **Example** | cat pre/10 (dog AND mouse) - invalid  <br>  <br>However, cat pre/10 dog AND mouse is valid because **AND**  has a lower precedence, so the search is effectively (cat pre/10 dog) AND mouse |

However, you can use the operator OR with a proximity operator.

|     |     |
| --- | --- |
| **Example** | `(water OR vinegar OR wine) w/5 (oil OR yogurt)` |

# Phrases

You can search for phrases in two ways depending on how exact a match you want to find. You can find an exact phrase or a loose or approximate phrase.

**To search for an exact phrase**

To find documents that contain an exact phrase, including any stop words, spaces, and punctuation, enclose the phrase in braces: `{oyster toadfish}`.

|     |     |
| --- | --- |
| **Example** | If you enter {oyster toadfish}, the search finds only documents that contain that exact phrase. In contrast, if you enter oyster toadfish, your search interprets that as "oyster AND toadfish" and finds documents containing both terms appearing separately or together. |

**Note**

·         Special characters are included in the search.

|     |     |
| --- | --- |
| **Example** | Searching for {heart-attack} or {heart attack} returns different results because the dash (-) is considered in the search. |

·         Wildcards are searched as characters.

|     |     |
| --- | --- |
| **Example** | Searching for {health care?} returns results such as: Who pays for health care?. |

**To search for a loose or approximate phrase**

To find documents where your search terms appear adjacent to each other, enclose the terms in double quotation marks: "cell behaviour".

When you use double quotation marks:

·         AND is not automatically inserted between terms.

|     |     |
| --- | --- |
| **Example** | Entering "heart attack"returns different results than heart attack because the latter would be searched as heart AND attack, which would find documents that contained both words, even if they were far apart from each other. The search "heart attack" only finds documents where heart and attack are adjacent to each other. |

·         Punctuation is ignored.

|     |     |
| --- | --- |
| **Example** | Entering "heart-attack" or "heart attack" returns the same results because the hyphen is ignored. |

·         Wildcards are searched as wildcards.

|     |     |
| --- | --- |
| **Example** | Searching for "criminal\* insan\*" finds criminally insane and criminal insanity. |

·         Plurals are included.

|     |     |
| --- | --- |
| **Example** | Searching for "heart attack" finds heart attack and heart attacks. |

·         Double quotation marks can also be used to search specifically for stop words, special characters, or punctuation marks, which would otherwise be ignored. To search for the double quotation character itself, place a backslash before it and enclose those 2 characters in double quotation marks:

|     |     |
| --- | --- |
| **Example** | Searching for "\\"" finds " |

# Wildcards

Use wildcard characters to search for variations of a word, making your search shorter and simpler.

|     |     |
| --- | --- |
| **Note** | Only one wildcard can be included in a single term. |

**Use this wildcard...**

**To do this...**

**Question Mark (?)**

Replace a single character anywhere in a word. Use one question mark for each character you want to replace.

|     |     |
| --- | --- |
| **Example** | `AFFIL(nure?berg)` finds `Nuremberg, Nurenberg` |

**Asterisk (\*)**

Replace multiple characters anywhere in a word.

|     |     |
| --- | --- |
| **Example** | `behav*` finds `behave, behavior, behaviour, behavioural, behaviourism`, etc. |

The asterisk replaces 0 or more characters, so it can be used to find any number or to indicate a character that may or may not be present.

|     |     |
| --- | --- |
| **Example** | `*tocopherol` finds `α-tocopherol, γ-tocopherol , δ-tocopherol, tocopherol, tocopherols`, etc. |

|     |     |
| --- | --- |
| **Note** | Scopus finds variant spellings and matches Greek characters and their common American/British English variant spellings. |

# Field Restriction

You can _search_ for a term in a specific _field_ by entering the _field_ name in your Advanced _search_:

_field\_name (search term)_

|     |     |
| --- | --- |
| **Example** | ·         The _search_ TITLE-ABS-KEY(prion disease) returns documents where the terms appear in the title, keywords, or abstract.<br><br>·         The _search_ INDEXTERMS(prion disease)returns documents with the indexing term prion disease. |

|     |     |
| --- | --- |
| **Note** | ·         A limited number of _field_ codes are available.<br><br>·         Enter _field_ codes in upper or lower case.<br><br>·         Make sure to use the correct _field_ code spelling, including hyphens.<br><br>·         Not all documents contain all _fields_. _Searching_ specific _fields_ may prevent some articles from appearing in your _search_ results. |

@ \= included in **ALL** _fields_ search

**Code**

**Description**

**Example**

**ALL**

All _Fields_

_Searches_ the following _fields_: ABS, AFFIL, ARTNUM, AUTH, AUTHCOLLAB, CHEM, CODEN, CONF, DOI, EDITOR, ISBN, ISSN, ISSUE, KEY, LANGUAGE, MANUFACTURER, PUBLISHER, PUBYEAR, REF, SEQBANK, SEQNUMBER, SRCTITLE, VOLUME, and TITLE.

ALL("heart attack") returns documents with "heart attack" in any of the _fields_ listed.

**ABS** @

Abstract

A summary of the document.

ABS(dopamine)returns documents where "dopamine" is in the document abstract.

**AF-ID** @

Affiliation ID

A unique identification number assigned to organizations affiliated with Scopus authors.

|     |     |
| --- | --- |
| **Note** | ·         You cannot _search_ using just the affiliation name. For example entering AF-ID(Harvard Medical School) would not result in a match.<br><br>·         Boolean operators cannot be used within the AF-ID _field_. |

AF-ID(Harvard Medical School 3000604) or AF-ID(3000604) returns documents written by authors affiliated with Harvard Medical School and variants of that name stored in Scopus.

**AFFIL** @

Affiliation

When _searching_ the AFFIL _field_, you can specify if you want all of your _search_ terms to be found in the same affiliation.

AFFIL is a combined _field_ that _searches_ the following author address _fields_:

·         AFFILCITY

·         AFFILCOUNTRY

·         AFFILORG.

The difference between using the field by itself and qualifying terms within subfields is that unqualified terms match against all author affiliations in a particular document and qualifying by subfields matches a specific author affiliation within the document (see example).

·         To find documents where your _search_ terms occur in the same affiliation, use:  
AFFIL(london and hospital)

or

AFFIL(AFFILCITY(london) AFFILORG(hospital))

·         To find documents where both terms appear in a document's affiliation, but not necessarily in the same affiliation, use:  
AFFIL (london) and AFFIL (hospital)

**AFFILCITY**

Affiliation city.

The city portion of an author address.

AFFILCITY(beijing) returns documents where "beijing" is the city in the author affiliation _fields_, such as:

Beijing Engineering Software Technology Co., Ltd., **Beijing** 100081, China

**AFFILCOUNTRY**

Affiliation country.

The country portion of an author address.

AFFILCOUNTRY(japan) returns documents where "japan" is the country in the author affiliation _fields_, such as:

Sojo University, Kumamoto 860-0082, **Japan**

**AFFILORG**

Affiliation organization.

The organization portion of an author address.

AFFILORG(toronto)returns documents where "toronto" is the organization in the author affiliation _fields_, such as:

Department of Mathematics, University of **Toronto**, Toronto, Ont. M5S 3G3, Canada

**ARTNUM** @

Article Number

A persistent identifier for a document used by a few publishers instead of, or in addition to, page numbers. Article numbers can be assigned at the time of electronic publication, so documents can be cited and _searched_ for earlier in the publication process.

ARTNUM(1)returns documents with article numbers, such as:

·         art. no. 1

·         art. no. EGT-Nr 1.096

**AU-ID** @

Author Identifier Number

A unique identification number assigned to Scopus authors. For more information, see Scopus Author Identifier.

|     |     |
| --- | --- |
| **Note** | ·         You cannot _search_ the AU-ID _field_ by entering an author name. For example entering AU-ID(Sato, A.) would not result in a match.<br><br>·         Boolean operators cannot be used in the AU-ID _field_. |

AU-ID(Sato, A. 100038831) or AU-ID(100038831) returns documents authored by Sato, A. and variants of that name stored in Scopus.

**AUTHOR-NAME**

Author Name

The name of an author. This _field_ finds variants for a single author name.

AUTHOR-NAME is a combined _field_ that _searches_ the following author _fields_:

·         AUTHLASTNAME

·         AUTHFIRST

·         AUTHSUFFIX

·         AUTHNAME

The difference between using the field by itself and qualifying terms within subfields is that unqualified terms match against all authors of the document and qualifying by subfields matches a specific author in the document (see example).

|     |     |
| --- | --- |
| **Note** | A comma can be used to separate last name and first name. The terms will automatically be qualified as AUTHLASTNAME and AUTHFIRST, respectively (see example). |

AUTHOR-NAME(carrera, s) returns documents with "carrera” in the last name and “s" in the first name for a specific author, including:

·         Carrera, F S

·         Carrera, S

·         Carrera, S R

·         Carrera, Samuele

·         Carrera Díaz, S

·         Carrera Justiz, S C

·         Dueñas Carrera, S

·         Sánchez Carrera, S

AUTHOR-NAME(AUTHLASTNAME(carrera) AUTHFIRST(s)) is the explicit search generated by the example above.

AUTHOR-NAME(carrera s), where no comma is provided, returns documents with documents where _any_ author with the name "carrera” and any author with the name “s", including:

·         Carrera, F S

·         Carrera, S

·         Carrera, S R

·         Carrera, Samuele

·         Carrera Díaz, S

·         Carrera Justiz, S C

·         Dueñas Carrera, S

·         Sánchez Carrera, S

·         Thomas, S

·         Carrera, M

·         …etc…

**AUTH** @

Author

A combined _field_ that _searches_ the following author _fields_:

·         AUTHLASTNAME

·         AUTHFIRST

AUTH(jr) returns documents with "jr" in the last name and first initial _fields_, including:

·         Finn Jr., C.E.

·         Jenkins, J.R.

**AUTHFIRST**

Author first initial

AUTHFIRST(j) returns documents with "j" in the author first initial _field_, including:

·         Yu, J.

·         Paradi, J.C.

·         Handelman, C.J.

·         Da Costa, J.C.S

**AUTHLASTNAME**

Author last name (family name)

AUTHLASTNAME(barney) returns documents with "barney" in the author last name _field_.

**AUTHCOLLAB** @

Collaboration Author

The name by which a group of authors is known.

AUTHCOLLAB("alpha group") returns documents with "alpha group" in the collaboration _field_.

**AUTHKEY**

Author Keywords. Keywords assigned to the document by the author.

AUTHKEY(stroke)returns documents where "stroke" is an author keyword.

**CASREGNUMBER**

CAS registry number

A numeric identifier assigned to a substance when it enters the CAS registry database.

CASREGNUMBER(1199-18-4)returns documents with "1199-18-4" in the CAS registry _fields_.

**CHEM**

Chemical

A combined _field_ that _searches_ the CHEMNAME and CASREGNUMBER _fields_.

CHEM(oxidopamine)returns documents with "oxidopamine" in the chemical name or CAS registry number _fields_.

**CHEMNAME** @

Chemical name

CHEMNAME(oxidopamine)returns documents with "oxidopamine" in the chemical name _field_.

**CODEN** @

A unique, code that identifies serial and nonserial publications.

CODEN(rnene) returns documents in the specified publication.

**CONF** @

Conference Information

A combined _field_ that _searches_ information about a conference or a conference proceeding in the CONFNAME, CONFSPONSORS, and CONFLOC _fields_.

|     |     |
| --- | --- |
| **Note** | A _search_ for an article includes conference papers. |

CONF(electrical transmission) returns documents such as:

Proceedings of the Conference: Electrical Transmission in a New Age

 **CONFLOC**

Conference location

CONFLOC(Tokyo)returns documents such as:

Proceedings - Seventh International Conference on High Performance Computing and Grid in Asia Pacific Region, HPCAsia 2004; Tokyo;

**CONFNAME**

Conference name

CONFNAME(electrical transmission)returns documents such as:

Proceedings of the Conference: Electrical Transmission in a New Age

**CONFSPONSORS**

Conference sponsors

CONFSPONSORS(IEEE)returns documents such as:

·         IEEE Aerospace Conference Proceedings

·         2004 IEEE 6th Workshop on Multimedia Signal Processing

**DOCTYPE (XX)**

Document Type

Possible values for XX are:

|     |     |
| --- | --- |
| **ar** | Article |
| **ab** | Abstract Report |
| ip  | Article in Press |
| **bk** | Book |
| **bz** | Business Article |
| **ch** | Book Chapter |
| **cp** | Conference Paper |
| **cr** | Conference Review |
| **ed** | Editorial |
| **er** | Erratum |
| **le** | Letter |
| **no** | Note |
| **pr** | Press Release |
| **re** | Review |
| **sh** | Short Survey |

DOCTYPE(ar)returns documents classified as articles.

**DOI** @

Digital Object Identifier (DOI)

A unique alphanumeric string created to identify a piece of intellectual property in an online environment.

DOI(10.1007/s00202-004-0261-3)returns the document with the matching DOI.

**EDFIRST**

Editor first name (given name)

EDFIRST(michael) returns documents with "michael" in the first name _field_.

**EDITOR** @

Editor

A combined _field_ that _searches_ the following _fields_: EDLASTNAME and EDFIRST.

EDITOR(smith) returns documents with "smith" in the editor last name and first initial _fields_.

**EDLASTNAME**

Editor last name (family name)

EDITOR(smith) returns documents with "smith" in the editor last name _field_.

**EISSN**

Electronic International Standard Serial Number

The ISSN of the electronic version of a serial publication.

EISSN(0-7623-106) or (07623106) returns documents containing "0762310669" as well as any other document containing single or multiple hyphens in any possible combination within "0-7623-106".

**EXACTSRCTITLE**

Exact Source Title

_Searches_ the title of the journal, book, conference proceeding, or report in which the document was published.

Exact source title _searches_ do not find variations of your _search_ terms—only sources that contain the exact words in your _search_ are returned.

EXACTSRCTITLE(behavior)returns documents published in the source "Physiology and Behavior", but not documents in the source "Addictive Behavior**s**".

**FIRSTAUTH**

First Author

The first author listed for a document.

FIRSTAUTH(Liming, T) returns documents with authors listed as ‘Liming, T., Mingan, S., Jiangzhong, Y., Zhenhua, T.’  The _search_ does not return a document with authors listed as ‘Mingan, S., Jiangzhong, Y., Liming, T., Zhenhua, T.’, since “Liming T.” is not the first author in the author list.

**FUND-SPONSOR**

Funding sponsor.

FUND-SPONSOR(National Aeronautics and Space Administration) returns documents with “National Aeronautics and Space Administration” mentioned as the sponsor name in the acknowledgements section of the article.

**FUND-ACR**

Funding sponsor acronym.

FUND-ACR(NASA) returns documents with “NASA” mentioned as the sponsor acronym in the acknowledgements section of the article.

**FUND-NO**

Funding grant number.

FUND-NO(CDA-8619893) returns documents with “CDA-8619893” mentioned as the grant number in the acknowledgements section of the article.

**INDEXTERMS**

Index terms.

Controlled vocabulary terms assigned to the document.

INDEXTERMS(Fluorimetric assay) returns documents where "fluorimetric assay " is an index term.

**ISBN** @

International Standard Book Number

A unique identification number assigned to all books.

ISBN(9780123456789)returns documents containing "9780123456789" as well as any other document containing single or multiple hyphens in any possible combination within "978-0-123-45678-9".

**ISSN** @

International Standard Serial Number

A unique identification number assigned to all serial publications.

ISSN(0959-8278) or (09598278) returns documents containing "09598278" as well as any other document containing single or multiple hyphens in any possible combination within "0959-8278".

_Searching_ on the ISSN _field_ also _searches_ the ISSNP and EISSN _fields_.

**ISSNP**

Print International Standard Serial Number

The ISSN of the print version of a serial publication.

ISSNP(0-7623-106) or (07623106) returns documents containing "0762310669" as well as any other document containing single or multiple hyphens in any possible combination within "0-7623-106".

**ISSUE**

Issue

Identifier for a serial publication.

ISSUE(summer)returns documents with an issue identifier of "summer".

**KEY** @

Keywords

A combined _field_ that _searches_ the AUTHKEY, INDEXTERMS, TRADENAME, and CHEMNAME _fields_.

KEY(oscillator)returns documents where "oscillator" is a keyword.

**LANGUAGE** @

Language

The language in which the original document was written.

LANGUAGE(french)returns documents originally written in French.

**MANUFACTURER**

Manufacturer

MANUFACTURER(sigma)returns documents with "sigma" in the keywords _fields_.

**PAGEFIRST**

First page

PAGEFIRST(9)returns documents with page numbers, such as:

·         9

·         9-16

**PAGELAST**

Last page

PAGELAST(9)returns documents with page numbers, such as:

·         9

·         9-16

**PAGES**

Pages

A combination _field_ that _searches_ the PAGEFIRST and PAGELAST _fields_.

PAGES(1-2)returns documents with a page number range of "1-2".

PAGES(9)returns documents with page numbers, such as:

·         1-9

·         9

·         9-16

**PMID**

PubMed Identifier

A unique identifier for all Medline documents.

PMID(10676951)returns documents that have a PubMed Identifier of "10676951".

**PUBDATETXT**

Date of publication

A text date _field_ indicating the date of publication.

PUBDATETXT(July 2004)returns documents with a publication date of "July 2004".

**PUBYEAR**

Year of Publication

A numeric _field_ indicating the year of publication.

|     |     |
| --- | --- |
| **Note** | You can indicate the year using the following operators:<br><br>·         < - Before<br><br>·         \> - After<br><br>·         \= - Equal to<br><br>You can continue to use the older notation for the above 3 operators (BEF, AFT, and IS, respectively) in numeric _fields_; saved _searches_ and alerts will continue to work as before. |

·         PUBYEAR > 1994 returns documents with a publication year after 1994.

·         PUBYEAR < 1994 returns documents with a publication year before 1994.

·         PUBYEAR = 1994 returns documents with a publication year of 1994.

**REF** @

References

When _searching_ the REF _field_, you can specify if you want all of your _search_ terms to be found in the same reference.

REF is a combined _field_ that _searches:_

·         REFAUTH

·         REFTITLE

·         REFSRCTITLE

·         REFPUBYEAR

·         REFPAGE

|     |     |
| --- | --- |
| **Note** | REF _search_ results include the URL of a website where applicable. |

·         To find documents where your _search_ terms occur in the same reference, use:  
REF(darwin 1859)

·         To find documents where both terms appear in a document's references, but not necessarily in the same reference, use:  
REF(darwin) and REF(1859)

**REFAUTH**

Reference authors.

REFAUTH is a combined _field_ that _searches:_

·         REFAUTHLASTNAME

·         REFAUTHFIRST

REFAUTH(Wu)returns documents with "Wu" in their reference author _fields_.

**REFTITLE**

Reference title

REFTITLE(dioxin)returns documents with "dioxin" in their reference title.

**REFSRCTITLE**

Reference source title

REFSRCTITLE(neuropharmacology) returns documents where "neuropharmacology" is in the source title of a reference.

**REFPUBYEAR**

Reference year

A numeric _field_ indicating the year of publication of a document reference.

|     |     |
| --- | --- |
| **Note** | You can indicate the year using the IS operator. |

REFPUBYEAR IS 1994 returns documents with references published in 1994.

**REFARTNUM**

Article Number

A persistent identifier for a document used by a few publishers instead of, or in addition to, page numbers. Article numbers can be assigned at the time of electronic publication, so documents can be cited and _searched_ for earlier in the publication process.

REFARTNUM(1)returns documents where "1" is in the article number of a document reference, such as:

·         art. no. 1

·         rt. no. EGT-Nr 1.096

**REFPAGE**

Reference page numbers

REFPAGE(75)returns documents where "75" is in the page numbering of a document reference, such as:

·         pp. 71-75

·         75 pp.

**REFPAGEFIRST**

First Page

REFPAGEFIRST(5)returns documents where "5" is in the page numbering of a document reference, such as:

·         pp. 854-879

·         pp. 5-7

**SEQBANK**

Sequence Bank

The name of the sequence bank that lists a nucleotide or amino acid sequence that is defined or mentioned in a document.

SEQBANK(GenBank)returns documents with "GenBank" in the keywords _field_.

**SEQNUMBER**

Sequence Bank Accession Number

The number assigned to an amino acid or nucleotide sequence defined or mentioned in a document.

SEQNUMBER(AB013289)returns documents with "AB013289" in the keywords _field_.

**SRCTITLE** @

Source Title

The title of the journal, book, conference proceeding, or report in which the document was published.

SRCTITLE(pacific)returns documents with "pacific" in the source title, such as:

·         Asia-Pacific Journal of Public Health

·         Pacific Conservation Biology

·         1989 Asia-Pacific Conference

**SRCTYPE (XX)**

Source Type

Possible values for XX are:

|     |     |
| --- | --- |
| **j** | Journal |
| **b** | Book |
| **k** | Book Series |
| **p** | Conference Proceeding |
| **r** | Report |
| **d** | Trade Publication |

SRCTYPE(j)returns documents from journal sources.

**SUBJAREA(XX)**

Subject Area

Possible values for XX are:

|     |     |
| --- | --- |
| **AGRI** | Agricultural and Biological Sciences |
| **ARTS** | Arts and Humanities |
| **BIOC** | Biochemistry, Genetics and Molecular Biology |
| **BUSI** | Business, Management and Accounting |
| **CENG** | Chemical Engineering |
| **CHEM** | Chemistry |
| **COMP** | Computer Science |
| **DECI** | Decision Sciences |
| **DENT** | Dentistry |
| **EART** | Earth and Planetary Sciences |
| **ECON** | Economics, Econometrics and Finance |
| **ENER** | Energy |
| **ENGI** | Engineering |
| **ENVI** | Environmental Science |
| **HEAL** | Health Professions |
| **IMMU** | Immunology and Microbiology |
| **MATE** | Materials Science |
| **MATH** | Mathematics |
| **MEDI** | Medicine |
| **NEUR** | Neuroscience |
| **NURS** | Nursing |
| **PHAR** | Pharmacology, Toxicology and Pharmaceutics |
| **PHYS** | Physics and Astronomy |
| **PSYC** | Psychology |
| **SOCI** | Social Sciences |
| **VETE** | Veterinary |
| **MULT** | Multidisciplinary |

SUBJAREA(CHEM)returns documents classified under the subject area Chemistry.

**TITLE** @

Article Title

The title of an article.

TITLE("neuropsychological evidence") returns documents with the phrase "neuropsychological evidence" in their title.

**TITLE-ABS-KEY**

A combined _field_ that _searches_ abstracts, keywords, and article titles.

TITLE-ABS-KEY("heart attack") returns documents with "heart attack" in their abstracts, article titles, or keyword _fields_.

**TITLE-ABS-KEY-AUTH**

A combined _field_ that _searches_ abstracts, article titles, keywords, and author names.

TITLE-ABS-KEY-AUTH(heart attack)returns documents with "heart attack" in their abstracts, article titles, keywords, or author name _fields_.

|     |     |
| --- | --- |
| Note | You can _search_ on the TITLE-ABS-KEY-AUTH _field_ in a Document _search_. |

**TRADENAME**

A name used to identify a commercial product or service.

TRADENAME(morbilvax) returns documents with "morbilvax" in the keywords _fields_.

**VOLUME**

Volume

Identifier for a serial publication.

VOLUME(34) returns documents with a volume number of 34.

**WEBSITE**

The URL of a website cited in the reference.

WEBSITE (bbc.co.uk) finds documents with this URL in the references.

 The list of search fields, with examples, can also be accessed through the following link:

[http://api.elsevier.com/content/search/fields/scopus](http://api.elsevier.com/content/search/fields/scopus)