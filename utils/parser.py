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
parse_url = "https://stat.gov.kz/en/"

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
        

def get_page(SOUP, category_name, btn_text, all):
    if category_name == 'All' and btn_text == 'All' and all == True:
        stats_pages = []
        category_div = SOUP.find('ul', class_='info-asside-list')
        category_list = category_div.find_all('li')
        for category in category_list:
            nav_slide_links = category.find(class_='body-nav-slide').find_all('a')
            for nav_slide_link in nav_slide_links:
                if btn_text == nav_slide_link.text.strip().split('\n')[0]:
                    link_to_stats = url + nav_slide_link['href']
                    stats_page = get_request(link_to_stats)
                    return stats_page
                else:
                    print(RED + f"Link to {btn_text} not found" + RESET)
                
    if category_name != 'All' and btn_text == 'All':
        print(f'this will download everything in {category_name}')
    
    category_div = SOUP.find('ul', class_='info-asside-list')
    category_list = category_div.find_all('li')
    for category in category_list:
        if category_name == category.find(class_='info-asside-item-text').text.strip().split('\n')[0]:
            nav_slide_links = category.find(class_='body-nav-slide').find_all('a')
            for nav_slide_link in nav_slide_links:
                if btn_text == nav_slide_link.text.strip().split('\n')[0]:
                    link_to_stats = url + nav_slide_link['href']
                    stats_page = get_request(link_to_stats)
                    return stats_page
                else:
                    print(RED + f"Link to {btn_text} not found" + RESET)
            
        else:
            pass



SOUP = get_request(parse_url)
page = get_page(SOUP, "Environment", "Statistics of environment", all=False)
if page:
    print('page found')
else:
    print('page not found   ')