import requests
from bs4 import BeautifulSoup

base_url = "https://stat.gov.kz"
url = "https://stat.gov.kz/en/industries/economy/prices/dynamic-tables/"

response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    # with open("./html/file.html", 'w', encoding='utf-8') as file:
    #     file.write(html_content)
    #     file.close()
    #     print("file got written!")
else:
    print(f"Error: {response.status_code}")

soup = BeautifulSoup(html_content, "lxml")








titles = soup.find("div", class_="tables-block__title")
print(titles.find_next_sibling("div"))






format = soup.find("div", class_ = "element-file-formats")
links = [a["href"] for a in format.find_all("a", href=True)]
print(format)
print(links[0])
print(f'link is: {base_url}{links[0]}')