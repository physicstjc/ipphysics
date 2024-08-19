import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Define the URL of the website you want to scrape
url = "https://www.savemyexams.co.uk/igcse-physics-cie-new/past-papers/"

# Define the location where you want to save the downloaded PDFs
folder_location = r'/Users/tansk/downloads'

# Create the folder if it doesn't exist
if not os.path.exists(folder_location):
    os.mkdir(folder_location)

# Send a GET request to the website
response = requests.get(url)

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all links that end with .pdf
for link in soup.select("a[href$='.pdf']"):
    # Create the complete filename by joining the folder location with the file name extracted from the link
    filename = os.path.join(folder_location, link['href'].split('/')[-1])
    
    # Send a GET request to download the PDF
    with open(filename, 'wb') as f:
        f.write(requests.get(urljoin(url, link['href'])).content)

print("Download completed successfully!")
