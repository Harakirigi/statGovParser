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

def get_link(bodies, json_selected):
    try:        
        links = {}
        for body in bodies:
            link = body.find('a')
            api_link = link['href']
            link_title = link.text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')

            if json_selected and link_title == 'json':
                link_title = body.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_').replace('\\n','')
                link_title = 'Dynamic table ' + link_title
                api_link = change_format(api_link, '/json')


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


def change_format(string, change):
    insert_position = -9
    pos = len(string) + insert_position
    new_s = string[:pos] + ''.join(change) + string[pos:]
    return new_s


def downloader():
    link_page_to_parse = check_for_links(all_links)

    bodies = []
    for link, page in link_page_to_parse.items():
        body = get_body(page, link)
        bodies.append(body)

    links = []
    for body in bodies:
        link = get_link(body, json_selected=True)
        links.append(link)

    for link in links:
        for title, url in link.items():
            download_excel_file(title, url)

downloader()