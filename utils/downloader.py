import requests
from bs4 import BeautifulSoup
from .parser import get_request
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


def check_for_links(links_to_stats, option):
    link_page_to_parse = {}

    match option:

        case 'Select All':
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
        
        case 'Spreadsheets only':
            for link_to_stats in links_to_stats:
                spreadsheets_page = get_request(f'{link_to_stats}spreadsheets/')
                if not spreadsheets_page:
                    print(YELLOW, ' Non-existent page skipped', RESET)
                    pass
                else:
                    link_page_to_parse[f'{link_to_stats}spreadsheets/'] = spreadsheets_page
                    print(GREEN, f'{link_to_stats}spreadsheets/ successfully added', RESET)
            
            print(CYAN, 'Links and pages successfully parsed!', RESET)
            return link_page_to_parse

        case 'Dynamic Tables only':
            for link_to_stats in links_to_stats:
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

def get_link(bodies, json_selected, csv_selected):
    try:
        links = {}
        for body in bodies:
            link = body.find('a')
            api_link = link['href']
            link_title = link.text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')

            if json_selected:
                json_table_title = body.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')
                json_table_title = 'JSON Dynamic table ' + json_table_title
                json_api_link = change_format(api_link, '/json')
                links[json_table_title] = url + json_api_link
            if csv_selected:
                csv_table_title = body.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')
                csv_table_title = 'CSV Dynamic table ' + csv_table_title
                csv_api_link = change_format(api_link, '/csv')
                links[csv_table_title] = url + csv_api_link

            if link_title == 'xls':
                table_title = body.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_').replace('\\t','').replace('\\n','')
                table_title = 'Dynamic table ' + table_title
                links[table_title] = url + api_link

            elif link_title:
                links[link_title] = url + api_link

        print(CYAN + 'links obtained successfully' + RESET)
        return links
            
    except Exception as error:
        print(RED + 'Error while getting link: ', error, RESET)


def downloader(title, link, save_path='downloads'):
    os.makedirs(save_path, exist_ok=True)
    try:
        response = requests.get(link, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        filename = title + '.xlsx'
        if title.startswith('JSON'):
            filename = title + '.json'
        filepath = os.path.join(save_path, filename)
        if title.startswith('CSV'):
            filename = title + '.csv'
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(CYAN + f"Successfully downloaded: {filename}" + RESET)
        return f"✅ Successfully downloaded: {filename}"
    except requests.exceptions.HTTPError:
        print(YELLOW + f"HTTP error for: {link}" + RESET)
        return f"⚠️ HTTP error for: {link}"
    except Exception as e:
        print(RED + f"Failed to download {link}: {str(e)}" + RESET)
        return f"❌ Failed to download {link}: {str(e)}"


def change_format(string, change):
    insert_position = -9
    pos = len(string) + insert_position
    new_s = string[:pos] + ''.join(change) + string[pos:]
    return new_s


# def downloader(links_to_stats, option, json_selected, csv_selected):
#     link_page_to_parse = check_for_links(links_to_stats, option)

#     bodies = []
#     for link, page in link_page_to_parse.items():
#         body = get_body(page, link)
#         bodies.append(body)

#     links = []
#     for body in bodies:
#         link = get_link(body, json_selected, csv_selected)
#         links.append(link)


#     for link in links:
#         for title, url in link.items():
#             message = download_excel_file(title, url)
#             return message

# downloader(['https://stat.gov.kz/en/industries/economy/national-accounts/'], 'Spreadsheets only', False, False)