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
parse_url = "https://stat.gov.kz/"

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


def get_stats(soup):
    stat_list = soup.find(class_='info-asside-list')
    stat = stat_list.find


soup = get_request(parse_url)
get_stats(soup)