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

def recorrer_eventos(links_events):
    print("\nINGRESE A RECORRER lOS LINKS DEL EVENTO DE UN PAIS\n")

#Ingresamos a cada link de paises y obtenemos enlaces de los eventos
def recorrer_paises(link_countries):
    count = 1 #Es para frenar el for y no visitar todas las paginas. Borrar al terminar el programa
    for link in link_countries:
        try:
            url_country = link
            page_country = requests.get(url_country)
            soup_country = BeautifulSoup(page_country.content, 'html.parser')
            
            table_country = soup_country.find('table',class_="listing text-muted")
            tbody_country = table_country.find('tbody',attrs={'id':'content'})
            tr_country = tbody_country.find_all('tr',class_="box")
            permite = False #Esta variable permite saltar el primer td ya que no nos interesa
            links_events = []
            for tr in tr_country:
                if permite != False:
                    td = tr.find_all('td')
                    try:
                        a = td[1].find('a').attrs.get('href')
                        links_events.append(a)
                        print(a)
                    except:
                        print("\nSe produjo un error. No hay enlace a evento\n")    
                permite = True
            recorrer_eventos (links_events)
        except:
            print("\nError en la estructura de la pagina país\n")
        count += 1
        print("\n"+str(count)+"\n")
        if count == 8:
            break


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
recorrer_paises(link_countries)



