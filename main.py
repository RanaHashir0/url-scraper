import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the base domain for comparison
        base_domain = urlparse(url).netloc

        internal_links = []
        external_links = []
        
        # Find all anchor tags with href attribute
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            link_domain = urlparse(full_url).netloc
            
            # Classify the link as internal or external
            if link_domain == base_domain:
                internal_links.append((full_url, link_domain))
            else:
                external_links.append((full_url, link_domain))
        
        return internal_links, external_links

    except requests.exceptions.RequestException as e:
        return [], [f"Error: {e}"]

st.set_page_config(page_title="URL Scraper") 
st.title('URL Scraper')

# Input URL from the user
url_input = st.text_input('Enter the URL of any website to scrape links from:', key='url_input', placeholder='Paste URL here')  

if st.button('Scrape Links'):
    if url_input:
        st.write(f'Scraping links from: {url_input}')
        internal_links, external_links = get_links(url_input)
        
        # Display External Links First
        st.subheader("External Links")
        if external_links:
            for link, domain in external_links:
                st.write(f"Website: {domain} - Link: {link}")
        else:
            st.write("No external links found.")
        
        # Display Internal Links
        st.subheader("Internal Links")
        if internal_links:
            for link, domain in internal_links:
                st.write(f"Website: {domain} - Link: {link}")
        else:
            st.write("No internal links found.")

        # Clear input for next use
        url_input = "" 

    else:
        st.write("Please enter a valid URL.")
