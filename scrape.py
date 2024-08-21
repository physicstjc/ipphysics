import os
import requests
from urllib.parse import urljoin
import streamlit as st

# Streamlit interface
st.title("PDF Scraper")

# Input field for URL
url = st.text_input("Enter the URL to scrape PDFs from:", "https://www.savemyexams.co.uk/igcse-physics-cie-new/past-papers/")

# Use a file uploader to select any file from the desired folder
uploaded_file = st.file_uploader("Select any file from the folder you want to save PDFs to:")

# If a file is uploaded, extract the directory path
if uploaded_file is not None:
    folder_location = os.path.dirname(uploaded_file.name)
    st.write(f"PDFs will be saved to: {folder_location}")
    
    # Button to start the scraping process
    if st.button("Start Scraping"):
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

else:
    st.write("Please select a file from the folder where you want to save the PDFs.")
