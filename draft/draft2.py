import requests
from bs4 import BeautifulSoup
import tkinter
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


def get_category(soup, category_name):
    category_div = soup.find('ul', class_='info-asside-list')
    category_list = category_div.find_all('li')
    for category in category_list:
        if category_name == category.find(class_='info-asside-item-text').text.strip().split('\n')[0]:
            nav_slide_links = category.find(class_='body-nav-slide').find_all('a')
            return [link.text.strip() for link in nav_slide_links]
            # for nav_slide_link in nav_slide_links:
            #     text = nav_slide_link.text.strip().split('\n')[0]
            #     print(text.strip().split('\n'))

    # for category_item in category_list:
    #     if category_name == category_item.find(class_='info-asside-item-text').text.strip():
    #         print(category_name +)

    #         print(category_text).text.strip()
    #         if category_name == category_text:
    #             print(category_text)


    # print(category)


def show_categories(parse_url, category_name):

    soup = get_request(parse_url)
    return get_category(soup, category_name)

# soup = get_request(parse_url)
# print(get_category(soup, 'Industry statistics'))


# print(show_categories(parse_url, 'Social statistics'))