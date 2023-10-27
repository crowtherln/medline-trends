# medline-trends
Retrieving data on MEDLINE-indexed literature

## Background

### MEDLINE

> MEDLINE is the [National Library of Medicine's](https://www.nlm.nih.gov/ "National Library of Medicine - National Institutes of Health") (NLM) premier bibliographic database that contains references to journal articles in life sciences, with a concentration on biomedicine.

> MEDLINE content is searchable via [PubMed](https://pubmed.ncbi.nlm.nih.gov/ "PubMed®") and constitutes the primary component of PubMed, a literature database developed and maintained by the NLM [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/ "National Center for Biotechnology Information") (NCBI). – [National Library of Medicine](https://www.nlm.nih.gov/medline/index.html "MEDLINE Home") (NLM), last reviewed 10 February 2021

### Medical Subject Headings (MeSH)

NLM uses Medical Subject Headings (MeSH) as controlled vocabulary to index its citations for PubMed. MeSH are searchable [here](https://www.ncbi.nlm.nih.gov/mesh/ "Home - MeSH - NCBI"). While MeSH were applied to earlier literature (see [OLDMEDLINE Data](https://www.nlm.nih.gov/databases/databases_oldmedline.html "OLDMEDLINE Data")), it was publications from 1966 and onwards that more consistently had MeSH applied (see [MEDLINE: Overview](https://www.nlm.nih.gov/medline/medline_overview.html "MEDLINE Overview")). However, MeSH are frequently updated, so many MeSH are not applied to literature from that far back.

## Programs

### mesh-intersections

These programs produce CSV files with data on the number of "intersecting citations" from each year—that is, the number of MEDLINE-indexed citations from the year that were tagged with combinations of specific MeSH. However, this variable alone can be misleading. Later years tend to have more MEDLINE-indexed citations than earlier years. For example, there are 219,000 MEDLINE-indexed citations from 1970 but 1.639 million from 2020. To filter out some of the noise from changes in MEDLINE indexing volumes, I added a field for the number of intersecting citations per 1,000 total MEDLINE-indexed citations from a given year.

The data produced by these programs might serve as a proxy for interest or publication activity. One potential use case might be to see when interest in a particular intersection has peaked and waned, to consider what world events might have contributed to that, and to identify areas for further investigation.

Note that approximate durations below assume the default start and end years and were measured in October 2023. Changing the start or end years will change the duration.

#### [mesh-intersections.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends")

* Intersections investigated: 2 user-selected MeSH
* Lines of code to edit: 3–5
* Default years covered: 1966–last year\*
* Approximate duration: 3 minutes

#### [mesh-intersections_physicians.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physicians.py "medline-trends/mesh-intersections_physicians.py at main • crowtherln/medline-trends")

* Intersections investigated: 1 user-selected MeSH with "[Physicians](https://www.ncbi.nlm.nih.gov/mesh/68010820 "Physicians - MeSH - NCBI")" and all 30 MeSH one level under it
* Lines of code to edit: 2–4
* Default years covered: 2017–last year\*
* Approximate duration: 4 minutes

#### [mesh-intersections_health-personnel.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_health-personnel.py "medline-trends/mesh-intersections_health-personnel.py at main • crowtherln/medline-trends")

* Intersections investigated: 1 user-selected MeSH with "[Health Personnel](https://www.ncbi.nlm.nih.gov/mesh/68006282 "Health Personnel - MeSH - NCBI")" and all 95 MeSH 1-2 levels under it
* Lines of code to edit: 2–4
* Default years covered: 2017–last year\*
* Approximate duration: 11 minutes

\* More precisely, the end year for these programs is the most recent year that has been completed for at least three months. This allows some time for literature published toward the end of the year to be indexed in MEDLINE and tagged with MeSH and makes years more comparable.
