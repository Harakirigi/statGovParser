import requests
from bs4 import BeautifulSoup
from parser import get_request
import os

CYAN = '\033[36m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

url = "https://stat.gov.kz"
parse_url = "https://stat.gov.kz/en/"


def get_request(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return True
        else:
            print(f"Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False


def check_for_links(links_to_stats):
    link_page_to_parse = {}
    pages_to_parse = []
    links_to_parse = []

    for link_to_stats in links_to_stats:
        spreadsheets_page = get_request(f'{link_to_stats}spreadsheets/')
        if not spreadsheets_page:
            pass
        else:
            pages_to_parse.append(spreadsheets_page)

        dynamic_tables_page = get_request(f'{link_to_stats}dynamic-tables/')
        if not dynamic_tables_page:
            pass
        else:
            links_to_parse.append(link_to_stats)
            pages_to_parse.append(dynamic_tables_page)
            link_page_to_parse[link_to_stats] = dynamic_tables_page

    print(pages_to_parse)
    print(links_to_parse)
    print(link_page_to_parse)

all_links = ['https://stat.gov.kz/en/industries/environment/stat-eco/', 'https://stat.gov.kz/en/climate-change/']

check_for_links(all_links)