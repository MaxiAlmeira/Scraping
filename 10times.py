from bs4 import BeautifulSoup
import requests

class event():
   
    def __init__(self,name,date,place,is_cancelled,link,categories,timing):
        self.name = name 
        self.date = date 
        self.place = place
        self.is_cancelled = is_cancelled 
        self.link = link
        self.categories = categories
        self.timing = timing


url_main = "https://10times.com/events/by-country"
page = requests.get(url_main)
soup = BeautifulSoup(page.content, "html.parser")

#EL SIGUIENTE CODIGO OBTIENE LOS LINKS PARA ENTRAR A LAS CATEGORIAS DE PAISES

table = soup.find_all('table',class_="tb-list" )
tr_table = table[0].find_all('tr')
link_countries = []
country_names = []
for tr in tr_table:
    td = tr.find('td')
    if td !=None:
        a = td.find('a').attrs.get('href')
        link = "https://10times.com" + a
        link_countries.append(link)
        country_name = td.find('a').text
        country_names.append(country_name)


