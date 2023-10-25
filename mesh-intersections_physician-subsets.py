#! python3
# mesh-intersections_physician-subsets.py

"""
BACKGROUND: "MEDLINE is the National Library of Medicine's (NLM)
    premier bibliographic database that contains references to journal
    articles in life sciences, with a concentration on biomedicine"
    (https://www.nlm.nih.gov/medline/index.html). Its content is
    searchable via PubMed (https://pubmed.ncbi.nlm.nih.gov/). NLM uses
    Medical Subject Headings (MeSH) as controlled vocabulary to index
    articles for PubMed.

SUMMARY: With this program, the user selects a MeSH. The program
    determines how much MEDLINE-indexed literature was published each
    year at the intersection of that MeSH and each MeSH that is one
    level beneath the "Physicians" heading, as well as the intersection
    with the "Physicians" heading itself. By "intersection," we mean
    the number of MEDLINE-indexed citations from a specified year that
    were tagged with both MeSH. The program produces a CSV file with
    the following fields:
    1) physician_subset: This is a MeSH one level below "Physicians" or
        "Physicians" itself. The intersection between this MeSH and the
        one the user selects is the source of the data for fields (2)-
        (4).
    2) year: The year in which the cited documents were published
    3) intersecting_citations: The number of MEDLINE-indexed citations
        published that year that are tagged with both the user-selected
        MeSH and the MeSH from field (1)
    (4) intersecting_citations_per_1k: The number of intersecting
        citations per 1,000 total MEDLINE-indexed citations published
        that year
    (5) total_medline_citations: The total number of MEDLINE-indexed
        citations published that year

DURATION: This program may take around 15 minutes to run. This is
    primarily due to the sleep time built in between each GET request
    to avoid overloading the server. However, I do not know what NCBI's
    rate limit is; I simply set up the program to wait 2-4 seconds
    between each request. If you need the program to be more efficient,
    you can contact NCBI about their EUtility programs at
    eutilities@ncbi.nlm.nih.gov. For more information visit
    https://www.ncbi.nlm.nih.gov/books/NBK25500/. If their rate limit
    allows for shorter wait times, you can edit the sleep times in
    lines 161 and 236 to make this program run faster.

USER ACTION ITEMS: Users need to do the following:
    1) Specify where to save the CSV file (see lines 83-85).
    2) Indicate which MeSH they want the program to look at
        intersections with physician subsets for (see lines 87-97).
    3) Determine whether they need to change the first year of
        literature for the program to search (see lines 93-110).
    4) (Optional) Decide if they want to override the default for the
        last year of literature for the program to search. The default
        is the last year that has been completed for at least three
        months (see lines 119-126)."""

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
# The random module is used to randomize the duration of time between
    # GET requests.
import random
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

# Specify which MeSH for which you want to see data on intersections
    # with physician subsets. You can search for MeSH here:
    # https://www.ncbi.nlm.nih.gov/mesh/. Make sure to keep the MeSH
    # within quotation marks.
mesh = "Internship and Residency"

