import geopandas as gpd
from shapely.geometry import Point
import os

geojson_path = '/Users/jayarza/Developer/Master Data Science/TFM/Proyecto_Git/TFM_GroupC_KS24-25/data_import/airbnb/data/neighbourhoods.geojson'

def get_neighbourhood_group(latitude, longitude, geojson_path='neighbourhoods.geojson'):
    """
    Returns the neighbourhood_group for given latitude and longitude
    based on the provided GeoJSON file.
    """
    print(os.getcwd())
    geojson_path = os.path.join('TFM_GroupC_KS24-25/data_import/airbnb/data/neighbourhoods.geojson')
    print(geojson_path)
    if not os.path.exists(geojson_path):
        raise FileNotFoundError(f"GeoJSON file not found at {geojson_path}")
    gdf = gpd.read_file(geojson_path)
    point = Point(longitude, latitude)
    match = gdf[gdf.geometry.contains(point)]
    if not match.empty:
        return match.iloc[0]['neighbourhood_group']
    else:
        return None
