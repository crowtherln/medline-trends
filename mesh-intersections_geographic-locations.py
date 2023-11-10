#! python3
# mesh-intersections_geographic-locations.py

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
    year at the intersection of that MeSH and many MeSH under the
    "Geographic Locations" heading. By "intersection," we mean the 
    number of MEDLINE-indexed citations from a specified year that were
    tagged with both MeSH. The program produces a CSV file with the
    following fields:
    1) geographic_location: This is a MeSH 1-4 levels below "Geographic
        Locations." The intersection between this MeSH and the one the
        user selects is the source of the data for fields (2)-(4).
    2) year: The year in which the cited documents were published
    3) intersecting_citations: The number of MEDLINE-indexed citations
        published that year that are tagged with both the user-selected
        MeSH and the MeSH from field (1)
    (4) intersecting_citations_per_1k: The number of intersecting
        citations per 1,000 total MEDLINE-indexed citations published
        that year
    (5) total_medline_citations: The total number of MEDLINE-indexed
        citations published that year

CAVEAT: MEDLINE-indexed articles are not reliably tagged with
    geographic location MeSH, so the data this program produces is not
    necessarily reflective of how much literature there is from or
    about a particular location on a particular topic.

USER ACTION ITEMS: Users need to do the following:
    1) Specify where to save the CSV file (see lines 156-158).
    2) Indicate which MeSH they want the program to look at
        intersections with health personnel places for (see lines 160-
        164).
    3) Determine whether they need to change the first year of
        literature for the program to search (see lines 166-192).
    4) (Optional) Decide if they want to override the default for the
        last year of literature for the program to search. The default
        is the last year that has been completed for at least three
        months (see lines 201-208).

DURATION: If you use the default start and end years, this program may
    take around 3 hours and 45 minutes to run. During that time, if
    your computer sleeps, the program may pause, causing it to take
    even longer, so you may need to keep your computer active during
    that time. If you want the program to take less time, one way to do
    that is to change the start year and/or end year to reduce the
    difference between them (see user action items 3 and 4 in lines 43-
    48). Another option is to remove terms from geo_places (lines 247-
    292) to focus on the locations you are most interested in. The
    duration is due in part to the sleep time built in between each GET
    request to avoid overloading the server. I set up the program to
    wait 0.5 seconds between each request, which is slightly longer
    than the NCBI minimum recommended here:
    https://www.ncbi.nlm.nih.gov/books/NBK25497/. You can also reduce
    the program duration by reducing the wait times in lines 243 and
    354, but do NOT use a wait time less than 0.34.

GEOGRAPHIC LOCATIONS INCLUDED: As stated in lines 20-21, this program
    includes MeSH from 1-4 levels below "Geographic Locations," but it
    does not include all MeSH from those levels. It includes all MeSH
    from any level that includes a sovereign state, even if not all
    MeSH on that level are sovereign states. For example, the MeSH
    "Melanesia" includes the sovereign states of "Fiji," "Papua New
    Guinea," and "Vanuatu," along with "New Caledonia," currently part
    of overseas France, but all four locations are included. This
    practice was followed both to simplify the program and to avoid
    making any political claims about sovereignty. There were
    nonetheless some exceptions: If a MeSH from an included level had
    subheadings that included sovereign countries, the subheadings were
    included instead. For example, "Asia, Eastern" includes the
    sovereign states of "China," "Japan," "Mongolia," and "Taiwan," as
    well as "Korea," which in turn includes headings for "Democratic
    People's Republic of Korea" and "Republic of Korea." "Korea" is not
    included, but its constituent parts are. Other exceptions include
    non-polities, such as "European Alpine Region," and former
    polities, such as "USSR."
Seven other geographic locations were included: "Arctic Regions,"
    "Antarctic Regions," and the five MeSH one level below "Oceans and
    Seas." While these are not polities, and most of them are a good
    deal bigger than most sovereign states, I figured they may help
    capture some data the other terms miss--for example, if researchers
    want to study health issues facing migrants crossing the
    Mediterranean Sea or to learn about COVID-19 impacted Antarctica.