# Establish the first year of literature you want to be searched.
start_year = 2017 # You may want to change this (see below).
""" 
The default start year is 2017 because most MeSH one level beneath
    "Physicians" have been applied that far back. The two exceptions
    are "Gynecologists" and "Obstetricians," which were not applied
    until 2023. (Earlier content about gynecologists and obstetricians
    was tagged with "Gynecology" or "Obstetrics.")
If the MeSH you selected was not applied that far back, YOU MAY WANT TO
    CHANGE THE START YEAR. You can use the MeSH database
    (https://www.ncbi.nlm.nih.gov/mesh/) to tell how far back a heading
    has been applied. For example, when I search for "COVID-19," I see
    that it says "Year introduced: 2021(2020)." This means that the
    term was introduced in 2021, but the heading has been retroactively
    applied to literature dating back to 2020, so the start year I
    would want to use would be 2020. (I could still run it with the
    default of 2017, but it would return a bunch of zeroes in those
    fields and would take unnecessarily longer to run.)"""

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
    beginning of line 126 and replace the value with the last year of
    literature you want to be searched."""
# end_year = 2000 # Custom end year (see lines 119-125)

# Get total MEDLINE citation counts for each year.

# Build the components for the year URLs.
yr_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term="])
# yr_url_pt_2 is the publication year. It will be added in the for loop
    # that begins in line 145.
# Add the field code for the publication year.
yr_url_pt_3 = "[pdat]"

# Create a list to which to add dictionaries for the year counts.
yr_counts = []

# Loop through each year to get total citation counts.
for yr in range(start_year, end_year + 1):
    # Put the URL together to search for data on all citations indexed
        # by MEDLINE during that year.
    yr_url = "".join([yr_url_pt_1, str(yr), yr_url_pt_3])
    # Send a GET request to the URL.
    yr_response = requests.get(yr_url)
    # Get the content of the response.
    yr_data = yr_response.text
    # Create a BeautifulSoup object.
    yr_soup = BeautifulSoup(yr_data, features = "xml")
    # Scrape the value of the "Count" attribute.
    medline_count = int(yr_soup.find("Count").text)
    # Create a dictionary with the year as the key and the MEDLINE
        # count as the value. Add it to the list created in line 142.
    yr_counts.append({"year": yr, "total_citations": medline_count})
    # Wait 2-4 seconds to avoid flooding the server.
    time.sleep(random.randint(2, 4))

# Create a list of MeSH that includes "Physicians" and all headings
    # that are one level below it.
physician_subsets = [
    "Physicians", "Allergists", "Anesthesiologists", "Cardiologists",
    "Dermatologists", "Endocrinologists", "Foreign Medical Graduates",
    "Gastroenterologists", "General Practitioners", "Geriatricians",
    "Gynecologists", "Hospitalists", "Nephrologists", "Neurologists",
    "Obstetricians", "Occupational Health Physicians", "Oncologists",
    "Ophthalmologists", "Osteopathic Physicians", "Otolaryngologists",
    "Pathologists", "Pediatricians", "Physiatrists", "Physicians, Family",
    "Physicians, Primary Care", "Physicians, Women", "Pulmonologists",
    "Radiologists", "Rheumatologists", "Surgeons", "Urologists"]

# Build the components for the intersection URLs.
x_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term=\""])
# x_url_pt_2 will be added from the physician_subsets in the for loop
    # that begins in line 200.
x_url_pt_3 = "".join([
    # Add field code and Boolean operator.
    "[mh]+AND+\"",
    # Add selected MeSH. Encode spaces and commas.
    mesh.replace(" ", "+").replace(",", "%2C"),
    # Add field code and Boolean operator.
    "[mh]+AND+"])
# x_url_pt_4 is the publication year. It will be added in the for loop
    # that begins in line 200.
# Add the field code for the publication year.
x_url_pt_5 = "[pdat]"

# Create a list to which to add dictionaries for each intersection.
mesh_intersections = []

# Loop through each subset and year to get citation counts.
for subset in physician_subsets:
    for y in yr_counts:
        # Put the URL together to search for data on citations from the
            # indicated year that are indexed with the specified MeSH
            # and the MeSH from the physician subset.
        x_url = "".join([
            x_url_pt_1,
            subset.replace(" ", "+").replace(",", "%2C"),
            x_url_pt_3, str(y["year"]), x_url_pt_5])
        # Send a GET request to the URL.
        try:
            x_response = requests.get(x_url)
            # Get the content of the response.
            x_data = x_response.text
            # Create a BeautifulSoup object.
            x_soup = BeautifulSoup(x_data, features= "xml")
            # Scrape the value of the "Count" attribute.
            x_count = int(x_soup.find("Count").text)
            # Add a dictionary to mesh_intersections.
            mesh_intersections.append({
                # The MeSH that is a subset of "Physicians"
                "physician_subset": subset,
                # The publication year
                "year": y["year"],
                # The number of intersecting citations that year
                "intersecting_citations": x_count,
                # The number of intersecting citations per 1,000 total
                    # MEDLINE-indexed citations that year
                "intersecting_citations_per_1k": round(
                    x_count / y["total_citations"]*1000, 4),
                # The total number of MEDLINE-indexed citations that
                    # year
                "total_medline_citations": y["total_citations"]})
        except:
            continue
        # Wait 2-4 seconds to avoid flooding the server.
        time.sleep(random.randint(2, 4))

# Create a filename.
filename = "".join([
    f"Physicians_{mesh}_{start_year}-{end_year}_",
    str(today.year), "-", "{:02d}".format(today.month), "-", 
    "{:02d}".format(today.day), ".csv"])

# Change to the directory to which to save the CSV file.
os.chdir(path)
# Create a dataframe out of mesh_intersections.
df = pd.DataFrame(mesh_intersections)
# Write the dataframe to a CSV file.
df.to_csv(filename, encoding = "utf-8-sig", index=False)
