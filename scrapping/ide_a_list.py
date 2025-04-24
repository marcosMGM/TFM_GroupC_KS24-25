from config_bd import get_connection, insert_ide_property
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


# ENLACE_INICIAL_LISTADO ="https://www.idealista.com/venta-viviendas/mostoles-madrid/con-sin-inquilinos/"
ENLACE_INICIAL_LISTADO ="https://www.idealista.com/venta-viviendas/oropesa-del-mar-castellon/con-sin-inquilinos/"
URL_INMUEBLE = "https://www.idealista.com/inmueble/%INMUEBLE_ID%/"
browser = uc.Chrome()

paginacion = 1
ids = []
resultados = []
while True:
# while paginacion == 1: ## fuerzo para recoger solo una página
    print('Página: ', paginacion)
    url = f'{ENLACE_INICIAL_LISTADO}{"pagina-" + str(paginacion) + ".htm" if paginacion > 1 else ""}'
    browser.get(url)
    time.sleep(random.randint(10, 28))

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
        precio_text = price_tag.get_text(strip=True) if price_tag else '0'
        try:
            precio = round(float(precio_text.replace('€', '').replace('.','').replace(',', '.').strip()), 2)
        except ValueError:
            precio = 0.0

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
        insert_ide_property({
            'id' : element_id,
            'update_date' : datetime.datetime.now(),
            'link' : enlace,
            'title' : titulo,
            'price' : precio,
            'description' : descripcion,
            'label' : etiquetas,
            # 'built_area' : '',
            # 'usable_area' : '',
            # 'bedrooms' : '',
            # 'bathrooms' : '',
            # 'has_terrace' : '',
            # 'garage_included' : '',
            # 'property_condition' : '',
            # 'heating_type' : '',
            # 'adapted_access' : '',
            # 'floor_number' : '',
            # 'is_exterior' : '',
            # 'has_elevator' : '',
            # 'has_air_conditioning' : '',
            # 'energy_consumption_kwh' : '',
            # 'energy_consumption_class' : '',
            # 'co2_emissions_kg' : '',
            # 'co2_emissions_class' : ''
        })

