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

SECRET_KEY = 'supersecretkey'
DEBUG = True
APP_NAME = 'BACKOFFICE - TFM GRUPO C'
VERSION = 0