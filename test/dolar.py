from bs4 import BeautifulSoup
import requests

#Guardamos en una variable la direccion de la pagina a la cual le vamos a realizar scraping
url = "https://www.dolarhoy.com/"
#La siguiente instruccion es un metodo de la librería request que permite hacer un pedido al url que le pasamos
#Nos va a cargar dentro de la variable page todo el contenido en HTML de la pagina que pasamos
page = requests.get(url)
#Lo que vamos a necesitar ahora es parciar  en codigo HTML y buscar informacion dentro de este HTML
#Lo que hace el metodo es devolver una "sopa" de codigo. Nos ofrece metodos para buscar dentro de esa sopa
soup = BeautifulSoup(page.content,"html.parser")

print("||------DOLAR HOY-------||")
print("::::::::::::::::::::::::::")
row = soup.find_all('div',"col-6")
compra = row[0].find_all('span')
compra_price_clean = compra[0].text
#/////////
#El codigo de la linea 19 hasta la linea 25 es para solucionar un problema de la página
admitidos = ["1","2","3","4","5","6","7","8","9","0",",","$"]
texto = ""
for i in compra_price_clean:
    for admit in admitidos:
        if i == admit:
            texto = texto + i
compra_price_clean = texto
#//////////7
print("Precio de compra:"+compra_price_clean)

venta = row[1].find_all('span')
venta_price_clean = venta[0].text
print("Precio de venta:" + venta_price_clean)


