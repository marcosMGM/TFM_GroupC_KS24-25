from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime
from collections import defaultdict
from app.models.idealista_model import get_percentile_roi
from app.models.custom_model import get_parameters_by_key

def get_home_cards():
    db = DatabaseInterface()
    card1 = db.getcountfromquery("SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0")
    card3 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND CONVERT(date, CREATED_DATE) = '{datetime.datetime.now().date()}'")
    card4 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND CONVERT(date, UPDATED_DATE) = '{datetime.datetime.now().date()}'")
    card5 = db.getallfromquery("SELECT ISNULL(SUM(PRICE) / NULLIF(SUM(BUILT_AREA), 0), 0) AS precio_medio FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0;")

    return {
        'card1': card1,
        'card2': 13871,  ### Lo pongo a cholón porque no tenemos aún tabla de AIRBNB, está en CSV
        'card3': card3,
        'card4': card4,
        'card5': round(float(card5[0].get('precio_medio', 0)),2),
    }

def get_pie_ide_by_district():
    db = DatabaseInterface()
    sql = """
        SELECT 
        DISTRITO,
        COUNT(HOUSE_ID) as propiedades
        FROM HOUSES 
        WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
        GROUP BY DISTRITO
        ORDER BY DISTRITO ASC
    """
    return db.getallfromquery(sql)

def get_pie_ide_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        BEDROOMS as bedrooms,
        COUNT(HOUSE_ID) as propiedades
        FROM HOUSES 
        WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
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
    WHERE PRICE IS NOT NULL AND BUILT_AREA IS NOT NULL AND BUILT_AREA > 0 AND DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0

    UNION ALL

    SELECT 
    CAST(BEDROOMS AS FLOAT) AS x,
    CAST(PRICE   AS FLOAT) AS y,
    '2' AS serie
    FROM HOUSES
    WHERE 
    1=1 AND DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 
    -- price IS NOT NULL AND bedrooms IS NOT NULL;
    """
    data = db.getallfromquery(sql)
 
    grouped = defaultdict(list)
    for item in data:
        grouped[item['serie']].append([item['x'], item['y']])

    return grouped

def get_map_markers():
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    group_roi = get_percentile_roi() # dict con keys P33, P66, P90
    sql = f"""
    SELECT 
        HOUSE_ID,
        CASE 
        WHEN LEN(TITLE) > 50 THEN LEFT(TITLE,50) + '...'
        ELSE TITLE
        END AS TITLE,
        LATITUDE,
        LONGITUDE,
        PRICE,
        BUILT_AREA, BEDROOMS, BATHROOMS,
        DISTRITO,
        URL as link,
        PRICE_PER_NIGHT, NP, BED, ROI, 
        CASE 
            WHEN ROI <= 0 THEN 'No Rentable'
            WHEN ROI > 0 AND ROI <= { group_roi.get('P33') } THEN 'Baja'
            WHEN ROI > { group_roi.get('P33') } AND ROI <= { group_roi.get('P66') } THEN 'Media'
            WHEN ROI > { group_roi.get('P66') } AND ROI <= { group_roi.get('P90') } THEN 'Alta'
            WHEN ROI > { group_roi.get('P90') } THEN 'Excelente'
        END AS ROI_GROUP,
        CASE 
            WHEN ROI <= 0 THEN '#FF5E40'
            WHEN ROI > 0 AND ROI <= { group_roi.get('P33') } THEN '#48443D'
            WHEN ROI > { group_roi.get('P33') } AND ROI <= { group_roi.get('P66') } THEN '#EBC33F'
            WHEN ROI > { group_roi.get('P66') } AND ROI <= { group_roi.get('P90') } THEN '#4FC9DA'
            WHEN ROI > { group_roi.get('P90') } THEN '#AECC34'
        END AS ROI_COLOR

    FROM HOUSES
    WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL AND DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
    AND ROI >= {parameters.get("INITIAL_MIN_ROI_DISPLAY_THRESOLD", dict).get("VALUE", -999)}
    AND PRICE <= {parameters.get("MAX_INVESTMENT_BUDGET", dict).get("VALUE", 0)}
    
    """
    data = db.getallfromquery(sql)
    
    markers = []
    for item in data:
        markers.append({
            'id': item['HOUSE_ID'],
            'title': item['TITLE'],
            'lat': item['LATITUDE'],
            'lng': item['LONGITUDE'],
            'price': item['PRICE'],
            'built_area': item['BUILT_AREA'],
            'bedrooms': item['BEDROOMS'],
            'bathrooms': item['BATHROOMS'],
            'distrito': item['DISTRITO'],
            'price_per_night': item['PRICE_PER_NIGHT'],
            'np': item['NP'],
            'bed': item['BED'],
            'roi': item['ROI'],
            'roi_group': item['ROI_GROUP'],
            'roi_color': item['ROI_COLOR'],
            'link': item['link']
        })
    
    return markers