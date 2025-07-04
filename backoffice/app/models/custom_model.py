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
        # # # # # # """ ACCIONES ESPECIALES SEGÚN EL PARÁMETRO """


        # # # # # # if key == "ESTIMATED_ANNUAL_OCCUPANCY":
        # # # # # #     value = float(value) if value else 0
        # # # # # #     dias_ocupacion = round(value * 365 / 100 ,2)
        # # # # # #     query = "UPDATE HOUSES SET ARR = PRICE_PER_NIGHT * "+ str(dias_ocupacion) + " WHERE DISTRITO <> 'Not defined'"
        # # # # # #     result = db.run_query(query)

        # # # # # # if key == "PURCHASE_COST":
        # # # # # #     value = float(value) / 100 if value else 0
        # # # # # #     query = "UPDATE HOUSES SET PURCHASE_COST = PRICE * "+ str(value) + " WHERE DISTRITO <> 'Not defined'"
        # # # # # #     result = db.run_query(query)
        # # # # # #     query = "UPDATE HOUSES SET TOTAL_PURCHASE_COST = PRICE + PURCHASE_COST WHERE DISTRITO <> 'Not defined'"
        # # # # # #     result = db.run_query(query)



        return True
    return False

def recalculate_all():
    """ Recalcula todos los parámetros de la base de datos """
    db = DatabaseInterface()
    parameters = get_parameters_by_key()
    if not parameters:
        return False
    
    PURCHASE_COST = parameters.get("PURCHASE_COST", {}).get("VALUE", 0)
    ESTIMATED_ANNUAL_OCCUPANCY = parameters.get("ESTIMATED_ANNUAL_OCCUPANCY", {}).get("VALUE", 0)
    FIXED_OPEX = parameters.get("FIXED_OPEX", {}).get("VALUE", 0)
    VARIABLE_OPEX = parameters.get("VARIABLE_OPEX", {}).get("VALUE", 0)

    dias_ocupacion = round(float(ESTIMATED_ANNUAL_OCCUPANCY) * 365 / 100 ,0)
    query = "UPDATE HOUSES SET ARR = PRICE_PER_NIGHT * "+ str(dias_ocupacion) + " WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)

    PURCHASE_COST = float(PURCHASE_COST) / 100 if PURCHASE_COST else 0
    query = "UPDATE HOUSES SET PURCHASE_COST = PRICE * "+ str(PURCHASE_COST) + " WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)
    query = "UPDATE HOUSES SET TOTAL_PURCHASE_COST = PRICE + PURCHASE_COST WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)

    FIXED_OPEX = float(FIXED_OPEX) / 100 if FIXED_OPEX else 0
    query = "UPDATE HOUSES SET FIXED_OPEX = PRICE * "+ str(FIXED_OPEX) + " WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)

    VARIABLE_OPEX = float(VARIABLE_OPEX) / 100 if VARIABLE_OPEX else 0
    query = "UPDATE HOUSES SET VARIABLE_OPEX = ARR * "+ str(VARIABLE_OPEX) + " WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)

    query = "UPDATE HOUSES SET ROI = (ARR -  FIXED_OPEX - VARIABLE_OPEX) / TOTAL_PURCHASE_COST * 100 WHERE DISTRITO <> 'Not defined'"
    result = db.run_query(query)



    