All in all, the geographic places this program looks at include all
    MeSH one level below the following MeSH, except as indicated:
    * Africa, Northern
    * Africa, Central
    * Africa, Eastern
    * Africa, Southern
    * Africa, Western
    * Caribbean Region [except "West Indies"]
    * West Indies
    * Central America
    * North America
    * South America
    * Antarctic Regions [this MeSH itself, not one level below]
    * Arctic Regions [this MeSH itself, not one level below]
    * Asia, Central
    * Asia, Eastern [except "Korea"]
    * Korea
    * Asia, Northern
    * Asia, Southeastern
    * Asia, Southern
    * Middle East
    * Europe [except "Europe, Eastern"; "European Alpine Region";
        "Mediterranean Region"; Scandinavian and Nordic Countries";
        "Transcaucasia"; and "USSR"]
    * Europe, Eastern
    * Baltic States
    * Mediterranean Islands
    * Scandinavian and Nordic Countries
    * Transcaucasia
    * Islands [except "Atlantic Islands"; "Indian Ocean Islands";
        "Mediterranean Islands"; "Pacific Islands"; and "West Indies"]
    * Atlantic Islands
    * Indian Ocean Islands
    * Pacific Islands [only "New Zealand"]
    * Melanesia
    * Micronesia
    * Polynesia
    * Australasia [except "Pacific Islands"]
    * Oceans and Seas"""

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
    # physician places. You can search for MeSH here:
    # https://www.ncbi.nlm.nih.gov/mesh/. Make sure to keep the MeSH
    # within quotation marks.
mesh = "Public Health"

# Establish the first year of literature you want to be searched.
start_year = 1966 # You may want to change this (see below).
""" 
The default start year is 1966 because that is the year from which
    MEDLINE-indexed literature more consistently had MeSH applied
    (https://www.nlm.nih.gov/medline/medline_overview.html). (For
    information on MEDLINE-indexed literature from earlier, see
    https://www.nlm.nih.gov/databases/databases_oldmedline.html.)
Because not all MeSH are applied back to 1966, YOU MAY WANT TO CHANGE
    THE START YEAR. If the MeSH you selected was not applied by 1966,
    edit line 167 to change the start year at least to the first year
    the MeSH was applied. You can use the MeSH database
    (https://www.ncbi.nlm.nih.gov/mesh/) to tell how far back a heading
    has been applied. For example, when I search for "COVID-19," I see
    that it says "Year introduced: 2021(2020)." This means that the
    term was introduced in 2021, but the heading has been retroactively
    applied to literature dating back to 2020, so the start year I
    would want to use would be 2020.
Another reason to consider changing the start year is that the longer
    the year range, the longer this program takes to run. If you don't
    need data from that long ago, you can choose a later start year to
    help the program run faster.
Note that some of the MeSH for geographic locations have also not been
    applied back to 1966. For example, the MeSH for "South Sudan" was
    introduced in 2016. Keeping an earlier start year will run searches
    for locations like these, but will simply put a zero in those
    fields."""

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
    beginning of line 208 and replace the value with the last year of
    literature you want to be searched."""
# end_year = 2000 # Custom end year (see lines 201-207)

# Get total MEDLINE citation counts for each year.

# Build the components for the year URLs.
yr_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term="])
# yr_url_pt_2 is the publication year. It will be added in the for loop
    # that begins in line 227.
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
        # count as the value. Add it to the list created in line 224.
    yr_counts.append({"year": yr, "total_citations": medline_count})
    # Wait 0.5 seconds to avoid overloading the server.
    time.sleep(0.5)

# Create a list of MeSH for geographic locations as described in lines
    # 67-131.
geo_places = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Antarctic Regions", "Antigua and Barbuda", "Arctic Regions", "Argentina",
    "Armenia", "Aruba", "Atlantic Ocean", "Australia", "Austria",
    "Azerbaijan", "Azores", "Bahamas", "Bahrain", "Balkan Peninsula",
    "Bangladesh", "Barbados", "Belgium", "Belize", "Benin", "Bermuda",
    "Bhutan", "Black Sea", "Bolivia", "Borneo", "Bosnia and Herzegovina",
    "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Caribbean Netherlands", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Cote d'Ivoire",
    "Croatia", "Cuba", "Curacao", "Cyprus", "Czech Republic",
    "Democratic People's Republic of Korea",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Falkland Islands", "Fiji", "Finland", "France", "French Guiana", "Gabon",
    "Gambia", "Georgia (Republic)", "Germany", "Ghana", "Gibraltar", "Greece",
    "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Hawaii", "Honduras", "Hungary",
    "Iceland", "India", "Indian Ocean", "Indochina", "Indonesia", "Iran",
    "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Macau", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Martinique", "Mauritania", "Mauritius",
    "Mediterranean Sea", "Mekong Valley", "Mexico", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia",
    "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "Norway", "Oman", "Pacific Ocean", "Pakistan",
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Pitcairn Island", "Poland", "Portugal", "Prince Edward Island",
    "Puerto Rico", "Qatar", "Republic of Belarus", "Republic of Korea",
    "Republic of North Macedonia", "Reunion", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia",
    "Seychelles", "Sicily", "Sierra Leone", "Singapore", "Sint Maarten",
    "Slovakia", "Slovenia", "Somalia", "South Africa", "South Sudan", "Spain",
    "Sri Lanka", "Sudan", "Suriname", "Svalbard", "Sweden", "Switzerland",
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
    "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
    "Turkmenistan", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom", "United States", "United States Virgin Islands",
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela",
    "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

# Build the components for the intersection URLs.
x_url_pt_1 = "".join([
    # Start of URL as shown in "Searching a Database" section of this
        # guide: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    "https://eutils.ncbi.nlm.nih.gov/",
    "entrez/eutils/esearch.fcgi?db=pubmed&term=\""])
# x_url_pt_2 will be added from the geo_places in the for loop
    # that begins in line 318.
x_url_pt_3 = "".join([
    # Add field code and Boolean operator.
    "[mh]+AND+\"",
    # Add selected MeSH. Encode spaces and commas.
    mesh.replace(" ", "+").replace(",", "%2C"),
    # Add field code and Boolean operator.
    "[mh]+AND+"])
# x_url_pt_4 is the publication year. It will be added in the for loop
    # that begins in line 318.
# Add the field code for the publication year.
x_url_pt_5 = "[pdat]"

# Create a list to which to add dictionaries for each intersection.
mesh_intersections = []

# Loop through each place and year to get citation counts.
for place in geo_places:
    for y in yr_counts:
        # Put the URL together to search for data on citations from the
            # indicated year that are indexed with the specified MeSH
            # and the MeSH for the geographic location.
        x_url = "".join([
            x_url_pt_1,
            place.replace(" ", "+").replace(",", "%2C"),
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
                # The MeSH that is a subset of "Geographic Locations"
                "geographic_location": place,
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
    f"geographic-locations_{fn_mesh}_{start_year}-{end_year}_",
    str(today.year), "-", "{:02d}".format(today.month), "-", 
    "{:02d}".format(today.day), ".csv"])

# Change to the directory to which to save the CSV file.
os.chdir(path)
# Create a dataframe out of mesh_intersections.
df = pd.DataFrame(mesh_intersections)
# Write the dataframe to a CSV file.
df.to_csv(filename, encoding = "utf-8-sig", index=False)
