import requests
from bs4 import BeautifulSoup
import os

CYAN = '\033[36m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

url = "https://stat.gov.kz"
parse_url = "https://stat.gov.kz/en/industries/labor-and-income/stat-empt-unempl/dynamic-tables/"

def get_request(parse_url):
    try:
        response = requests.get(parse_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        print(CYAN + 'request obtained successfully' + RESET)
        return soup

    except requests.exceptions.RequestException as error:
        print(RED + f"Request failed: {error}" + RESET)
    except Exception as error:
        print(RED + f"Unexpected error: {error}" + RESET)

# get_request(parse_url)

def get_category(soup, category_name):
    category_div = soup.find('ul', class_='info-asside-list')
    category_list = category_div.find_all('li')
    for category in category_list:
        if category_name == category.find(class_='info-asside-item-text').text.strip().split('\n')[0]:
            nav_slide_links = category.find(class_='body-nav-slide').find_all('a')
            return [link.text.strip() for link in nav_slide_links]
        

def downloader(category_name, btn_text, all):
    print('downloader')

