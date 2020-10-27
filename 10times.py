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

#---------------------///////////////////////-------------------------#

#Extraemos la cantidad de Participantes
# Estos se dividen en tres:
#     - Visitors
#     - Exibitors
#     - Delegates
# No siempre la pagina muestra todos estos datos.

def get_participants (soup_event):
    enlaces = soup_event.find('table',class_="table noBorder mng").find_all('tr')[1].find_all('td')[0].find_all('a')
    isThere_h2_a = soup_event.find('table',class_="table noBorder mng").find_all('tr')[1].find_all('td')[0].find('h2').find('a')
    if len(enlaces) == 3 and isThere_h2_a != None:
        visitors = enlaces[1].text.strip() +" "+ soup_event.find('table',class_="table noBorder mng").find_all('tr')[1].find_all('td')[0].find('div',id='name_vis').text.strip()
        exibitors = enlaces[2].text.strip() + " Exhibitors"
    elif len(enlaces)==2 and isThere_h2_a != None: #Revisar este https://10times.com/trauma-informed-school-conference
        visitors = enlaces[1].text.strip() +" "+ soup_event.find('table',class_="table noBorder mng").find_all('tr')[1].find_all('td')[0].find('div',id='name_vis').text.strip()
        exibitors = "- Exhibitors"
    elif len(enlaces) == 2 and isThere_h2_a == None:
        visitors = enlaces[0].text.strip() +" "+ soup_event.find('table',class_="table noBorder mng").find_all('tr')[1].find_all('td')[0].find('div',id='name_vis').text.strip()
        exibitors = enlaces[1].text.strip() + " Exhibitors"
    return visitors, exibitors

#---------------------///////////////////////-------------------------#

#Extraemos el link de la imagen y la guardamos en un strings
#Posteriormente tenemos que ver como descargamos esa imagen y en donde la guardamos
def get_event_image(soup_event):
    try:
        link_img = soup_event.find('img',class_='img-thumbnail img-160 lazy').attrs.get('data-src')
        return link_img
    except:
        return "No image"

#---------------------///////////////////////-------------------------#

#Extraemos las caterorias de los eventos y las guardamos en una lista 
def get_event_categories(soup_event):
    categories = soup_event.find("td",id="hvrout2").find_all('a')
    i = 0
    for category in categories:
        categories[i] = category.text
        i+=1
    return categories

#---------------------///////////////////////-------------------------#

#Extraemos el tipo de evento. Si es conference o tradeShow
def get_event_type(soup_event):
    cadena = soup_event.find('td',id="hvrout2").text
    tradeShow_word = cadena.find("Trade Show")
    conference_word = cadena.find("Conference")
    if tradeShow_word > 0:
        return "Trade Show"
    elif conference_word > 0:
        return "Conference"

#---------------------///////////////////////-------------------------#

#Extraemos la hora o el periodo de tiempo en el cual se realiza el evento
def get_timings(soup_event):
    timing = soup_event.find('tr',id='hvrout1').find('td').text.strip()
    l_aux = ""
    timing_checked = ""
    for l in timing:
        if (l == " " and l_aux == " ") or l=="\n":
            timing_checked = timing_checked + ""
        else:
            timing_checked = timing_checked + l
        l_aux = l

    return timing_checked

#---------------------///////////////////////-------------------------#

#Lee los eventos que son presenciales, esten cancelados o no
#En caso de no tener un establecimiento, define a place como  "unkown"
#Todos tienen ciudad y pais 

def get_event_place(soup_event):
    place = ""
    city = ""
    country = ""
    div = soup_event.find_all('div',class_="lead mb-0")[1]

    city = div.find_all('a')[0].text
    country = div.find_all('a')[1].text
    specific_place = div.text
    specific_place = specific_place.split(sep=',')

    if len(specific_place) == 3:
        place = specific_place[0].strip()
        city = specific_place[1].strip()
        country = specific_place[2].strip()
    elif len(specific_place) == 2:
        place = "Unknown"
        city = specific_place[0].strip()
        country = specific_place[1].strip()

    return place,city,country

#---------------------///////////////////////-------------------------#

#El siguiente bloque extrae el nombre, la fecha, el estado del evento, y si es online o presencial
#Posee un if para tres tipos de estructuras diferentes de eventos
#El primer bloque es para los eventos que han sido cancelado o pospuesto, y que son presenciales
#El segundo es para los eventos vigentes y presenciales
#El tercero es para los eventos vigentes y online (estos no son leidos por problemas posteriores a este bloque)
def get_event_data(soup_event):
    try:
        if soup_event.find('strike') != None:
            name = soup_event.find('h1').text
            strike = soup_event.find('strike')
            date = strike.find('span').attrs.get("content")
            status = soup_event.find('small',class_="font-12 status mx-5").text.strip()
            is_cancelled = True
            is_online = False
        elif soup_event.find('div',class_="header_date color_orange mt-5") != None: 
            name = soup_event.find('h1').text
            name = name.lstrip()
            div = soup_event.find('div',class_="header_date color_orange mt-5")
            date = div.find('span').attrs.get('content')
            status = "Vigente"
            is_cancelled = False
            is_online = True
        else:
            name = soup_event.find('h1').text
            div = soup_event.find('div',class_="lead mb-0")
            date = div.find('span').attrs.get("content")
            status = "Vigente"
            is_cancelled = False
            is_online = False
        return name,date,is_cancelled,is_online, status
    except:
        print("Error al leer la fecha")
        return "0000-00-00",True

