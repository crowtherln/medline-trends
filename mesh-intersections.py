#! python3
# mesh-intersections.py

"""
BACKGROUND: "MEDLINE is the National Library of Medicine's (NLM)
    premier bibliographic database that contains references to journal
    articles in life sciences, with a concentration on biomedicine"
    (https://www.nlm.nih.gov/medline/index.html). Its content is
    searchable via PubMed (https://pubmed.ncbi.nlm.nih.gov/). NLM uses
    Medical Subject Headings (MeSH) as controlled vocabulary to index
    articles for PubMed.

SUMMARY: This program determines how much MEDLINE-indexed literature
    was published each year at the intersection of two MeSH headings.
    ("MeSH headings" is technically redundant, but NLM uses the term,
    so I will, too.) That is, it determines how many citations from
    each year were indexed that were tagged with both MeSH headings. It
    produces a two-field CSV file with year of publication and number
    of citations.

USER ACTION ITEMS: Users need to do the following:
    1) Specify where to save the CSV file (see lines 44-46).
    2) Indicate which two MeSH headings they want the program to look
        at (see lines 48-53).
    3) Determine whether they need to change the first year of
        literature for the program to search (see lines 55-74).
    4) (Optional) Decide if they want to override the default for the
        last year of literature for the program to search. The default
        is the last year that has been completed for at least three
        months (see lines 83-91)."""

# Import libraries.

from bs4 import BeautifulSoup
from datetime import date
import lxml
import os
import pandas as pd
import requests
import time # for sleep

# Set variables.

# Specify the folder to which to save the CSV file. Keep four
    # backslashes between each folder or drive.
path = "C:\\\\Users\\\\rastley\\\\Downloads"

# Specify which two MeSH headings you want the program to look at the
    # intersection of. You can search for MeSH headings here:
    # https://www.ncbi.nlm.nih.gov/mesh/. Make sure to keep the MeSH
    # headings within quotation marks.
mesh_1 = "Quality of Life"
mesh_2 = "Education, Medical, Graduate"

# Establish the first year of literature you want to be searched.
start_year = 1975 # You may want to change this (see below).
""" 
The default start year is 1966 because that is the year from which
    MEDLINE-indexed literature more consistently had MeSH headings
    applied (https://www.nlm.nih.gov/medline/medline_overview.html).
    (For information on MEDLINE-indexed literature from earlier, see
    https://www.nlm.nih.gov/databases/databases_oldmedline.html.)
Because not all MeSH headings are applied back to 1966, YOU MAY WISH TO
    CHANGE THE START YEAR. You can use the MeSH database
    (https://www.ncbi.nlm.nih.gov/mesh/) to tell how far back a heading
    has been applied. For example, when I search for "Workforce," I see
    that it says "Year introduced: 2019(1968)." This means that the
    term was introduced in 2019, but the MeSH heading has been
    retroactively applied to literature dating back to 1968. When I
    search for "Sequence Analysis," I see that the term was not
    introduced until 1993. If I wanted data from the intersection of
    the two terms, the latter of the two years is the earliest I might
    find any intersecting literature, so I will want to change
    start_year to 1993."""

# Establish the last year of literature you want to be searched.
today = date.today()
if today.month >= 4:
    end_year = today.year - 1
else:
    end_year = today.year - 2
"""
To make years more comparable, the default end year is the most
    recently completed year that has been over for at least three
    months. That allows some time for literature published toward the
    end of the year to be indexed in MEDLINE and tagged with MeSH
    headings.
If you prefer a different end year, remove the hash and space from the
    beginning of line 91 and replace the value with the last year of
    literature you want to be searched."""
# end_year = 2000 # Custom end year (see lines 83-90)

# Build the URL components.
url_pt_1 = "https://eutils.ncbi.nlm.nih.gov/"
url_pt_2 = "entrez/eutils/esearch.fcgi?db=pubmed&term=\""
url_pt_3 = mesh_1.replace(" ", "+") # Replace spaces with pluses.
url_pt_3 = url_pt_3.replace(",", "%2C") # Encode commas for URL.
url_pt_4 = "[mh]+AND+\""
url_pt_5 = mesh_2.replace(" ", "+") # Replace spaces with pluses.
url_pt_5 = url_pt_5.replace(",", "%2C") # Encode commas for URL.
url_pt_6 = "[mh]+AND+"

# Combine first six parts.
url_pt_a = url_pt_1 + url_pt_2 + url_pt_3 + url_pt_4 + url_pt_5 + url_pt_6
# The next part with be the year, which will get added in the for loop
    # that begins in line 115.
# Name the final part of the URL.
url_pt_c = "[pdat]"

# Create a list to which to add dictionaries for each year.
mesh_intersections = []

# Loop through each year and determine how many citations are indexed
    # for that year that include both MeSH headings.
for pub_year in range(start_year, end_year + 1):
    url = url_pt_a + str(pub_year) + url_pt_c #  Put the URL together.
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, features="xml")
    count = int(soup.find("Count").text)
    mesh_intersections.append({
        "year": pub_year,
        "citations": count})
    time.sleep(2) # Wait two seconds to avoid flooding the server.

# Create a filename.
filename = "".join([
    f"mesh-intersection_{mesh_1}_{mesh_2}_{start_year}-{end_year}_",
    str(today.year), "-", "{:02d}".format(today.month), "-", 
    "{:02d}".format(today.day), ".csv"])

# Change to the directory to which to save the CSV file.
os.chdir(path)
# Create a dataframe out of mesh_intersections.
df = pd.DataFrame(mesh_intersections)
# Write the dataframe to a CSV file.
df.to_csv(filename, encoding = "utf-8-sig", index=False)
