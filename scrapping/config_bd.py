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

# def insert_property(data: dict):
#     """
#     Inserta un nuevo registro en la tabla property.
#     :param data: Diccionario con los campos y valores a insertar.
#     """
#     keys = ", ".join(data.keys())
#     placeholders = ", ".join(["?" for _ in data])
#     values = tuple(data.values())

#     query = f"INSERT INTO property ({keys}) VALUES ({placeholders})"
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(query, values)
#         conn.commit()

def insert_property(data: dict):
    """
    Inserta un nuevo registro en la tabla property, actualiza ya existente.
    :param data: Diccionario con los campos y valores a insertar.
    """
    keys = list(data.keys())
    values = tuple(data.values())

    set_clause = ", ".join([f"target.{k} = source.{k}" for k in keys if k != "id"])
    columns = ", ".join(keys)
    placeholders = ", ".join(["?" for _ in keys])
    source_alias = ", ".join([f"? AS {k}" for k in keys])

    query = f"""
    MERGE INTO property AS target
    USING (SELECT {source_alias}) AS source
    ON target.id = source.id
    WHEN MATCHED THEN
        UPDATE SET {set_clause}
    WHEN NOT MATCHED THEN
        INSERT ({columns})
        VALUES ({placeholders});
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, values * 2)
        conn.commit()
