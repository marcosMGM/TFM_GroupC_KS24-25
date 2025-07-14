import geopandas as gpd
from shapely.geometry import Point
import os
from credenciales_sqlserver import GOOGLE_API_KEY
import requests
from geopy.distance import distance
import pandas as pd
from decimal import *

def get_neighbourhood_group(latitude, longitude, geojson_path='neighbourhoods.geojson'):
    """
    Returns the neighbourhood_group for given latitude and longitude
    based on the provided GeoJSON file.
    """

    project_root = os.getcwd()
    print(f"Path:{project_root}")
    
    geojson_path = os.path.abspath(os.path.join(project_root, "data_import/data/neighbourhoods.geojson"))
    if not os.path.exists(geojson_path):
        raise FileNotFoundError(f"GeoJSON file not found at {geojson_path}")
    gdf = gpd.read_file(geojson_path)
    point = Point(longitude, latitude)
    match = gdf[gdf.geometry.contains(point)]
    if not match.empty:
        return match.iloc[0]['neighbourhood_group']
    else:
        return None



def get_lat_long_from_address(address, city):
    """
    Returns the latitude and longitude for a given address and city using Google Maps Geocoding API.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    full_address = f"{address}, {city}"
    params = {
        "address": full_address,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None
    else:
        raise Exception(f"Error fetching data from Google API: {response.status_code}")
    
def get_df_rentas():
    df_rentas = pd.read_csv('../data_import/data/Datos_Rentas_Madrid_2022.csv',delimiter=";")
    
    for col in df_rentas.select_dtypes(include='float'):
        df_rentas[col] = df_rentas[col].apply(lambda x: x * 1000)

    df_rentas['Distrito'] = df_rentas['Distrito'].str[4:]
    df_rentas['Distrito'] = df_rentas['Distrito'].apply(lambda x: x.replace('-', ' - ') if '-' in x else x)
    #Bin of 5 
    df_rentas['renta_bin'] = pd.cut(
        df_rentas['Renta neta media por hogar'].sort_values(),
        bins=5,
        labels=['muy_bajo','bajo','medio','alto','muy_alto'],
        include_lowest=True
    )
    return df_rentas[['Distrito', 'Renta neta media por hogar', 'renta_bin']]

def get_renta_bin(distrito:str, df_rentas):
    # Busca el distrito en df_rentas y devuelve el valor de 'renta_bin'
    row = df_rentas[df_rentas['Distrito'] == distrito]
    if not row.empty:
        return row['renta_bin'].values[0]
    else:
        return None
    
TIPOS_TRANSPORTE = [4,5,6,8,10] #El 9 está integrado en el 8

def calcular_distancias_vivienda_transportes(latitude, longitude,stops):
    resultados = {}
    if isinstance(stops, pd.DataFrame):
        stops_pd = stops
    else:
        stops_pd = pd.DataFrame(stops)
        stops_pd.columns = ['id','mode','stop_name','stop_desc','lat', 'lon']
    for modo in TIPOS_TRANSPORTE:
        paradas_tipo = stops_pd[stops_pd['mode'] == modo]
        if paradas_tipo.empty:
            resultados[f'distancia_mode_{modo}'] = None
            continue
        # filtrar primero por lat/lon cercanas para acelerar
        delta = 0.01
        paradas_candidatas = paradas_tipo[
            (abs(paradas_tipo['lat'] - Decimal(latitude)) < delta) &
            (abs(paradas_tipo['lon'] - Decimal(longitude)) < delta)
        ]
        """ Para mejorar el rendimiento voy iterando incrementando el delta a comprobar, tengo que 
        asegurarme de que haya al menos una parada en el dataset porque sino morimos en el while"""
        while paradas_candidatas.empty:  
            delta += 0.01
            print(f"Buscando paradas cercanas al modo {modo} con delta {delta}")
            paradas_candidatas = paradas_tipo[
                (abs(paradas_tipo['lat'] - Decimal(latitude)) < delta) &
                (abs(paradas_tipo['lon'] - Decimal(longitude)) < delta)
            ]
      
        distancias = paradas_candidatas.apply(
            lambda stop: distance(
                (latitude, longitude),
                (stop['lat'], stop['lon'])
            ).meters,
            axis=1
        )

        resultados[f'distancia_mode_{modo}'] = distancias.min()

    return pd.Series(resultados)

 