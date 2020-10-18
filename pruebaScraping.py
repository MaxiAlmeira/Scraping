from bs4 import BeautifulSoup
import requests

url = "https://www.lanacion.com.ar/"
#La siguiente instruccion es un metodo de la librería request que permite hacer un pedido al url que le pasamos
#Nos va a cargar dentro de la variable page todo el contenido en HTML de la pagina que pasamos
page = requests.get(url)
#Lo que vamos a necesitar ahora es parciar y buscar informacion dentrod el HTML
soup = BeautifulSoup(page.content,"html.parser")
content_titulos = soup.find_all('h2')
for tit in content_titulos:
    sub = tit.find_all('a')
    print(sub[0].attrs.get('title'))
