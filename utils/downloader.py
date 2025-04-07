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


def head_request(url):
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

    for link_to_stats in links_to_stats:
        spreadsheets_page = get_request(f'{link_to_stats}spreadsheets/')
        if not spreadsheets_page:
            print(YELLOW, ' Non-existent page skipped', RESET)
            pass
        else:
            link_page_to_parse[f'{link_to_stats}spreadsheets/'] = spreadsheets_page
            print(GREEN, f'{link_to_stats}spreadsheets/ successfully added', RESET)

        dynamic_tables_page = get_request(f'{link_to_stats}dynamic-tables/')
        if not dynamic_tables_page:
            print(YELLOW, ' Non-existent page skipped', RESET)
            pass
        else:
            link_page_to_parse[f'{link_to_stats}dynamic-tables/'] = dynamic_tables_page
            print(GREEN, f'{link_to_stats}dynamic-tables/ successfully added', RESET)
    
    print(CYAN, 'Links and pages successfully parsed!', RESET)
    return link_page_to_parse

all_links = ['https://stat.gov.kz/en/industries/environment/stat-eco/', "https://stat.gov.kz/en/industries/economy/national-accounts/",  'https://stat.gov.kz/en/climate-change/']



def get_body(soup, parse_url):
    try:
        table_body = soup.find_all(class_='divTableBody')

        bodies_list = []
        for table in table_body:
            bodies = table.find_all(class_='divTableRow')
            if not bodies:
                print(f"Could not find bodies in {parse_url}")
                return
            bodies_list.extend(bodies)

        print(CYAN + 'body list obtained successfully' + RESET)
        return bodies_list

    except Exception as error:
        print(RED + 'Error while getting body: ', error, RESET)



link_page_to_parse = check_for_links(all_links)

for link, page in link_page_to_parse.items():
    get_body(page, link)