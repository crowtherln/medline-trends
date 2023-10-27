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
    was published each year at the intersection of two MeSH--that is,
    it determines how many MEDLINE-indexed citations from each year
    were tagged with both MeSH. It produces a four-field CSV file. The
    fields include (1) the year of publication and (2) the number of
    citations at the intersection. However, because the number of
    MEDLINE-indexed citations has generally trended upwards year-over-
    year, this value can be misleading, so two more fields were added:
    (3) the total number of MEDLINE-indexed citations published that
    year and (4) the number of intersecting citations per 1,000 total
    citations.

DURATION: For a pair of MeSH going back to 1966, this program may take
    around 3 minutes to run. This is primarily due to the sleep time
    built in between each GET request to avoid overloading the server.
    I set up the program to wait 0.5 seconds between each request,
    which is slightly longer than the NCBI minimum recommended here:
    # https://www.ncbi.nlm.nih.gov/books/NBK25497/.

USER ACTION ITEMS: Users need to do the following:
    1) Specify where to save the CSV file (see lines 66-68).
    2) Indicate which two MeSH they want the program to look at (see
        lines 70-75).
    3) Determine whether they need to change the first year of
        literature for the program to search (see lines 77-100).
    4) (Optional) Decide if they want to override the default for the
        last year of literature for the program to search. The default
        is the last year that has been completed for at least three
        months (see lines 109-116)."""

# Import libraries.

# The URLs that this program creates are XML files. The bs4 module is
    # used to pull data from them.
from bs4 import BeautifulSoup
# The datetime module is used to establish a default end year and to
    # create a filename for the CSV file.
from datetime import date
# The os module is used to save the CSV file to the user's computer.
import os
# The pandas module is used to create a dataframe out of the list of
    # dictionaries that the for loop produces. The dataframe is what
    # gets written to the CSV file.
import pandas as pd
# The requests module is used to connect to the internet and submit a
    # GET request to each URL that this program creates.
import requests
# The time module is used to pause the program between GET requests to
    # avoid overloading the server.
import time

# Set variables.

# Specify the folder to which to save the CSV file. Keep four
    # backslashes between each folder or drive.
path = "C:\\\\Users\\\\rastley\\\\Downloads"

# Specify which two MeSH you want the program to look at the
    # intersection of. You can search for MeSH here:
    # https://www.ncbi.nlm.nih.gov/mesh/. Make sure to keep the MeSH
    # within quotation marks.
mesh_1 = "Public Health"
mesh_2 = "Communication"

# Establish the first year of literature you want to be searched.
start_year = 1966 # You may want to change this (see below).
""" 
The default start year is 1966 because that is the year from which
    MEDLINE-indexed literature more consistently had MeSH applied
    (https://www.nlm.nih.gov/medline/medline_overview.html). (For
    information on MEDLINE-indexed literature from earlier, see
    https://www.nlm.nih.gov/databases/databases_oldmedline.html.)
Because not all MeSH are applied back to 1966, YOU MAY NEED TO CHANGE
    THE START YEAR. You can use the MeSH database
    (https://www.ncbi.nlm.nih.gov/mesh/) to tell how far back a heading
    has been applied. For example, when I search for "Workforce," I see
    that it says "Year introduced: 2019(1968)." This means that the
    term was introduced in 2019, but the heading has been retroactively
    applied to literature dating back to 1968, so 1968 is the year we
    are interested in for this project. If the "Year introduced" field
    doesn't have a year in parentheses, that means that the heading has
    been applied only to citations of literature published after the
    heading was introduced. For example, when I search for "Sequence
    Analysis," it just says, "Year introduced: 1993." If I wanted data
    from the intersection of "Workforce" and "Sequence Analysis," the
    latter of the two years is the earliest I might find any
    intersecting literature, so I would want to change start_year to
    1993."""

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
    end of the year to be indexed in MEDLINE and tagged with MeSH.
If you prefer a different end year, remove the hash and space from the
    beginning of line 116 and replace the value with the last year of
    literature you want to be searched."""
# end_year = 2000 # Custom end year (see lines 109-115)

# Build the components for the intersection URLs.
x_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/.
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term=\"",
    # Add first MeSH. Encode spaces and commas.
    mesh_1.replace(" ", "+").replace(",", "%2C"),
    # Add field code and Boolean operator.
    "[mh]+AND+\"",
    # Add second MeSH. Encode spaces and commas.
    mesh_2.replace(" ", "+").replace(",", "%2C"),
    # Add field code and Boolean operator.
    "[mh]+AND+"])
# x_url_pt_2 is the publication year. It will be added in the for loop
    # that begins in line 152.
# Add the field code for the publication year.
x_url_pt_3 = "[pdat]"

# Build the components for the year URLs.
yr_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/.
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term="])
# yr_url_pt_2 is the publication year. It will be added in the for loop
    # that begins in line 152.
# Add the field code for the publication year.
yr_url_pt_3 = "[pdat]"

# Create a list to which to add dictionaries for each year.
mesh_intersections = []

# Loop through each year.
for yr in range(start_year, end_year + 1):
    # Put the URL together to search for data on all citations indexed
        # by MEDLINE during that year.
    yr_url = "".join([yr_url_pt_1, str(yr), yr_url_pt_3])
    # Send a GET request to the URL.
    yr_response = requests.get(yr_url)
    # Get the content of the response.
    yr_data = yr_response.text
    # Create a BeautifulSoup object, using lxml's XML parser.
    yr_soup = BeautifulSoup(yr_data, features = "xml")
    # Scrape the value of the "Count" attribute.
    medline_count = int(yr_soup.find("Count").text)
    # Wait 0.5 seconds to avoid overloading the server.
    time.sleep(0.5)
    # Put the URL together to search for data on citations from the
        # indicated year that are indexed with both specified MeSH.
    x_url = "".join([x_url_pt_1, str(yr), x_url_pt_3])
    # Send a GET request to the URL.
    x_response = requests.get(x_url)
    # Get the content of the response.
    x_data = x_response.text
    # Create a BeautifulSoup object, using lxml's XML parser.
    x_soup = BeautifulSoup(x_data, features= "xml")
    # Scrape the value of the "Count" attribute.
    x_count = int(x_soup.find("Count").text)
    # Create a dictionary for the values you want to add to the CSV
        # file. Add the dictionary to the list created in line 149.
    mesh_intersections.append({
        # Indicate the year the cited documents were published.
        "publication_year": yr,
        # Note how many MEDLINE-indexed citations include both MeSH.
        "intersecting_citations": x_count,
        # Note how many MEDLINE citations in total were indexed.
        "total_citations": medline_count,
        # Note how many MEDLINE-indexed citations that include both
            # MeSH there were per 1,000 total MEDLINE citations.
        "intersecting_citations_per_1k": round(
            x_count / medline_count * 1000, 4)})
    # Wait 0.5 seconds to avoid overloading the server.
    time.sleep(0.5)

# Create a filename.
filename = "".join([
    f"{mesh_1}-AND-{mesh_2}_{start_year}-{end_year}_",
    str(today.year), "-", "{:02d}".format(today.month), "-", 
    "{:02d}".format(today.day), ".csv"])

# Change to the directory to which to save the CSV file.
os.chdir(path)
# Create a dataframe out of mesh_intersections.
df = pd.DataFrame(mesh_intersections)
# Write the dataframe to a CSV file.
df.to_csv(filename, encoding = "utf-8-sig", index=False)
