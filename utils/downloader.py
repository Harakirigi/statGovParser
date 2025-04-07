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
    pages_to_parse = []
    links_to_parse = []

    for link_to_stats in links_to_stats:
        spreadsheets_page = head_request(f'{link_to_stats}spreadsheets/')
        if not spreadsheets_page:
            pass
        else:
            pages_to_parse.append(spreadsheets_page)

        dynamic_tables_page = head_request(f'{link_to_stats}dynamic-tables/')
        if not dynamic_tables_page:
            pass
        else:
            links_to_parse.append(link_to_stats)
            pages_to_parse.append(dynamic_tables_page)
            link_page_to_parse = {link_to_stats: dynamic_tables_page}

    print(pages_to_parse)
    print(links_to_parse)
    print(link_page_to_parse)

all_links = ['https://stat.gov.kz/en/industries/economy/national-accounts/', 'https://stat.gov.kz/en/industries/economy/prices/', 'https://stat.gov.kz/en/industries/economy/stat-kon-obs/', 'https://stat.gov.kz/en/industries/economy/local-market/', 'https://stat.gov.kz/en/industries/economy/foreign-market/', 'https://stat.gov.kz/en/industries/social-statistics/demography/', 'https://stat.gov.kz/en/industries/social-statistics/stat-medicine/', 'https://stat.gov.kz/en/industries/social-statistics/stat-crime/', 'https://stat.gov.kz/en/industries/social-statistics/stat-edu-science-inno/', 'https://stat.gov.kz/en/industries/social-statistics/stat-culture/', 'https://stat.gov.kz/en/cluster/', 'https://stat.gov.kz/en/industries/business-statistics/stat-industrial-production/', 'https://stat.gov.kz/en/industries/business-statistics/stat-forrest-village-hunt-fish/', 'https://stat.gov.kz/en/industries/business-statistics/stat-transport/', 'https://stat.gov.kz/en/industries/business-statistics/stat-service/', 'https://stat.gov.kz/en/industries/business-statistics/stat-energy/', 'https://stat.gov.kz/en/industries/business-statistics/stat-tourism/', 'https://stat.gov.kz/en/industries/business-statistics/stat-inno-build/', 'https://stat.gov.kz/en/industries/business-statistics/stat-invest/', 'https://stat.gov.kz/en/industries/business-statistics/stat-struct/', 'https://stat.gov.kz/en/industries/business-statistics/stat-org/', 'https://stat.gov.kz/en/industries/business-statistics/stat-it/', 'https://stat.gov.kz/en/industries/labor-and-income/stat-empt-unempl/', 'https://stat.gov.kz/en/industries/labor-and-income/stat-wags/', 'https://stat.gov.kz/en/industries/labor-and-income/stat-life/', 'https://stat.gov.kz/en/industries/environment/stat-eco/', 'https://stat.gov.kz/en/ecologic-indicators/', 'https://stat.gov.kz/en/green-economy-indicators/', 'https://stat.gov.kz/en/climate-change/', 'https://stat.gov.kz/en/sustainable-development-goals/goal/', 'https://stat.gov.kz/en/sustainable-development-goals/publications/', 'https://stat.gov.kz/en/sustainable-development-goals/millennium-development-goals/', 'https://stat.gov.kz/en/sustainable-development-goals/events-activities/', 'https://stat.gov.kz/en/sustainable-development-goals/useful-resources/', 'https://stat.gov.kz/en/sustainable-development-goals/contacts/', 'https://stat.gov.kz/en/national/2021/']

check_for_links(all_links)