#---------------------///////////////////////-------------------------#

def recorrer_eventos(links_events):
    count = 0 # Variable que limita la cantidad de eventos que se recorren
    for link in links_events:
        try:
            print("\n::::::::INGRESAMOS AL LINK DE UN EVENTO Y OBTENEMOS SUS DATOS::::::::\n")
            #Obtenemos el codigo html de cada uno de los eventos
            url_event = link
            page_event = requests.get(url_event)
            soup_event = BeautifulSoup(page_event.content, "html.parser")

            #Comenzamos a extraer los datos
            name,date,is_cancelled,is_online, status = get_event_data(soup_event)
            place, city, country = get_event_place(soup_event)
            categories = get_event_categories(soup_event)
            link_img = get_event_image(soup_event)
            event_type = get_event_type(soup_event)
            visitors, exhibitors = get_participants(soup_event)
            timing = get_timings(soup_event)


            print("Nombre: " + name)
            print("Link: " + link)
            print("Fecha: " + date)
            print("Ubicación: \n\tLugar: %s\n\tCiudad: %s\n\tPaís: %s"% (place,city,country))
            print("Hora: " + timing)
            print("Estado: " + status)
            print("Evento online" if is_online else "Evento presencial")
            print("Categorías: " )
            for category in categories:
                print("\t %s" % category)
            print("Link: \n\t"+ link_img)
            print("Tipo de evento: " + event_type)
            print("Participantes:\n\t%s\n\t%s" % (visitors,exhibitors))

        except:
            print("No se pudo leer los datos del evento")
            print(link)

        count += 1
        if count ==8:
            print("Leyó todos los eventos")
            break


#---------------------///////////////////////-------------------------#

#Ingresamos a cada link de paises y obtenemos enlaces de los eventos
def recorrer_paises(link_countries):
    count = 0 #Es para frenar el for y no visitar todas las paginas. Borrar al terminar el programa
    for link in link_countries:
        print("\n::::::::INGRESAMOS AL LINK DE UN PAIS Y OBTENEMOS LOS ENLACES DE SUS EVENTOS::::::::\n")

        url_country = link
        page_country = requests.get(url_country)
        soup_country = BeautifulSoup(page_country.content, 'html.parser') #Extraido el HTML de cada evento
        
        #Buscamos la etiqueda en donde los link de los eventos
        table_country = soup_country.find('table',class_="listing text-muted") 
        tbody_country = table_country.find('tbody',attrs={'id':'content'})
        tr_country = tbody_country.find_all('tr',class_="box")

        permite = False #Esta variable permite saltar el primer td ya que no nos interesa

        links_events = [] #En esta lista guardamos los links a todos los eventos
        for tr in tr_country:
            if permite != False:
                td = tr.find_all('td')
                try:
                    a = td[1].find('a').attrs.get('href')
                    # print(a)
                    links_events.append(a) 
                except:
                    print("Se produjo un error. No hay enlace a evento ")    
            permite = True

        recorrer_eventos (links_events)
        
        #Permite determinar la cantidad de paises que vamos a recorrer
        count += 1
        if count == 1:
            break


#---------------------///////////////////////-------------------------#

#PUNTO DE INICIO DEL PROGRAMA
#Tenemos como referencia el link de categorias por paises
#Obtenemos el codigo HTML y lo guardamos en soup
url_main = "https://10times.com/events/by-country"
page = requests.get(url_main)
soup = BeautifulSoup(page.content, "html.parser")

#EL SIGUIENTE CODIGO OBTIENE LOS LINKS PARA ENTRAR A CADA UNA DE LAS CATEGORIAS DE PAISES

table = soup.find_all('table',class_="tb-list" )
tr_table = table[0].find_all('tr')
link_countries = [] #En esta lista almacenamos todos los links 
country_names = [] #En esta guardamos los nombres de los paises (no la uso pero por las dudas la deje)
for tr in tr_table:
    td = tr.find('td')
    if td !=None:
        a = td.find('a').attrs.get('href')
        link = "https://10times.com" + a  #Creamos el link porque "a" solo es la terminacion
        link_countries.append(link)  # Guardamos el link
        country_name = td.find('a').text 
        country_names.append(country_name)      
recorrer_paises(link_countries) # Enviamos los link al metodo que obtiene los link de los eventos



