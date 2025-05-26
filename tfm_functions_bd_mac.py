import pymssql
import credenciales_sqlserver as cred

def get_connection():
    """
    Establece una conexión a la base de datos SQL Server.
    """
    try:
        conn = pymssql.connect(
            server=cred.SERVER,
            port=cred.PORT,
            database=cred.DATABASE,
            user=cred.USERNAME,
            password=cred.PASSWORD
        )
        return conn
    except pymssql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def get_all_houses():
    """
    Obtiene todas las casas de la base de datos.
    :return: Lista de diccionarios con los datos de las casas.
    """
    query = "SELECT * FROM HOUSES"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    

def get_all_houses_id():
    """
    Obtiene todas las casas de la base de datos.
    :return: Lista de diccionarios con los datos de las casas.
    """
    query = "SELECT ID FROM HOUSES"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def get_all_houses_id_url():
    query = "SELECT HOUSE_ID,URL FROM HOUSES WHERE UPDATED_DATE IS NULL"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def update_latlong(house_id, lat, lon, district):
    """
    Actualiza la latitud y longitud de una casa en la base de datos.
    :param house_id: ID de la casa.
    :param lat: Latitud.
    :param lon: Longitud.
    """
    query = f"UPDATE HOUSES SET LATITUDE = {lat}, LONGITUDE = {lon}, DISTRICT = \'{district}\' UPDATED_DATE = getdate() WHERE ID = {house_id}"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (lat, lon, house_id))
        conn.commit()
    
