import requests as rq
from bs4 import BeautifulSoup
import datetime as dt
import re
import logging
from airflow.exceptions import AirflowFailException

import httpx
import asyncio

import credentials_db as cred
import pyodbc


conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={cred.server},{cred.port};'
    f'DATABASE={cred.database};'
    f'UID={cred.username};'
    f'PWD={cred.password};'
    f'TrustServerCertificate=yes;'
)

BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)


def insert_houses_db(house):
    #Insert the houses in the database
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO HOUSES (
            HOUSE_ID, TITLE, PRICE, ADDRESS1, ADDRESS2, CITY, ENERGY_CONSUME, ENERGY_EMISSION, PLANTA, SUPERFICIE, 
            HABITACIONES, BANOS, GARAJE, ESTADO, ARMARIOS_EMPOTRADOS, ANO, CALEFACCION, PISCINA, JARDIN, UPDATE_DATE, 
            URL, ZONA, MORE_INFO, ASCENSOR, MOVILIDAD_REDUCIDA, TRASTERO, TERRAZA, BALCON, AIRE_ACOND, ORIENTACION
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            house["house_id"], house["title"], house["price"], house["address_1"], house["address_2"], house["city"], 
            house["energy_consume"], house["energy_emission"], house["planta"], house["superficie"], 
            house["habitaciones"], house["baños"], house["garaje"], house["estado"], house["armarios_empotrados"], 
            house["año"], house["calefaccion"], house["piscina"], house["jardin"], house["update_date"], 
            house["url"], house["zona"], house["more_info"], house["ascensor"], house["movilidad_reducida"], 
            house["trastero"], house["terraza"], house["balcon"], house["aire_acond"], house["orientacion"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting houses in database: {e}")
        raise


def procces_features(features, house_detail):
    #Process the features of the house
    try:
        for feature in features:
            feature_lower = str.lower(feature)
            if "m²" in feature_lower:
                house_detail["superficie"] = feature
            elif "habitaciones" in feature_lower or "habitación" in feature_lower:
                house_detail["habitaciones"] = feature
            elif "baño" in feature_lower or "baños" in feature_lower:
                house_detail["baños"] = feature
            elif "planta" in feature_lower:
                house_detail["planta"] = feature
            elif "ascensor" in feature_lower:
                house_detail["ascensor"] = True
            elif "movilidad reducida" in feature_lower:
                house_detail["movilidad_reducida"] = True
            elif "trastero" in feature_lower:
                house_detail["trastero"] = True
            elif "calefacción" in feature_lower:
                house_detail["calefaccion"] = feature
            elif "segunda mano" in feature_lower:
                house_detail["estado"] = feature
            elif "obra nueva" in feature_lower:
                house_detail["estado"] = feature
            elif "piscina" in feature_lower:
                house_detail["piscina"] = True
            elif "jardín" in feature_lower:
                house_detail["jardin"] = True
            elif "garaje" in feature_lower:
                house_detail["garaje"] = True
            elif "terraza" in feature_lower:
                house_detail["terraza"] = True
            elif "balcón" in feature_lower:
                house_detail["balcon"] = True
            elif "construido" in feature_lower:
                house_detail["año"] = feature
            elif "aire acondicionado" in feature_lower:
                house_detail["aire_cond"] = True
            elif "orientación" in feature_lower:
                house_detail["orientacion"] = feature
            elif "armarios empotrados" in feature_lower:
                house_detail["armarios_empotrados"] = True
    except Exception as e:
        logging.error(f"Error processing features: {e}")


async def get_house_description(ids_houses, zone):
    #Get the description of the house
    for id_house in ids_houses:
        url = f"https://www.idealista.com/inmueble/{id_house}/"
        response = session.get(url)
        response = await response
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code} {url}")
            #If error we finish the process
            return False
        else:
            print(f"Success: {response.status_code}")
            soup = BeautifulSoup(response.content, "html.parser")

            house_detail = dict()
            house_detail["house_id"] = id_house
            house_detail["url"] = url
            house_detail["zona"] = zone

            #Generate all default values in the dictionary
            house_detail["title"] = None
            house_detail["price"] = 0.0
            house_detail["address_1"] = None
            house_detail["address_2"] = None
            house_detail["city"] = None
            house_detail["energy_consume"] = None
            house_detail["energy_emission"] = None
            house_detail["planta"] = None
            house_detail["superficie"] = None
            house_detail["habitaciones"] = None
            house_detail["baños"] = None
            house_detail["garaje"] = 0
            house_detail["estado"] = None
            house_detail["armarios_empotrados"] = 0
            house_detail["año"] = None
            house_detail["calefaccion"] = None
            house_detail["piscina"] = 0
            house_detail["jardin"] = 0
            house_detail["update_date"] = None
            house_detail["more_info"] = None
            house_detail["ascensor"] = 0
            house_detail["movilidad_reducida"] = "Not defined"
            house_detail["trastero"] = 0
            house_detail["terraza"] = 0
            house_detail["balcon"] = 0
            house_detail["aire_acond"] = 0
            house_detail["orientacion"] = None

            #Get the zone

            try:
                 house_detail["title"] = soup.find_all("span",class_="main-info__title-main").pop().text.strip()
            except:
                 logging.error(f"Error getting title {id_house}")
            
            #Price
            try:
                 price_html = soup.find_all("span",class_="info-data-price")
                 house_detail["price"] = int(price_html.pop().text.replace("€","").replace(".","").strip())
            except:
                 logging.error(f"Error getting price {id_house}")
           

            try:
                more_info_html = soup.find_all("div",class_="detail-info-tags")
                if more_info_html:
                    house_detail["more_info"] = more_info_html[0].find("span").text.strip()
            except:
                logging.error(f"Error getting more info {id_house}")

            #Location
            try:
                all_directions = soup.find_all("li",class_="header-map-list")
                if all_directions:
                    house_detail["address_1"] = all_directions[0].text.strip()
                    if len(all_directions) > 2:
                        house_detail["address_2"] = all_directions[1].text.strip()
                    house_detail["city"] = all_directions[-1].text.strip()
            except:
                logging.error(f"Error getting address {id_house}")


            #Get all the features
            features = []
            try:
                caracteristics_html = soup.find_all("div",class_="details-property-feature-one")
                if caracteristics_html:
                     property_features = caracteristics_html[0].find_all("li")
                     for prop_feature in property_features:
                         features.append(prop_feature.text.strip())
            except:
                logging.error(f"Error getting features {id_house}")


            try:
                equipment_html = soup.find_all("div",class_="details-property-feature-two")
                if equipment_html:
                    details_property_features = equipment_html[0].find_all("div",class_="details-property_features")
                    for prop_feature in details_property_features[0].find_all("li"):
                        features.append(prop_feature.text.strip())
                    if details_property_features[1]:
                        #Energy certification
                        details_property_features = details_property_features[1].find_all("li")
                        for prop_feature in details_property_features:
                            if "Consumo:" in prop_feature.text:
                                energy_class = prop_feature.find(class_=True)
                                house_detail["energy_consume"] = energy_class['class'][0]
                            elif "Emisiones:" in prop_feature.text:
                                energy_class = prop_feature.find(class_=True)
                                house_detail["energy_emission"] = energy_class['class'][0]
            except:
                logging.error(f"Error getting features {id_house}")

            procces_features(features,house_detail)

            #Update date
            try:
                house_detail["update_date"] = soup.find("p",class_="stats-text").text.strip()
            except:
                logging.error(f"Error getting update date {id_house}")

            #Insert the house in the database
            try:
                insert_houses_db(house_detail)
            except Exception as e:
                logging.error(f"Error inserting house {id_house} in database: {e}")
                #If error we finish the process
                return False      
    return True

async def houseLinks(zone:str, num_process:int,db_data_houses:set, text_filter_publicacion:str = ",publicado_ultimo-mes"):
    logging.info(f"Getting all houses from {zone} on idealista")
    initial_load = False
    filter_meters = [["menos","40"],
                        ["mas","40","menos","60"],
                        ["mas","60","menos","80"],
                        ["mas","80","menos","100"],
                        ["mas","100","menos","120"],
                        ["mas","120","menos","140"],
                        ["mas","140","menos","160"],
                        ["mas","160","menos","180"],
                        ["mas","180","menos","200"],
                        ["mas","200","menos","220"],
                        ["mas","220","menos","240"],
                        ["mas","240","menos","260"],
                        ["mas","260","menos","280"],
                        ["mas","280","menos","300"],
                        ["mas","300"]
                    ]
    
    #Load of all_houses from a Zone
    #Before scraping we have to get the number of total houses
    filter_met = filter_meters[num_process]
    text_filter_meter = f"con-metros-cuadrados-{filter_met[0]}-de_{filter_met[1]}"
    if len(filter_met) > 2:
        text_filter_meter += f",metros-cuadrados-{filter_met[2]}-de_{filter_met[3]}"
    url = f"https://www.idealista.com/venta-viviendas/{zone}-provincia/{text_filter_meter}{text_filter_publicacion}/?ordenado-por=fecha-publicacion-desc"
    response = session.get(url)
    response = await response
    if response.status_code != 200:
        logging.error(f"Error_00: {response.status_code} getting {url}")
        return False
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        num_houses = 0
        try:
            num_houses = soup.find("span", class_="breadcrumb-navigation-element-info").text
            num_houses = num_houses.split(" con tus criterios")[0]
            num_houses = int(re.sub(r'\D', '', num_houses))
        except:
            logging.error(f"Error getting number of houses {zone}")
        if num_houses > 0:
            #Get pagination
            max_page = (59 if num_houses > 1800 else num_houses // 30)
            for page in range(1, max_page + 2):
                text_page = f"pagina-{page}.htm"
                url = f"https://www.idealista.com/venta-viviendas/{zone}-provincia/{text_filter_meter}{text_filter_publicacion}/{text_page}?ordenado-por=fecha-publicacion-desc"
                response = session.get(url)
                response = await response
                if response.status_code != 200:
                    logging.error(f"Error_01: {response.status_code} getting {url}")
                    return False
                else:
                    soup = BeautifulSoup(response.content, "html.parser")
                    id_houses = set()
                    for ref in [a.get('data-element-id') for a in soup.find_all('article') if a.get('data-element-id') and a.get('data-online-booking')]:
                        id_houses.add(ref)
                    diff_id_houses = id_houses.difference(db_data_houses)
                    if len(diff_id_houses) > 0:
                        all_house_processes_status = False
                        all_house_processes_status = await get_house_description(diff_id_houses, zone)
                        if all_house_processes_status == False:
                            return False
            logging.info(f"Process {num_process} finished")
            logging.info(f"Number of houses processed: {num_houses}")
    #All the houses are processed fo process_number are processed
    return True

def get_all_db_houses():
    #Get all the houses from the database
    id_houses = set()
    logging.info("Getting all houses from database")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT HOUSE_ID FROM HOUSES")
        rows = cursor.fetchall()
        for row in rows:
            id_houses.add(row[0])
        cursor.close()
        conn.close()
        logging.info(f"Number of houses in database: {len(id_houses)}")
    except Exception as e:
        logging.error(f"Error getting all houses from database: {e}")
        raise AirflowFailException(f"Error getting all houses from database: {e}")
    return id_houses

def get_no_finished_processes():
    processed_set = set()
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT PROCESS_NUMBER FROM PROCESSES")
        processes = cursor.fetchall()
        for process in processes:
            processed_set.add(process[0])
        if len(processed_set ) == 0:
            #Insert all the processes
            #Number of processes is associated to the number of filters
            for i in range(0, 15):
                cursor.execute("INSERT INTO PROCESSES (PROCESS_NUMBER) VALUES (?)", (i,))
                conn.commit()
            processed_set = set(range(0, 15))
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error getting unantended processes: {e}")
        raise AirflowFailException(f"Error getting unantended processes: {e}")
        raise
    return processed_set


def delete_process(num_process):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES WHERE PROCESS_NUMBER = ?", (num_process,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error deleting process {num_process}: {e}")
        raise

async def run():
    #Fixed paramaters
    zone = "madrid"
    text_filter_publicacion = ",publicado_ultima-semana"
    
    db_data_houses = get_all_db_houses()
    no_finished_process = get_no_finished_processes()
    logging.info(f"Unattended processes: {no_finished_process}")
    for num_process in no_finished_process:
        status_process = False
        status_process = await houseLinks(zone, num_process,db_data_houses, text_filter_publicacion)
        if status_process == False:
            logging.error(f"Error in process {num_process}")
            break
        else:
            try:
                delete_process(num_process)
                logging.info(f"Process {num_process} deleted")
            except Exception as e:
                logging.error(f"Error deleting process {num_process}: {e}")
                break

if __name__ == "__main__":
    asyncio.run(run())