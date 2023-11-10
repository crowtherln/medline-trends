#! python3
# mesh-intersections_medicine.py

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
    year at the intersection of that MeSH and each MeSH that is 1-2
    levels beneath the "Medicine" heading, as well as the intersection
    with the "Medicine" heading itself. By "intersection," we mean the
    number of MEDLINE-indexed citations from a specified year that were
    tagged with both MeSH. The program produces a CSV file with the
    following fields:
    1) medicine_subset: This is a MeSH 1-2 levels below "Medicine" or
        is "Medicine" itself. The intersection between this MeSH and
        the one the user selects is the source of the data for fields
        (2)-(4).
    2) year: The year in which the cited documents were published
    3) intersecting_citations: The number of MEDLINE-indexed citations
        published that year that are tagged with both the user-selected
        MeSH and the MeSH from field (1)
    (4) intersecting_citations_per_1k: The number of intersecting
        citations per 1,000 total MEDLINE-indexed citations published
        that year
    (5) total_medline_citations: The total number of MEDLINE-indexed
        citations published that year

DURATION: This program may take around 30 minutes to run. This is due
    in part to the sleep time built in between each GET request to
    avoid overloading the server. I set up the program to wait 0.5
    seconds between each request, which is slightly longer than the
    NCBI minimum recommended here:
    https://www.ncbi.nlm.nih.gov/books/NBK25497/.

USER ACTION ITEMS: Users need to do the following:
    1) Specify where to save the CSV file (see lines 77-79).
    2) Indicate which MeSH they want the program to look at
        intersections with health personnel subsets for (see lines 81-
        85).
    3) Determine whether they need to change the first year of
        literature for the program to search (see lines 87-103).
    4) (Optional) Decide if they want to override the default for the
        last year of literature for the program to search. The default
        is the last year that has been completed for at least three
        months (see lines 112-119)."""

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

# Specify the MeSH for which you want to see data on intersections with
    # subsets of "Medicine." You can search for MeSH here:
    # https://www.ncbi.nlm.nih.gov/mesh/. Make sure to keep the MeSH
    # within quotation marks.
mesh = "Quality of Health Care"

# Establish the first year of literature you want to be searched.
start_year = 2009 # You may want to change this (see below).
""" 
I selected a default start year of 2009 because 75% of MeSH 1-2 levels
    below "Medicine" have been applied that far back. Feel free to
    change it by editing line 88. Some other options to consider are
    1980 (50%) or 1966 (25%).
