import requests
from bs4 import BeautifulSoup
import os


url = "https://stat.gov.kz"
parse_url = "https://stat.gov.kz/en/industries/economy/national-accounts/spreadsheets/"

def get_request():
    try:
        response = requests.get(parse_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        get_link(soup, parse_url)
    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

def get_link(soup, parse_url):
    try:
        table_body = soup.find(class_='divTableBody')

        rows = table_body.find_all(class_='divTableRow')
        if not rows:
            print(f"Could not find rows in {parse_url}")
            return
        
        links = []
        for row in rows:
            link = row.find('a')
            api_link = link['href']
            links.append(url + api_link)
        print(links)
            
    except Exception as error:
        print('Error while getting link: ', error)



get_request()
