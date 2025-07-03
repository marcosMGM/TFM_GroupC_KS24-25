from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime


def get_parameters_by_key():
    """ Obtiene todos los parámetros que tenemos almacenados en la base de datos """
    db = DatabaseInterface()
    query = "SELECT PARAMETER_ID, NAME, VALUE, TYPE, MODE, SORT_ORDER, DESCRIPTION FROM PARAMETERS ORDER BY TYPE ASC, SORT_ORDER ASC"
    result = db.getallfromquery(query)
    if result:
        param_dict = {}
        for row in result:
            param_dict[row['NAME']] = dict(row)
        return param_dict
    return None

def get_parameters():
    """ Obtiene todos los parámetros que tenemos almacenados en la base de datos """
    db = DatabaseInterface()
    query = "SELECT PARAMETER_ID, NAME, VALUE, TYPE, MODE, SORT_ORDER, DESCRIPTION FROM PARAMETERS ORDER BY TYPE ASC, SORT_ORDER ASC"
    result = db.getallfromquery(query)
    if result:
        return result
    return None

def update_by_key(key, value=""):
    if not key:
        return False
    db = DatabaseInterface()
    update = {
        'NAME': key,
        'VALUE': value,
        'UPDATED_DATE': datetime.datetime.now()
    }
    result = db.update('PARAMETERS', update, f"NAME = '{key}'")
    if result:
        return True
    return False


