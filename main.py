import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            full_url = urljoin(url, href)
            links.append(full_url)
    
        return links
    
    except requests.exceptions.RequestException as e:
        return [f"Error: {e}"]


st.set_page_config(page_title="URL Scraper") 
st.title('URL Scraper')

url_input = st.text_input('Enter the URL of any website to scrape links from:', key='url_input', placeholder='Paste URL here')  

if st.button('Scrape Links'):
    if url_input:
        st.write(f'Scraping links from: {url_input}')
        links = get_links(url_input)
        if links:
            st.write("Here are the links found on the website:")
            for link in links:
                st.write(link)
        else:
            st.write("No links found or an error occurred.")
        
        url_input = "" 

    else:
        st.write("Please enter a valid URL.")
