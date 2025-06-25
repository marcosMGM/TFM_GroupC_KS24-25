from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime
from collections import defaultdict

def get_home_cards():
    db = DatabaseInterface()
    card1 = db.getcountfromquery("SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined'")
    card3 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND CONVERT(date, CREATED_DATE) = '{datetime.datetime.now().date()}'")
    card4 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND CONVERT(date, UPDATED_DATE) = '{datetime.datetime.now().date()}'")
    card5 = db.getallfromquery("SELECT ISNULL(SUM(PRICE) / NULLIF(SUM(BUILT_AREA), 0), 0) AS precio_medio FROM HOUSES WHERE DISTRITO <> 'Not defined';")

    return {
        'card1': card1,
        'card2': 13250,  ### Lo pongo a cholón porque no tenemos aún tabla de AIRBNB, está en CSV
        'card3': card3,
        'card4': card4,
        'card5': round(float(card5[0].get('precio_medio', 0)),2),
    }

def get_pie_ide_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        BEDROOMS as bedrooms,
        COUNT(HOUSE_ID) as propiedades
        FROM HOUSES 
        WHERE DISTRITO <> 'Not defined'
        GROUP BY BEDROOMS
        ORDER BY BEDROOMS ASC
    """
    return db.getallfromquery(sql)

def get_pie_ide_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        BEDROOMS as bedrooms,
        COUNT(HOUSE_ID) as propiedades
        FROM HOUSES 
        WHERE DISTRITO <> 'Not defined'
        GROUP BY BEDROOMS
        ORDER BY BEDROOMS ASC
    """
    return db.getallfromquery(sql)

def get_sct1():
    db = DatabaseInterface()
    sql = """
    SELECT 
    CAST(BUILT_AREA AS FLOAT) AS x,
    CAST(PRICE AS FLOAT) AS y,
    '1' AS serie
    FROM HOUSES
    WHERE PRICE IS NOT NULL AND BUILT_AREA IS NOT NULL AND BUILT_AREA > 0 AND DISTRITO <> 'Not defined'

    UNION ALL

    SELECT 
    CAST(BEDROOMS AS FLOAT) AS x,
    CAST(PRICE   AS FLOAT) AS y,
    '2' AS serie
    FROM HOUSES
    WHERE 
    1=1 AND DISTRITO <> 'Not defined' 
    -- price IS NOT NULL AND bedrooms IS NOT NULL;
    """
    data = db.getallfromquery(sql)
 
    grouped = defaultdict(list)
    for item in data:
        grouped[item['serie']].append([item['x'], item['y']])

    return grouped

def get_map_markers():
    db = DatabaseInterface()
    sql = """
    SELECT 
        HOUSE_ID,
        LATITUDE,
        LONGITUDE,
        PRICE,
        BUILT_AREA,
        BEDROOMS,
        BATHROOMS,
        DISTRITO
    FROM HOUSES
    WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL AND DISTRITO <> 'Not defined'
    """
    data = db.getallfromquery(sql)
    
    markers = []
    for item in data:
        markers.append({
            'id': item['HOUSE_ID'],
            'lat': item['LATITUDE'],
            'lng': item['LONGITUDE'],
            'price': item['PRICE'],
            'built_area': item['BUILT_AREA'],
            'bedrooms': item['BEDROOMS'],
            'bathrooms': item['BATHROOMS'],
            'distrito': item['DISTRITO']
        })
    
    return markers