# medline-trends
Retrieving data on MEDLINE-indexed literature

## Background

### MEDLINE

> MEDLINE is the [National Library of Medicine's](https://www.nlm.nih.gov/ "National Library of Medicine - National Institutes of Health") (NLM) premier bibliographic database that contains references to journal articles in life sciences, with a concentration on biomedicine.

> MEDLINE content is searchable via [PubMed](https://pubmed.ncbi.nlm.nih.gov/ "PubMed®") and constitutes the primary component of PubMed, a literature database developed and maintained by the NLM [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/ "National Center for Biotechnology Information") (NCBI). – [National Library of Medicine](https://www.nlm.nih.gov/medline/index.html "MEDLINE Home") (NLM), last reviewed 10 February 2021

### Medical Subject Headings (MeSH)

NLM uses Medical Subject Headings (MeSH) as controlled vocabulary to index its citations for PubMed. MeSH are searchable [here](https://www.ncbi.nlm.nih.gov/mesh/ "Home - MeSH - NCBI"). While MeSH were applied to earlier literature (see [OLDMEDLINE Data](https://www.nlm.nih.gov/databases/databases_oldmedline.html "OLDMEDLINE Data")), it was publications from 1966 and onwards that more consistently had MeSH applied (see [MEDLINE: Overview](https://www.nlm.nih.gov/medline/medline_overview.html "MEDLINE Overview")). However, MeSH are frequently updated, so many MeSH are not applied to literature from that far back.

## Programs

## mesh-intersections

These programs find how many MEDLINE-indexed citations from each year were tagged with combinations of specific MeSH. They produce CSV files with data like the following:

* The year of publication
* The number of "intersecting citations"—that is, the number of MEDLINE-indexed citations from that year that were tagged with both specified MeSH
* The number of intersecting citations per 1,000 total MEDLINE-indexed citations that year (In general, the number of MEDLINE-indexed citations has increased year over year. For example, there are 219,000 MEDLINE-indexed citations from 1970 but 1.639 million from 2020. As a result, looking solely at the number of intersecting citations may be misleading. This field was added to provide a better sense of trends at an intersection while filtering out some of the noise from changes in MEDLINE indexing volumes.)
* The total number of MEDLINE citations indexed that year
* In cases where the program provides one of the MeSH at the intersection, the CSV file also includes a field for the program-provided MeSH. For example, with [mesh-intersections_physician-subsets.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physician-subsets.py "medline-trends/mesh-intersections_physician-subsets.py at main • crowtherln/medline-trends"), the user provides only one MeSH, which is then intersected with "[Physicians](https://www.ncbi.nlm.nih.gov/mesh/68010820 "Physicians - MeSH - NCBI")" and all MeSH one level under "Physicians."

The values produced by these programs might serve as a proxy for interest or publication activity. One potential use case might be to see when interest in a particular intersection has peaked and waned, to consider what world events might have contributed to that, and to identify areas for further investigation.

#### [mesh-intersections.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends")

* Intersections investigated: 2 user-selected MeSH
* Lines of code to edit: 3-5
* Approximate duration: 3 minutes if the default start year is used

#### [mesh-intersections_physicians.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physicians.py "medline-trends/mesh-intersections_physicians.py at main • crowtherln/medline-trends")

* Intersections investigated: 1 user-selected MeSH with "[Physicians](https://www.ncbi.nlm.nih.gov/mesh/68010820 "Physicians - MeSH - NCBI")" and all 30 MeSH one level under it
* Lines of code to edit: 2-4
* Approximate duration: 4 minutes

#### [mesh-intersections_health-personnel.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_health-personnel.py "medline-trends/mesh-intersections_health-personnel.py at main • crowtherln/medline-trends")

* Intersections investigated: 1 user-selected MeSH with "[Health Personnel](https://www.ncbi.nlm.nih.gov/mesh/68006282) "Health Personnel - MeSH - NCBI")" and all 95 MeSH 1-2 levels under it
* Lines of code to edit: 2-4
* Approximate duration: 11 minutes