If the MeSH you selected was not applied by 2009, YOU WILL WANT TO
    CHANGE THE START YEAR. You can use the MeSH database
    (https://www.ncbi.nlm.nih.gov/mesh/) to tell how far back a heading
    has been applied. For example, when I search for "COVID-19," I see
    that it says "Year introduced: 2021(2020)." This means that the
    term was introduced in 2021, but the heading has been retroactively
    applied to literature dating back to 2020, so the start year I
    would want to use would be 2020. (I could still run it with the
    default of 2009, but it would return a bunch of zeroes in those
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
    beginning of line 119 and replace the value with the last year of
    literature you want to be searched."""
# end_year = 2000 # Custom end year (see lines 112-118)

# Get total MEDLINE citation counts for each year.

# Build the components for the year URLs.
yr_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term="])
# yr_url_pt_2 is the publication year. It will be added in the for loop
    # that begins in line 138.
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
        # count as the value. Add it to the list created in line 135.
    yr_counts.append({"year": yr, "total_citations": medline_count})
    # Wait 0.5 seconds to avoid overloading the server.
    time.sleep(0.5)

# Create a list of MeSH that includes "Medicine" and all headings that
    # are 1-2 levels below it.
medicine_subsets = [
    "Medicine", "Addiction Medicine", "Adolescent Medicine",
    "Aerospace Medicine", "Allergy and Immunology", "Immunochemistry",
    "Anesthesiology", "Bariatric Medicine", "Behavioral Medicine",
    "Clinical Medicine", "Evidence-Based Medicine", "Genomic Medicine",
    "Precision Medicine", "Community Medicine", "Dermatology",
    "Disaster Medicine", "Emergency Medicine", "Pediatric Emergency Medicine",
    "Forensic Medicine", "Forensic Genetics", "Forensic Pathology",
    "General Practice", "Family Practice", "Genetics, Medical",
    "Geography, Medical", "Topography, Medical", "Geriatrics", "Geroscience",
    "Global Health", "Hospital Medicine", "Integrative Medicine",
    "Internal Medicine", "Cardiology", "Endocrinology", "Gastroenterology",
    "Hematology", "Infectious Disease Medicine", "Medical Oncology",
    "Nephrology", "Pulmonary Medicine", "Rheumatology",
    "Sleep Medicine Specialty", "Military Medicine", "Molecular Medicine",
    "Naval Medicine", "Submarine Medicine", "Neurology", "Neuropathology",
    "Neurotology", "Osteopathic Medicine", "Palliative Medicine", "Pathology",
    "Pathology, Clinical", "Pathology, Molecular", "Pathology, Surgical",
    "Telepathology", "Pediatrics", "Neonatology", "Perinatology",
    "Perioperative Medicine", "Physical and Rehabilitation Medicine",
    "Rehabilitation", "Psychiatry", "Adolescent Psychiatry",
    "Biological Psychiatry", "Child Psychiatry", "Community Psychiatry",
    "Forensic Psychiatry", "Geriatric Psychiatry", "Military Psychiatry",
    "Neuropsychiatry", "Public Health", "Epidemiology", "Preventive Medicine",
    "Radiology", "Imaging Genomics", "Nuclear Medicine", "Radiation Genomics",
    "Radiation Oncology", "Radiology, Interventional",
    "Regenerative Medicine", "Reproductive Medicine", "Andrology",
    "Gynecology", "Social Medicine", "Specialties, Surgical",
    "Colorectal Surgery", "General Surgery", "Neurosurgery", "Obstetrics",
    "Ophthalmology", "Orthognathic Surgery", "Orthopedics", "Otolaryngology",
    "Surgery, Plastic", "Surgical Oncology", "Thoracic Surgery",
    "Traumatology", "Urology", "Sports Medicine",
    "Sports Nutritional Sciences", "Veterinary Sports Medicine",
    "Telemedicine", "Teleradiology", "Telerehabilitation",
    "Theranostic Nanomedicine", "Travel Medicine", "Tropical Medicine",
    "Vaccinology", "Venereology", "Wilderness Medicine"]

# Build the components for the intersection URLs.
x_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term=\""])
# x_url_pt_2 will be added from the medicine_subsets in the for loop
    # that begins in line 219.
x_url_pt_3 = "".join([
    # Add field code and Boolean operator.
    "[mh]+AND+\"",
    # Add selected MeSH. Encode spaces and commas.
    mesh.replace(" ", "+").replace(",", "%2C"),
    # Add field code and Boolean operator.
    "[mh]+AND+"])
# x_url_pt_4 is the publication year. It will be added in the for loop
    # that begins in line 219.
# Add the field code for the publication year.
x_url_pt_5 = "[pdat]"

# Create a list to which to add dictionaries for each intersection.
mesh_intersections = []

# Loop through each subset and year to get citation counts.
for subset in medicine_subsets:
    for y in yr_counts:
        # Put the URL together to search for data on citations from the
            # indicated year that are indexed with the specified MeSH
            # and the MeSH from the medicine subset.
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
                # The MeSH that is a subset of "Medicine"
                "medicine_subset": subset,
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
        # Wait 0.5 seconds to avoid overloading the server.
        time.sleep(0.5)

# Format the user-selected MeSH for the filename by making it lowercase
    # and replacing any spaces with hyphens.
fn_mesh = mesh.replace(" ", "-").lower()

# Create a filename.
filename = "".join([
    f"medicine_{fn_mesh}_{start_year}-{end_year}_",
    str(today.year), "-", "{:02d}".format(today.month), "-", 
    "{:02d}".format(today.day), ".csv"])

# Change to the directory to which to save the CSV file.
os.chdir(path)
# Create a dataframe out of mesh_intersections.
df = pd.DataFrame(mesh_intersections)
# Write the dataframe to a CSV file.
df.to_csv(filename, encoding = "utf-8-sig", index=False)
