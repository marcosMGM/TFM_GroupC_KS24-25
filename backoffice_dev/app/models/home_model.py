from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime
from collections import defaultdict

def get_home_cards():
    db = DatabaseInterface()
    card1 = db.getcountfromquery("SELECT id FROM ide_property")
    card3 = db.getcountfromquery(f"SELECT id FROM ide_property WHERE CONVERT(date, insert_date) = '{datetime.datetime.now().date()}'")
    card4 = db.getcountfromquery(f"SELECT id FROM ide_property WHERE CONVERT(date, update_date) = '{datetime.datetime.now().date()}'")
    card5 = db.getallfromquery("SELECT SUM(price) / SUM(built_area) as precio_medio FROM ide_property")

    return {
        'card1': card1,
        'card2': 0,  ### Lo pongo a cholón porque no tenemos aún tabla de AIRBNB, está en CSV
        'card3': card3,
        'card4': card4,
        'card5': round(float(card5[0].get('precio_medio', 0)),2),
    }

def get_pie_ide_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        bedrooms,
        COUNT(id) as propiedades
        FROM ide_property 
        GROUP BY bedrooms
        ORDER BY bedrooms ASC
    """
    return db.getallfromquery(sql)

def get_pie_ide_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        bedrooms,
        COUNT(id) as propiedades
        FROM ide_property 
        GROUP BY bedrooms
        ORDER BY bedrooms ASC
    """
    return db.getallfromquery(sql)

def get_sct1():
    db = DatabaseInterface()
    sql = """
    SELECT 
    CAST(built_area AS FLOAT) AS x,
    CAST(price AS FLOAT) AS y,
    '1' AS serie
    FROM ide_property
    WHERE price IS NOT NULL AND built_area IS NOT NULL

    UNION ALL

    SELECT 
    CAST(bedrooms AS FLOAT) AS x,
    CAST(price AS FLOAT) AS y,
    '2' AS serie
    FROM ide_property
    WHERE 
    1=1
    -- price IS NOT NULL AND bedrooms IS NOT NULL;
    """
    data = db.getallfromquery(sql)
 
    grouped = defaultdict(list)
    for item in data:
        grouped[item['serie']].append([item['x'], item['y']])

    return grouped