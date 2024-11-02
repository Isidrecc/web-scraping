"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO

EDIT POR: ISIDRE CAÑELLAS 02/11/2024
El cambio entre páginas en la web ya no se realiza con el botón "cargar más", ahora tenemos una lista de páginas
Puede que fuera mejor aplicar SCRAPY para extraer información en esta web
Modifico la estructura del código añadiendo una iteración for para acceder a cada página
Modificio también la manera en que obtenemos la descripción de cada anuncio
"""

#####
### ATENCION: OLX necesita que le demos permisos de geolocalizacion al navegador de selenium para que nos muestre los datos
### Esto lo haremos una unica vez en la primer corrida del programa. Este problema es mas comun en usuarios de MAC
#####
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
# Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
opts.add_argument("--disable-search-engine-choice-screen")

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(options=opts)

# Voy a la pagina que quiero
driver.get('https://www.olx.in/cars_c84')
sleep(4)

# Cerramos dialogo de disclaimer (2024)
try:
    disclaimer_boton = driver.find_element(By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
    disclaimer_boton.click()
except:
    pass

sleep(10)

#El formato de la página ha cambiado, ya no tenemos el botón "cargar mas"
#El nuevo formato es una lista de páginas con nuevos botones de "previous"; "next"; "1"; "2"; etc.
#Podemos hacer un for de tres iteraciones y dentro del for extraer la información necesaria
for i in range(3):
    try:
        print('\nPAGINA: ', i + 1, '\n\n')
        # Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
        # Esto es una LISTA. Por eso el metodo esta en plural
        # Esperar hasta que al menos un anuncio esté cargado antes de proceder
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-aut-id="itemBox2"]'))
        )
        autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox2"]')

        # Recorro cada uno de los anuncios que he encontrado
        for auto in autos:
            try:
                #print('Checkpoint2')
                # Por cada anuncio hallo el precio
                precio = driver.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
                print (precio)
                # Por cada anuncio hallo la descripcion
                # Cambiamos el xpath según el elemento de la nueva página para coger los "Item Details"
                descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemDetails"]').text
                print (descripcion)
            except Exception as e:
                print ('Anuncio carece de precio o descripcion')

        #Pasamos a la nueva página con el boton "Next"
        boton = driver.find_element(By.XPATH, '//a[@data-aut-id="arrowRight"]')
        boton.click()
        # espero que cargue la informacion dinamica
        sleep(random.uniform(10.0, 15.0))
    except Exception as e:
        print('Error en la iteración de páginas:')
        print(e)
        break

print('Final de la iteración sin errores')
