from bs4 import BeautifulSoup
import requests

url_main = "https://10times.com/events/by-industry"

page = requests.get(url_main)

soup = BeautifulSoup(page.content, "html.parser")

#A continuación se guardan los enlaces para cada una de las categorías
tr_table = soup.find_all('tr')
category_links = []
for tr in tr_table:
    td = tr.find('td')
    if td != None:
        atri_a = td.find('a').attrs.get('href')
        link = "https://10times.com"+ atri_a
        category_links.append(link)

print(category_links)
