import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import streamlit as st

# Set up the Streamlit app
st.title("PDF Downloader from URL")

# Input box for the URL
url = st.text_input("Enter the URL:", "https://www.savemyexams.co.uk/igcse-physics-cie-new/past-papers/")

# Input box for the folder location
folder_location = st.text_input("Enter the folder location to save PDFs:", "/Users/tansk/downloads")

# Create the folder if it doesn't exist
if not os.path.exists(folder_location):
    os.mkdir(folder_location)

# Button to start the download process
if st.button("Download PDFs"):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all PDF links and download them
        for link in soup.select("a[href$='.pdf']"):
            # Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url, link['href'])).content)
        
        st.success("Download completed successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Provide some instructions or feedback to the user
st.write("Enter the URL and the folder location, then click 'Download PDFs' to start the process.")
