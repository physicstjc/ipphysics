import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import streamlit as st

# Streamlit interface
st.title("PDF Scraper")

# Input fields for URL and folder location
url = st.text_input("Enter the URL to scrape PDFs from:", "https://www.savemyexams.co.uk/igcse-physics-cie-new/past-papers/")
folder_location = st.text_input("Enter the folder location to save PDFs:", "/Users/tansk/downloads")

# Button to start the scraping process
if st.button("Start Scraping"):
    if not os.path.exists(folder_location):
        os.mkdir(folder_location)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = soup.select("a[href$='.pdf']")

        if not pdf_links:
            st.warning("No PDF files found at the provided URL.")
        else:
            for link in pdf_links:
                filename = os.path.join(folder_location, link['href'].split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(requests.get(urljoin(url, link['href'])).content)
            st.success(f"Downloaded {len(pdf_links)} PDF files to {folder_location}")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Additional instructions or information
st.write("Enter the URL and folder location, then click 'Start Scraping' to download PDF files.")
