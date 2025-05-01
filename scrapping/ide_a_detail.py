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
ENLACE_INI = "https://www.idealista.com/inmueble/102146350/"

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
    time.sleep(random.randint(1, 2))
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
time.sleep(random.randint(2, 4))




""" Trabajo con el contenido de la página """
html = browser.page_source
soup = bs(html, 'html.parser')

full_detail = soup.find('section', {'class': 'detail-content-wrapper'})
if full_detail:
    titulo = full_detail.find('span', {'class': 'main-info__title-main'}).text.strip()
    ubicacion = full_detail.find('span', {'class': 'main-info__title-minor'}).text.strip()
    precio  = float(full_detail.find('span', {'class': 'info-data-price'}).find('span',{'class':'txt-bold'}).text.strip().replace('.','').replace('€','').replace(',','.'))
    etiquetas_html = full_detail.find('div', {'class': 'detail-info-tags'})
    etiquetas_final =""
    if etiquetas_html:
        etiquetas = etiquetas_html.find_all('span', class_='tag')
        etiquetas_final = " | ".join([etiqueta.text.strip() for etiqueta in etiquetas])
    commentario = full_detail.find('div', {'class': 'comment'}).find('div', {'class': 'adCommentsLanguage'}).find('p').text.strip() 
    comentario = "" if not commentario else commentario


""" Trabajo con el bloque de detalles """
detalles = soup.find('section', {'class': 'details-box'}).find('div', {'class': 'details-property'})

built_area = 0
usable_area = 0
bedrooms = 0
bathrooms = 0
garages = 0
origin = ''
status = ''
builtin_wardrobes = 0
orientation = ''
heating = ''
pmr_adapted = 0
floor = ""
lift = 0
air_conditioning = 0
pool = 0




if detalles:
    div_features_one = detalles.find('div', {'class': 'details-property-feature-one'})
    for li in div_features_one.find_all('li'):
        if 'habitaciones' in li.text.strip().lower():
            habitaciones = li.find('span', {'class': 'value'}).text.strip()
   




""" Trabajo con el mapa """
mapa = soup.find('div', {'class': 'static-map-container'})
map_img = mapa.find('img', id='sMap') if mapa else None
map_image_link = map_img.get('src') if map_img else ''
lat, lon = 0,0
if map_image_link and len(map_image_link) > 10:
    parsed_url = urlparse(map_image_link)
    params = parse_qs(parsed_url.query)
    center = params.get('center', [''])[0]
    if "," in center:
        lat, lon, *rest = center.split(",") #no creo que vengas más "," pero por si acaso
lat, lon = float(lat), float(lon)

            
   



""" Pruebas de lo que estamos haciendo """
print(titulo)
print(ubicacion)
print(precio)
print(lat, lon)
print(etiquetas_final)
# print(commentario)

