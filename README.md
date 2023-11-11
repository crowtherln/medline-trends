# medline-trends
Retrieving data on MEDLINE-indexed literature

## Background

### MEDLINE

> MEDLINE is the [National Library of Medicine's](https://www.nlm.nih.gov/ "National Library of Medicine - National Institutes of Health") (NLM) premier bibliographic database that contains references to journal articles in life sciences, with a concentration on biomedicine.
>
> MEDLINE content is searchable via [PubMed](https://pubmed.ncbi.nlm.nih.gov/ "PubMed®") and constitutes the primary component of PubMed, a literature database developed and maintained by the NLM [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/ "National Center for Biotechnology Information") (NCBI). – [National Library of Medicine](https://www.nlm.nih.gov/medline/index.html "MEDLINE Home") (NLM), last reviewed 10 February 2021

### Medical Subject Headings (MeSH)

NLM uses Medical Subject Headings (MeSH) as controlled vocabulary to index its citations for PubMed. MeSH are searchable [here](https://www.ncbi.nlm.nih.gov/mesh/ "Home - MeSH - NCBI").

## Programs

### mesh-intersections

#### Introduction

These programs produce CSV files with data on "intersecting citations," by which I mean MEDLINE-indexed citations tagged with combinations of specific MeSH. They measure the intersections in two ways:

* Getting a count of how many such citations were published each year
* Calculating how many such citations were published each year per 1,000 overall MEDLINE citations

The point of the second way is to filter out noise from changes in MEDLINE indexing volumes, which can be considerable: For example, there are 219,000 MEDLINE-indexed citations from 1970 but 1.639 million from 2020.

#### Potential Use Cases

The data produced by these programs might serve as a proxy for interest or publication activity and might be used to explore questions like the following:

* What relationship might there be between publication activity at the intersection of public health and communication and real-world public health crises?
* Which medical specialties are more likely to have literature published regarding their interns and residents? Has this shifted over time?
* Which health professions seem to have more literature published on patient safety?
* Which countries have had more research conducted on air pollution?

#### Intersections

Below are the intersections each program looks at.

* [mesh-intersections.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends") intersects two user-selected MeSH with each other.
* [mesh-intersections_physicians.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physicians.py "medline-trends/mesh-intersections_physicians.py at main • crowtherln/medline-trends") intersects one user-selected MeSH with "[Physicians](https://www.ncbi.nlm.nih.gov/mesh/68010820 "Physicians - MeSH - NCBI")" and all 30 MeSH one level under it.
* [mesh-intersections_health-personnel.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_health-personnel.py "medline-trends/mesh-intersections_health-personnel.py at main • crowtherln/medline-trends") intersects one user-selected MeSH with "[Health Personnel](https://www.ncbi.nlm.nih.gov/mesh/68006282 "Health Personnel - MeSH - NCBI")" and all 95 MeSH one to two levels under it.
* [mesh-intersections_medicine.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_medicine.py "medline-trends/mesh-intersections_medicine.py at main • crowtherln/medline-trends") intersects one user-selected MeSH with "[Medicine](https://www.ncbi.nlm.nih.gov/mesh/68008511 "Medicine - MeSH - NCBI")" and all 110 MeSH one to two levels under it.
* [mesh-intersections_geographic-locations.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_geographic-locations.py "medline-trends/mesh-intersections_geographic-locations.py at main • crowtherln/medline-trends") intersects one user-selected MeSH with 225 MeSH from one to four levels below "[Geographic Locations](https://www.ncbi.nlm.nih.gov/mesh/68006282 "Geographic Locations - MeSH - NCBI")." The selection criteria for this list are more complicated and are described in the program documentation.

#### Basic Metrics

The table below presents some basic data for each program. This is what the field names mean:

* Program: A short name for the program with a hyperlink to the program itself
* User MeSH: The number of MeSH selected by the user
* Program MeSH: The number of MeSH selected by the program
* Edits: The number of lines of code that the user needs to edit before running the program
* Start: The default start year from which the program starts checking MEDLINE-indexed publications
* Calls: The number of API calls the program will make when using the default start year and an end year of 2022
* Duration: An estimate of how long, in hours and minutes, it may take the program to complete if you use the default start year and an end year of 2022

| Program | User MeSH | Program MeSH | Edits | Start | Calls | Duration |
| --- | ---:| ---:| ---:| ---:| ---:| ---:|
| [MeSH intersections](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends") | 2 | 0 | 3–5 | 1966 | 114 | 0:03 |
| [Physicians](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physicians.py "medline-trends/mesh-intersections_physicians.py at main • crowtherln/medline-trends") | 1 | 31 | 2–4 | 2017 | 192 | 0:04 |
| [Health personnel](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_health-personnel.py "medline-trends/mesh-intersections_health-personnel.py at main • crowtherln/medline-trends") | 1 | 96 | 2–4 | 2017 | 582 | 0:11 |
| [Medicine](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_medicine.py "medline-trends/mesh-intersections_medicine.py at main • crowtherln/medline-trends") | 1 | 111 | 2–4 | 2009 | 1,568 | 0:30 |
| [Geographic locations](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_geographic-locations.py "medline-trends/mesh-intersections_geographic-locations.py at main • crowtherln/medline-trends") | 1 | 225 | 2–4 | 1966 | 12,882 | 3:45 |

#### Reducing Program Duration

There are a few ways to reduce the lengthy duration of some of these programs. The simplest is to change the start year and/or end year to reduce the difference between them (see the user action items in the documentation for each program). To illustrate the kind of difference this can make, the table below shows how long each program may take if you use a five-year range (2018–2022) instead of the default.

| Program | Calls, 2018–2022 | Duration, 2018–2022 |
| --- | ---:| ---:|
| [MeSH intersections](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends") | 10 | 0:01 |
| [Physicians](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_physicians.py "medline-trends/mesh-intersections_physicians.py at main • crowtherln/medline-trends") | 160 | 0:03 |
| [Health personnel](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_health-personnel.py "medline-trends/mesh-intersections_health-personnel.py at main • crowtherln/medline-trends") | 485 | 0:09 |
| [Medicine](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_medicine.py "medline-trends/mesh-intersections_medicine.py at main • crowtherln/medline-trends") | 230 | 0:10 |
| [Geographic locations](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections_geographic-locations.py "medline-trends/mesh-intersections_geographic-locations.py at main • crowtherln/medline-trends") | 1,130 | 0:20 |

Another option for each program except [mesh-intersections.py](https://github.com/crowtherln/medline-trends/blob/main/mesh-intersections.py "medline-trends/mesh-intersections.py at main • crowtherln/medline-trends") is to remove terms from the program-provided list if you are interested in data for only some of them.

A third option is to reduce the amount of sleep time built in between each GET request. I set up the programs to wait 0.5 seconds between each requests, which is slightly longer than the NCBI minimum recommended [here](https://www.ncbi.nlm.nih.gov/books/NBK25497/ "A General Introduction to the E-utilities - Entrez Programming Utilities Help - NCBI Bookshelf"). However, do NOT reduce the sleep time to anything less than 0.34.

#### Default Start and End Years

While MeSH were applied to earlier literature (see [OLDMEDLINE Data](https://www.nlm.nih.gov/databases/databases_oldmedline.html "OLDMEDLINE Data")), it was publications from 1966 and onwards that more consistently had MeSH applied (see [MEDLINE: Overview](https://www.nlm.nih.gov/medline/medline_overview.html "MEDLINE Overview")), so 1966 is the earliest default start year used for any of the programs. However, MeSH are frequently updated, so many MeSH are not applied to literature from that far back, which is why some of the programs have later start years.

The default end year is the most recent year that has been completed for at least three months. This allows some time for literature published toward the end of the year to be indexed in MEDLINE and tagged with MeSH, thus making years more comparable. When these programs were written (fall 2023), 2022 was the default end year.
