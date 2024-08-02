import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape links from a given section
def scrape_links(url, section_class, limit=35):
    links = set()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    section = soup.find('div', class_=section_class)
    if section:
        link_elements = section.find_all('a', href=True)
        for link_element in link_elements[:limit]:
            link = link_element['href']
            links.add(link)

    return list(links)

# Function to scrape article details
def scrape_article_details(article_url):
    details = {
        'heading': 'N/A',
        'published_date': 'N/A',
        'main_text': 'N/A',
        'image_link': 'N/A'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        text_section = soup.find('div', class_='renderitemutils__StyledSection-sc-10yg7pe-0 gcmkQJ')
        if text_section:
            main_text_elements = text_section.find_all('p')
            details['main_text'] = '\n'.join([element.get_text(strip=True) for element in main_text_elements])

        section = soup.find('div', class_='Paris2024Header-styles__HeaderContent-sc-4b058929-0 hxilJZ')
        if section:
            heading = section.find('h1')
            if heading:
                details['heading'] = heading.get_text(strip=True)

        image_section = soup.find('picture', class_='styles__Picture-sc-3cfb7849-0 eeYsQp')
        if image_section:
            image_container = image_section.find('img')
            if image_container:
                details['image_link'] = image_container.get('src', 'N/A')

    except Exception as e:
        st.error(f"Error scraping article {article_url}: {e}")

    return details

# Function to fetch medal table data
# Medal Table Scraping
def scrape_medal_table():
    base_url = "https://olympics.com/"
    website_url = base_url + "en/paris-2024/medals?utm_campaign=dp_google"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(website_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    section = soup.find('div', class_='emotion-srm-1a32gjt')
    
    # Prepare to parse the data
    data = []
    if section:
        spans = section.find_all('span')
        current_row = []
        for span in spans:
            text = span.get_text(strip=True)
            if text:
                current_row.append(text)
                if len(current_row) == 6:
                    data.append(current_row[:-1])
                    current_row = []
        if current_row:
            if len(current_row) == 6:
                data.append(current_row[:-1])

    columns = ['Country', 'Gold', 'Silver', 'Bronze', "Total"]
    df = pd.DataFrame(data, columns=columns)
    df = df[~df['Country'].str.contains('NOCs|#', na=False)]
    df.reset_index(drop=True, inplace=True)

    return df

# News Scraping
def scrape_news():
    base_url = "https://olympics.com/"
    website_url = base_url + "en/paris-2024/news-all"
    section_class = "Grid-styles_GridContainer-sc-57f17f60-0 gaYTef ContentList-stylesContainer-sc-76ecbea3-0 dQeFNb ShowContentContentListstyles_ContentListWrapper-sc-pfcb0a-0 kupnZV"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(website_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    section = soup.find('section', class_=section_class)

    links = []
    if section:
        link_elements = section.find_all('a', href=True)
        for link_element in link_elements[:9]:
            link = link_element['href']
            links.append(link)

    return links

def scrape_news_article(article_url):
    details = {
        'heading': 'N/A',
        'published_date': 'N/A',
        'main_text': 'N/A',
        'image_link': 'N/A'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        text_section = soup.find('section', class_='Grid-styles__GridContainer-sc-57f17f60-0 gaYTef')

        if text_section:
            main_text_elements = text_section.find_all('p')
            details['main_text'] = '\n'.join([element.get_text(strip=True) for element in main_text_elements])

        section = soup.find('section', class_='Grid-styles__GridContainer-sc-57f17f60-0 gaYTef')
        if section:
            heading = section.find('h1')
            if heading:
                details['heading'] = heading.get_text(strip=True)

            image_container = text_section.find('img')
            if image_container:
                details['image_link'] = image_container.get('src', 'N/A')

    except Exception as e:
        print(f"Error scraping article {article_url}: {e}")

    return details


# Streamlit page configurations
st.set_page_config(layout="wide")

# Sidebar navigation
st.sidebar.title("Olympics Dashboard")
page = st.sidebar.selectbox("Select a page", ["Venues", "Medal Table", "News"])

# Venues Page
if page == "Venues":
    st.title("Olympic Venues")

    base_url = "https://olympics.com/"
    website_url = base_url + "en/paris-2024/venues"
    section_class = "renderitemutils__StyledSection-sc-10yg7pe-0 gcmkQJ"

    links = scrape_links(website_url, section_class)

    for i, link in enumerate(links[:6], 1):
        article_url = base_url + link if not link.startswith("http") else link
        details = scrape_article_details(article_url)

        col1, col2 = st.columns([1, 2])

        with col1:
            if details['image_link'] != 'N/A':
                st.image(details['image_link'], width=300)

        with col2:
            st.subheader(details['heading'])
            #st.write(f"**Published Date:** {details.get('published_date', 'N/A')}")
            st.write(details.get('main_text', 'N/A'))

        st.markdown("---")

# Medal Table Page
elif page == "Medal Table":
    st.title("Olympic Medal Table")
    df = scrape_medal_table()
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No medal data available.")


# News Page
elif page == "News":
    st.title("Olympics News")

    base_url = "https://olympics.com/"
    website_url = base_url + "en/paris-2024/news-all"
    section_class = "Grid-styles_GridContainer-sc-57f17f60-0 gaYTef ContentList-stylesContainer-sc-76ecbea3-0 dQeFNb ShowContentContentListstyles_ContentListWrapper-sc-pfcb0a-0 kupnZV"

    links = scrape_links(website_url, section_class)

    for i, link in enumerate(links[:6], 1):
        article_url = base_url + link if not link.startswith("http") else link
        details = scrape_article_details(article_url)

        col1, col2 = st.columns([1, 2])

        with col1:
            if details['image_link'] != 'N/A':
                st.image(details['image_link'], width=300)

        with col2:
            st.subheader(details['heading'])
            #st.write(f"**Published Date:** {details.get('published_date', 'N/A')}")
            st.write(details.get('main_text', 'N/A'))

        st.markdown("---")
    else:
        st.write("No news articles found.")

# Set background color to white
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)