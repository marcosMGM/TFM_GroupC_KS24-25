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
from urllib.parse import urlparse, parse_qs

ENLACE_INI = "https://www.idealista.com/inmueble/100000581/"

browser = uc.Chrome()

browser.get(ENLACE_INI)
time.sleep(random.randint(4, 12))



""" Acepto las cookies """
try:
    browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
except:
    pass



""" Hago scroll hacia abajo del todo para que cargue todo (imagen del mapa) """
# time.sleep(random.randint(2, 4))
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(2, 4))
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height




""" Trabajo con el contenido de la página """
html = browser.page_source
soup = bs(html, 'html.parser')

full_detail = soup.find('section', {'class': 'detail-content-wrapper'})

if full_detail:
    titulo = full_detail.find('span', {'class': 'main-info__title-main'}).text.strip()
    ubicacion = full_detail.find('span', {'class': 'main-info__title-minor'}).text.strip()
    precio  = float(full_detail.find('span', {'class': 'info-data-price'}).find('span',{'class':'txt-bold'}).text.strip().replace('.','').replace('€','').replace(',','.'))

    """ idealista no carga la img hasta que el usuario hace scroll. Imagino que para ahorra costes de google maps."""
    mapa = soup.find('div', {'class': 'static-map-container'})
    map_img = mapa.find('img', id='sMap') if mapa else None
    map_image_link = map_img.get('src') if map_img else ''

    if map_image_link and len(map_image_link) > 10:
        parsed_url = urlparse(map_image_link)
        params = parse_qs(parsed_url.query)
        center = params.get('center', [''])[0]

   
    print(titulo)
    print(ubicacion)
    print(precio)
    print(map_image_link)
    print(center)

else:
    print(f"No se ha podido carga el detalle del inmueble {ENLACE_INI}")
    
