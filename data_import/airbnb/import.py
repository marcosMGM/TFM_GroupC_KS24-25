""" 
Importación de ficheros de AIRBNB. Preprocesado y cargado a la base de datos 

Obtenemos los datos desde https://insideairbnb.com/get-the-data/

Podríamos hacer scraping, obtener la fecha de la última actualización de Madrid y generar el enlace para descargarlo, pero no es necesario por que se actualiza cada mucho tiempo y no es necesario tener la última versión. Podemos cambiar la info procesable en la carpeta data manualmente.

"""
import os
import pandas as pd
import numpy as np
import datetime
from config_bd import *
import requests
import sys
import gzip
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TEMP_DIR = os.path.join(DATA_DIR, 'TEMP')


""" Comprobamos que existe el directorio de datos """

if not os.path.exists(DATA_DIR):
    print(f"El directorio {DATA_DIR} no existe. No es posible continuar...")
    sys.exit()

""" Descomprimimos el archivo de calendario """

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


gz_file_path = os.path.join(DATA_DIR, 'calendar.csv.gz')
output_file_path = os.path.join(TEMP_DIR, os.path.splitext(os.path.basename(gz_file_path))[0])

if os.path.exists(gz_file_path):
    try:
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Archivo {gz_file_path} descomprimido como {output_file_path}")
    except Exception as e:
        print(f"Error al descomprimir el archivo {gz_file_path}: {e}")
        sys.exit()
else:
    print(f"El archivo {gz_file_path} no existe. No es posible continuar...")
    sys.exit()








