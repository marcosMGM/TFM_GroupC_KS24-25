from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime
from collections import defaultdict
from app.models.idealista_model import get_percentile_roi
from app.models.custom_model import get_parameters_by_key
import json


def get_home_kpi():
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    group_roi = get_percentile_roi() # dict con keys P33, P66, P90

    card01 = db.getcountfromquery("SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0")
    card02 = db.getcountfromquery("SELECT DISTRITO FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 GROUP BY DISTRITO")
    card03 = db.getallfromquery("SELECT ISNULL(AVG(PRICE), 0) AS precio_promedio FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0")
    card03 = round(float(card03[0].get('precio_promedio', 0)), 2)

    houses_with_roi_gt_0 = db.getcountfromquery("SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND ROI > 0")
    card04 = round((houses_with_roi_gt_0 / card01 * 100) if card01 > 0 else 0, 2)

    card05 = db.getallfromquery("SELECT ISNULL(AVG(ROI), 0) AS promedio_roi FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0")
    card05 = round(float(card05[0].get('promedio_roi', 0)), 2)
    card06 = db.getallfromquery("SELECT ISNULL(AVG(NP), 0) AS promedio_np FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0")
    card06 = round(float(card06[0].get('promedio_np', 0)), 2)

    card11 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")
    card12 = db.getcountfromquery(f"SELECT DISTRITO FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0  AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)} GROUP BY DISTRITO")
    card13 = db.getallfromquery(f"SELECT ISNULL(AVG(PRICE), 0) AS precio_promedio FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0  AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")
    card13 = round(float(card13[0].get('precio_promedio', 0)), 2)

    houses_with_roi_gt_0 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND ROI > 0  AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")
    card14 = round((houses_with_roi_gt_0 / card11 * 100) if card11 > 0 else 0, 2)

    card15 = db.getallfromquery(f"SELECT ISNULL(AVG(ROI), 0) AS promedio_roi FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0  AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")
    card15 = round(float(card15[0].get('promedio_roi', 0)), 2)
    card16 = db.getallfromquery(f"SELECT ISNULL(AVG(NP), 0) AS promedio_np FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0  AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")
    card16 = round(float(card16[0].get('promedio_np', 0)), 2)



    # card2 = db.getcountfromquery(f"SELECT HOUSE_ID FROM HOUSES WHERE DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}")



    return {
        'card01': card01,
        'card02': card02, 
        'card03': card03,
        'card04': card04,
        'card05': card05,
        'card06': card06,
        'card11': card11,
        'card12': card12,
        'card13': card13,
        'card14': card14,
        'card15': card15,
        'card16': card16,
        
    }

def get_houses_by_distrito():
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    group_roi = get_percentile_roi() # dict con keys P33, P66,
    sql = f"""
    SELECT 
    DISTRITO,
    CASE 
            WHEN ROI <= 0 THEN 'No Rentable'
            WHEN ROI > 0 AND ROI <= {group_roi.get('P33')} THEN 'Baja'
            WHEN ROI > {group_roi.get('P33')} AND ROI <= {group_roi.get('P66')} THEN 'Media'
            WHEN ROI > {group_roi.get('P66')} AND ROI <= {group_roi.get('P90')} THEN 'Alta'
            WHEN ROI > {group_roi.get('P90')} THEN 'Excelente'
    END AS ROI_GROUP,
    COUNT(HOUSE_ID) AS PROPIEDADES


    FROM HOUSES 


    WHERE 
    DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0 AND ROI IS NOT NULL
    AND PRICE <= {parameters.get('MAX_INVESTMENT_BUDGET', dict).get('VALUE', 0)} AND ROI >= {parameters.get('INITIAL_MIN_ROI_DISPLAY_THRESOLD', dict).get('VALUE', -999)}

    GROUP BY DISTRITO, CASE 
            WHEN ROI <= 0 THEN 'No Rentable'
            WHEN ROI > 0 AND ROI <= {group_roi.get('P33')} THEN 'Baja'
            WHEN ROI > {group_roi.get('P33')} AND ROI <= {group_roi.get('P66')} THEN 'Media'
            WHEN ROI > {group_roi.get('P66')} AND ROI <= {group_roi.get('P90')} THEN 'Alta'
            WHEN ROI > {group_roi.get('P90')} THEN 'Excelente'
    END
    ORDER BY DISTRITO ASC;"""
    casas = db.getallfromquery(sql)

    roi_categories = ['No Rentable', 'Baja', 'Media', 'Alta', 'Excelente']
    color_map = {
        'No Rentable': '#FF5E40',
        'Baja': '#48443D',
        'Media': '#EBC33F',
        'Alta': '#4FC9DA',
        'Excelente': '#AECC34'
    }

    districts, seen = [], set()
    for item in casas:
        d = item['DISTRITO']
        if d not in seen:
            districts.append(d)
            seen.add(d)

    data_by_district = {d: {c: 0 for c in roi_categories} for d in districts}
    for item in casas:
        data_by_district[item['DISTRITO']][item['ROI_GROUP']] = item['PROPIEDADES']

    series = [
        {'name': cat, 'data': [data_by_district[d][cat] for d in districts]}
        for cat in roi_categories
    ]

    chart_dict = {
        'series': series,
        'categories': districts,
        'colors': [color_map[c] for c in roi_categories]
    }

    chart_data_json = json.dumps(chart_dict, ensure_ascii=False)
    return chart_data_json


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
    WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL AND DISTRITO <> 'Not defined' AND PROCESSED=2 AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
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