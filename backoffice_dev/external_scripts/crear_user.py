from werkzeug.security import generate_password_hash
import os, sys
# # Con esto añado la ruta de la carpeta padre al path temporalmente para poder importar el módulo credenciales_sqlserver.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from credenciales_sqlserver import *
import pyodbc


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

def crear_usuario(login,password,nombre="",apellidos="",email=""):
    hashed_pw = generate_password_hash(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sys_user (login,password,nombre,apellidos,email) VALUES (?, ?, ?, ?, ?)", (login,hashed_pw,nombre,apellidos,email))
        conn.commit()
    print(f"✅ Insertado el usuario con login: {login}.")

crear_usuario("dasago", "dasago", "David", "Santamaría Gómez","david@dasago.es")


