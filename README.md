# medline-trends
Retrieving data on MEDLINE-indexed literature

## Background

### MEDLINE

> MEDLINE is the [National Library of Medicine's](https://www.nlm.nih.gov/ "National Library of Medicine - National Institutes of Health") (NLM) premier bibliographic database that contains references to journal articles in life sciences, with a concentration on biomedicine.
> MEDLINE content is searchable via [PubMed](https://pubmed.ncbi.nlm.nih.gov/ "PubMed®") and constitutes the primary component of PubMed, a literature database developed and maintained by the NLM [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/ "National Center for Biotechnology Information") (NCBI). – [National Library of Medicine](https://www.nlm.nih.gov/medline/index.html "MEDLINE Home") (NLM), last reviewed 10 February 2021

### Medical Subject Headings (MeSH)

NLM uses Medical Subject Headings (MeSH) as controlled vocabulary to index its citations for PubMed. MeSH are searchable [here](https://www.ncbi.nlm.nih.gov/mesh/ "Home - MeSH - NCBI"). While MeSH were applied to earlier literature (see [OLDMEDLINE Data](https://www.nlm.nih.gov/databases/databases_oldmedline.html "OLDMEDLINE Data")), it was publications from 1966 and onwards that more consistently had MeSH applied (see [MEDLINE: Overview](https://www.nlm.nih.gov/medline/medline_overview.html "MEDLINE Overview")). However, MeSH are frequently updated, so many MeSH are not applied to literature from that far back.

## Program

### mesh-intersections.py

[mesh-intersections.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends") finds how many MEDLINE-indexed citations from each year were tagged with two specific MeSH. The values might serve as a proxy for interest or publication activity. One purpose of the program might be to see when interest in a particular intersection has peaked and waned, to consider what world events might have contributed to that, and to identify areas for further investigation.

CAUTION: The values this program produces are not a perfect proxy, for several reasons. For example, MeSH are not perfectly applied. The number of articles indexed by MEDLINE does not remain static year over year, so an increase might simply mean that more articles overall were indexed, not necessarily that there is more interest in the intersection.
