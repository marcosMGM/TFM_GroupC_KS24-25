import geopandas as gpd
from shapely.geometry import Point
import os
from credenciales_sqlserver import GOOGLE_API_KEY
import requests


def get_neighbourhood_group(latitude, longitude, geojson_path='neighbourhoods.geojson'):
    """
    Returns the neighbourhood_group for given latitude and longitude
    based on the provided GeoJSON file.
    """
    geojson_path = os.path.join('TFM_GroupC_KS24-25/data_import/airbnb/data/neighbourhoods.geojson')
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