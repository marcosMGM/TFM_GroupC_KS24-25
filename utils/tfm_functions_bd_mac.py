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
    query = "SELECT HOUSE_ID FROM HOUSES"
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
    
def get_all_houses_id_address():
    query = "SELECT HOUSE_ID, ADDRESS1, ADDRESS2, CITY FROM HOUSES WHERE UPDATED_DATE IS NULL"
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
    query = "UPDATE HOUSES SET LATITUDE = %s, LONGITUDE = %s, DISTRITO = %s, UPDATED_DATE = getdate() WHERE HOUSE_ID = %s"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (lat, lon, district, house_id))
        conn.commit()

def insert_houses_db(house):
    #Insert the houses in the database
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO HOUSES (
            HOUSE_ID, TITLE, PRICE, ADDRESS1, ADDRESS2, CITY, ENERGY_CONSUME, ENERGY_EMISSION, PLANTA, SUPERFICIE, 
            HABITACIONES, BANOS, GARAJE, ESTADO, ARMARIOS_EMPOTRADOS, ANO, CALEFACCION, PISCINA, JARDIN, UPDATE_DATE, 
            URL, ZONA, MORE_INFO, ASCENSOR, MOVILIDAD_REDUCIDA, TRASTERO, TERRAZA, BALCON, AIRE_ACOND, ORIENTACION, CREATED_DATE,
            UPDATED_DATE,LATITUDE, LONGITUDE, DISTRITO, DISTANCE_TO_METRO, DISTANCE_TO_CERCANIAS, DISTANCE_TO_EMT, DISTANCE_TO_INTERURBANOS, DISTANCE_TO_MLO
        ) VALUES (
            %(house_id)s, %(title)s, %(price)s, %(address_1)s, %(address_2)s, %(city)s, %(energy_consume)s, 
            %(energy_emission)s, %(planta)s, %(superficie)s, %(habitaciones)s, %(baños)s, %(garaje)s, %(estado)s, 
            %(armarios_empotrados)s, %(año)s, %(calefaccion)s, %(piscina)s, %(jardin)s, %(update_date)s, 
            %(url)s, %(zona)s, %(more_info)s, %(ascensor)s, %(movilidad_reducida)s, %(trastero)s, %(terraza)s, 
            %(balcon)s, %(aire_acond)s, %(orientacion)s, getdate(), getdate(), %(latitude)s, %(longitude)s, %(distrito)s, %(distance_to_metro)s, %(distance_to_cercanias)s,
            %(distance_to_emt)s, %(distance_to_interurbanos)s, %(distance_to_mlo)s
        )
        """, house)
        conn.commit()


def get_proccessed_numbers():
    query = "SELECT PROCESS_NUMBER FROM PROCESSES"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
def insert_process_number(process_number):
    query = "INSERT INTO PROCESSES (PROCESS_NUMBER) VALUES (%s)"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (process_number,))
        conn.commit()

def get_all_transports():
    query = "SELECT * FROM TRANSPORTS"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def update_processed_with_distrito_not_defined():
    """
    Actualiza el processed a 1, para que se consideren por no tener distrito
    """
    query = "UPDATE HOUSES SET PROCESSED=1, UPDATED_DATE = getdate() WHERE DISTRITO = 'Not defined' and PROCESSED=0"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def update_predicted_price(house_id, price):
    query = f"UPDATE HOUSES SET PROCESSED=2, PRICE_PER_NIGHT={price} WHERE HOUSE_ID={house_id} AND PROCESSED = 0"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()