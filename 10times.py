from bs4 import BeautifulSoup
import requests

class event():
   
    def __init__(self,name,date,place,is_cancelled,is_online,link,categories,timing):
        self.name = name 
        self.date = date 
        self.place = place
        self.is_cancelled = is_cancelled 
        self.is_online = is_online 
        self.link = link
        self.categories = categories
        self.timing = timing


url_main = "https://10times.com/events/by-country"
page = requests.get(url_main)
soup = BeautifulSoup(page.content, "html.parser")

def get_event_date(soup_event):
    try:
        if soup_event.find('strike') != None:
            name = soup_event.find('h1').text
            strike = soup_event.find('strike')
            date = strike.find('span').attrs.get("content")
            is_cancelled = True
            is_online = False
        elif soup_event.find('div',class_="header_date color_orange mt-5") != None: 
            name = soup_event.find('h1').text
            name = name.lstrip()
            div = soup_event.find('div',class_="header_date color_orange mt-5")
            date = div.find('span').attrs.get('content')
            is_cancelled = False
            is_online = True
        else:
            name = soup_event.find('h1').text
            div = soup_event.find('div',class_="lead mb-0")
            date = div.find('span').attrs.get("content")
            is_cancelled = False
            is_online = False
        return name,date,is_cancelled,is_online
    except:
        print("Error al leer la fecha")
        return "0000-00-00",True


def recorrer_eventos(links_events):
    count = 0
    for link in links_events:
        try:
            print("\n::::::::INGRESAMOS AL LINK DE UN EVENTO Y OBTENEMOS SUS DATOS::::::::\n")
            url_event = link
            page_event = requests.get(url_event)
            soup_event = BeautifulSoup(page_event.content, "html.parser")
            name,date,is_cancelled,is_online = get_event_date(soup_event)
            
            print("Nombre: "+name)
            print("Fecha: "+date)
            print("Evento cancelado" if is_cancelled else "Evento vigente")
            print("Evento online" if is_online else "Evento presencial")
            
        except:
            print("No se pudo leer los datos del evento")

        count += 1
        if count == 20:
            print("Leyó todos los eventos")
            break

#Ingresamos a cada link de paises y obtenemos enlaces de los eventos
def recorrer_paises(link_countries):
    count = 0 #Es para frenar el for y no visitar todas las paginas. Borrar al terminar el programa
    for link in link_countries:
        print("\n::::::::INGRESAMOS AL LINK DE UN PAIS Y OBTENEMOS LOS ENLACES DE SUS EVENTOS::::::::\n")

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
                    print(a)
                    links_events.append(a)
                except:
                    print("Se produjo un error. No hay enlace a evento ")    
            permite = True
        recorrer_eventos (links_events)

        count += 1
        if count == 1:
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



