import pyodbc
from credenciales_sqlserver import *

connection_string = (
    # f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    # f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"DRIVER={{SQL Server}};"
    f"SERVER={SERVER},{PORT};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD}"
)

def get_connection():
    return pyodbc.connect(connection_string)

def insert_property(data: dict):
    """
    Inserta un nuevo registro en la tabla property.
    :param data: Diccionario con los campos y valores a insertar.
    """
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    values = tuple(data.values())

    query = f"INSERT INTO property ({keys}) VALUES ({placeholders})"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
