import os
import requests
from urllib.parse import urljoin
import streamlit as st
from pathlib import Path

# Streamlit interface
st.title("PDF Scraper")

# Input field for URL
url = st.text_input("Enter the URL to scrape PDFs from:", "https://www.savemyexams.co.uk/igcse-physics-cie-new/past-papers/")

# Prompt the user for a folder name to save the files
folder_name = st.text_input("Enter a folder name to save the PDFs:")

# Use the user's home directory as the base location
base_dir = Path.home()

# Construct the full path to the folder
if folder_name:
    folder_location = base_dir / folder_name
else:
    folder_location = None

# Button to start the scraping process
if st.button("Start Scraping") and folder_location:
    if not os.path.exists(folder_location):
        os.mkdir(folder_location)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Simple string matching to find PDF links
        pdf_links = []
        for line in response.text.splitlines():
            if '.pdf' in line and 'href="' in line:
                start = line.find('href="') + len('href="')
                end = line.find('"', start)
                link = line[start:end]
                if link.endswith('.pdf'):
                    pdf_links.append(link)

        if not pdf_links:
            st.warning("No PDF files found at the provided URL.")
        else:
            for link in pdf_links:
                full_url = urljoin(url, link)
                filename = os.path.join(folder_location, link.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(requests.get(full_url).content)
            st.success(f"Downloaded {len(pdf_links)} PDF files to {folder_location}")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Additional instructions or information
st.write("Enter the URL and folder name, then click 'Start Scraping' to download PDF files.")
