from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime


def get_pie_by_bedrooms():
    db = DatabaseInterface()
    sql = """
        SELECT 
        bedrooms,
        COUNT(id) as propiedades
        FROM ide_property 
        GROUP BY bedrooms
        ORDER BY bedrooms ASC
    """
    result = db.getallfromquery(sql)
    print(result)