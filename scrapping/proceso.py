from config_bd import get_connection, add_house
import pandas as pd
import numpy as np
import datetime
import os
import requests
from bs4 import BeautifulSoup as bs
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


# for i in range(1, 15001):
#     add_house({
#         "id": i,
#         "address": "Calle Falsa "+str(i),
#         "price": 250000,
#         "bedroom": 3,
#         "bathroom": 2
#     })


ENLACE_INICIAL_LISTADO ="https://www.idealista.com/venta-viviendas/mostoles-madrid/con-sin-inquilinos/"
URL_INMUEBLE = "https://www.idealista.com/inmueble/%INMUEBLE_ID%/"
browser = uc.Chrome()

paginacion = 1
ids = []
resultados = []
# while True:
while paginacion == 1:
    print('Página: ', paginacion)
    url = f'{ENLACE_INICIAL_LISTADO}{"pagina-" + str(paginacion) + ".htm" if paginacion > 1 else ""}'
    browser.get(url)
    time.sleep(random.randint(8, 12))

    # Trata de marcar el sí en la información de cookies
    try:
        browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass

    html = browser.page_source
    soup = bs(html, 'html.parser')

    pagina_actual = int(soup.find('main', {'class': 'listing-items'}).find('div', {'class': 'pagination'}).find('li', {'class': 'selected'}).text)
    if paginacion == pagina_actual:
        # articles = soup.find('main', {'class': 'listing-items'}).find_all('article')
        articles = soup.find('main', {'class': 'listing-items'}).find_all('article', attrs={'data-element-id': True})
    else:
        break

    paginacion += 1


for article in articles:
    # ID del artículo
    element_id = article.get('data-element-id')

    # Enlace y título
    link_tag = article.find('a', class_='item-link')
    enlace = link_tag.get('href') if link_tag else ''
    titulo = link_tag.get('title') if link_tag else ''

    # Precio
    price_tag = article.find('span', class_='item-price')
    precio = price_tag.get_text(strip=True) if price_tag else ''

    # Detalles (habitaciones, m2, planta...)
    detalles_tags = article.find_all('span', class_='item-detail')
    detalles = ' | '.join([d.get_text(strip=True) for d in detalles_tags])

    # Descripción
    desc_tag = article.find('div', class_='item-description')
    descripcion = desc_tag.get_text(strip=True) if desc_tag else ''

    # Etiquetas (ej: Vistas al mar)
    tag_container = article.find('div', class_='listing-tags-container')
    etiquetas = ''
    if tag_container:
        etiquetas = ' | '.join([
            tag.get_text(strip=True) for tag in tag_container.find_all('span', class_='listing-tags')
        ])

    # Diccionario final para este artículo
    # datos = {
    #     'id': element_id,
    #     'enlace': enlace,
    #     'titulo': titulo,
    #     'precio': precio,
    #     'detalles': detalles,
    #     'descripcion': descripcion,
    #     'etiquetas': etiquetas
    # }

    add_house({
        "id": element_id,
        "link": enlace,
        "title": titulo,
        "address": "Calle Falsa "+str(i),
        "price": precio,
        "bedroom": 3,
        "bathroom": 2
    })

    resultados.append(datos)
print(resultados)
