from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime

def get_home_cards():
    db = DatabaseInterface()
    card1 = db.getcountfromquery("SELECT id FROM ide_property")
    card3 = db.getcountfromquery(f"SELECT id FROM ide_property WHERE CONVERT(date, insert_date) = '{datetime.datetime.now().date()}'")
    card4 = db.getcountfromquery(f"SELECT id FROM ide_property WHERE CONVERT(date, update_date) = '{datetime.datetime.now().date()}'")

    return {
        'card1': card1,
        'card2': 0,  ### Lo pongo a cholón porque no tenemos aún tabla de AIRBNB, está en CSV
        'card3': card3,
        'card4': card4,
        'card5': 0,
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