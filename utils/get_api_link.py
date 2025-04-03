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


def get_body(soup, parse_url):
    try:
        precheck_table_body = soup.find_all(class_='divTableBody')

        if len(precheck_table_body) > 1:
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

        table_body = soup.find(class_='divTableBody')

        bodies = table_body.find_all(class_='divTableRow')
        if not bodies:
            print(f"Could not find bodies in {parse_url}")
            return
        
        print(CYAN + 'body obtained successfully' + RESET)
        return bodies

    except Exception as error:
        print(RED + 'Error while getting body: ', error, RESET)


def get_link(bodies):
    try:        
        links = {}
        for body in bodies:
            link = body.find('a')
            api_link = link['href']
            link_title = link.text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')

            if not link_title or link_title == 'xls':
                link_title = body.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_').replace('\\n','')
                link_title = 'Dynamic table ' + link_title
                
            links[link_title] = url + api_link

        print(CYAN + 'links obtained successfully' + RESET)
        return links
            
    except Exception as error:
        print(RED + 'Error while getting link: ', error, RESET)


def download_excel_file(title, link, save_path='downloads'):
    os.makedirs(save_path, exist_ok=True)
    try:
        response = requests.get(link, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        filename = title + '.xlsx'
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(CYAN + f"Successfully downloaded: {filename}" + RESET)
        return filepath
    except Exception as e:
            print(RED + f"Failed to download {link}: {str(e)}" + RESET)
            return None