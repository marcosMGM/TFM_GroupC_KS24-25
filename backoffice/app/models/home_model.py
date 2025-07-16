from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime
from collections import defaultdict
from app.models.custom_model import get_parameters_by_key

def get_oportunities():
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    order_by = parameters.get("RECOMMEND_BY", dict).get("VALUE", "ROI")
    if order_by == "ROI" or order_by == "NP":
        order_by = order_by
    else:
        order_by = "ROI"

    sql = f"""
        SELECT 
        TOP 12
            HOUSE_ID,
            CASE 
                WHEN LEN(TITLE) > 50 THEN LEFT(TITLE,50) + '...'
                ELSE TITLE
            END AS TITLE,
            PRICE,
            BUILT_AREA,
            BEDROOMS,
            BATHROOMS,
            DISTRITO,
            ROUND(ROI,1) AS ROI,
            NP,
            BED
        FROM HOUSES
        WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
        AND ROI > 0 AND ROI >= {parameters.get("INITIAL_MIN_ROI_DISPLAY_THRESOLD",dict).get("VALUE",-999)}
         AND PRICE <= {parameters.get("MAX_INVESTMENT_BUDGET",dict).get("VALUE",0)}
        ORDER BY {order_by} DESC

    """
    return db.getallfromquery(sql)

def get_improvable_oportunities():
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    order_by = parameters.get("RECOMMEND_BY", dict).get("VALUE", "ROI")
    if order_by == "ROI" or order_by == "NP":
        order_by = order_by
    else:
        order_by = "ROI"
    sql = f"""
        SELECT 
        TOP 6
            HOUSE_ID,
            CASE 
                WHEN LEN(TITLE) > 50 THEN LEFT(TITLE,50) + '...'
                ELSE TITLE
            END AS TITLE,
            PRICE,
            BUILT_AREA,
            BEDROOMS,
            BATHROOMS,
            DISTRITO,
            ROUND(ROI,1) AS ROI,
            NP,
            BED
        FROM HOUSES
        WHERE DISTRITO <> 'Not defined' AND PRICE_PER_NIGHT IS NOT NULL AND PRICE_PER_NIGHT > 0
        AND ROI > 0 AND ROI >= {parameters.get("INITIAL_MIN_ROI_DISPLAY_THRESOLD",dict).get("VALUE",-999)}
         AND PRICE >= {parameters.get("MAX_INVESTMENT_BUDGET",dict).get("VALUE",0)} 
        ORDER BY {order_by} DESC

    """
    return db.getallfromquery(sql)
