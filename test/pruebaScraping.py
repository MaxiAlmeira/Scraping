from bs4 import BeautifulSoup
import requests

#Guardamos en una variable la direccion de la pagina a la cual le vamos a realizar scraping
url = "https://www.lanacion.com.ar/"
#La siguiente instruccion es un metodo de la librería request que permite hacer un pedido al url que le pasamos
#Nos va a cargar dentro de la variable page todo el contenido en HTML de la pagina que pasamos
page = requests.get(url)
#Lo que vamos a necesitar ahora es parciar  en codigo HTML y buscar informacion dentro de este HTML
#Lo que hace el metodo es devolver una "sopa" de codigo. Nos ofrece metodos para buscar dentro de esa sopa
soup = BeautifulSoup(page.content,"html.parser")
#Con la siguiente instruccion obtenemos todos los h2 incluido el contenido que poseen estos.
#Nos devuelve tambien otras etiquetas que estan dentro del h2
#Entre comillas simples colocamos la etiqueta HTML y entre comillas dobles la clase Css
content_titulos = soup.find_all('h2',"com-title")
#content_titulos es una lista de h2 con sub elementos
#Recorremos cada uno de esos titulos y dentro de cada uno buscamos los elementos "a"
print("||--------TITULARES LA NACION--------||")
print()
for tit in content_titulos:
    sub = tit.find_all('a')
    #Se coloca sub[0] porque find_all trae una lista asique siempre tenemos que indicar con corchetes
    #por mas que solo tenga un elemento
    #Ademas traemos el atributo titulo de esa etiqueta con el metodo attrs.get()
    print(sub[0].attrs.get('title'))
    print()

