import requests
from bs4 import BeautifulSoup
import os
import pprint


url = "https://stat.gov.kz"
parse_url = "https://stat.gov.kz/en/industries/economy/prices/dynamic-tables/"

def get_request():
    try:
        response = requests.get(parse_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        return get_body(soup, parse_url)
    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

def get_body(soup, parse_url):
    try:
        table_body = soup.find_all(class_='divTableBody')

        if len(table_body) > 1:
            for body in table_body:
                rows = body.find_all(class_='divTableRow')
                if not rows:
                    print(f"Could not find rows in {parse_url}")
                    return
                
                get_link(rows)

            return

        rows = table_body.find_all(class_='divTableRow')
        if not rows:
            print(f"Could not find rows in {parse_url}")
            return
        
        return get_link(rows)

    except Exception as error:
        print('Error while getting body: ', error)

def get_link(rows):
    try:        
        links = {}
        for row in rows:
            link = row.find('a')
            api_link = link['href']
            link_title = link.text.strip().replace('"','').replace(' ','_')

            if not link_title or link_title == 'xls':
                link_title = row.find(class_='divTableCell').text.strip().replace('"','').replace(' ','_')
                link_title = 'Dynamic table ' + link_title
                
            links[link_title] = url + api_link

        return links
            
    except Exception as error:
        print('Error while getting link: ', error)



links = get_request()
print(links)

# def download_excel_file(title, link, save_path='downloads'):
#     os.makedirs(save_path, exist_ok=True)
#     try:
#         response = requests.get(link, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
#         response.raise_for_status()
        
#         filename = title + '.xlsx'
#         filepath = os.path.join(save_path, filename)
        
#         with open(filepath, 'wb') as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)
        
#         print(f"Successfully downloaded: {filename}")
#         return filepath
#     except Exception as e:
#             print(f"Failed to download {link}: {str(e)}")
#             return None
    
# for title, link in links.items():
#     download_excel_file(title, link)


