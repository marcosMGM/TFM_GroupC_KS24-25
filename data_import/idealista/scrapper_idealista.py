import requests as rq
from bs4 import BeautifulSoup
import datetime as dt
import re

import httpx
import asyncio
import pymssql


import sys
import os

project_root = os.getcwd()
print(f"Path:{project_root}")
base_dir = os.path.abspath(os.path.join(project_root, "../..")) #Should be the root directory of the project
print(f"Base***:{base_dir}")

#for debug we add also project_root


# Add to sys.path if not already added
if base_dir not in sys.path:
    sys.path.append(base_dir)
print(sys.path)

#for debug we add also project_root
if project_root not in sys.path:
    sys.path.append(project_root)
print(sys.path)

from urllib.parse import urlparse, parse_qs
from utils.tfm_auxiliar_functions import *
from utils.tfm_functions_bd_mac import *
from utils.fetcher_chrome import *



BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)



def procces_features(features, house_detail):
    #Process the features of the house
    try:
        for feature in features:
            feature_lower = str.lower(feature)
            if "m² construidos" in feature_lower:
                house_detail["superficie"] = feature
            elif "Parcela" in feature_lower and house_detail["superficie"] is not None:
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
        print(f"Error processing features: {e}")


async def get_house_description(ids_houses, zone, all_transports):
    #Get the description of the house
    max_fails = 0
    for id_house in ids_houses:
        url = f"https://www.idealista.com/inmueble/{id_house}/"
        response = fetch_page(url)
        if not response:
            print(f"Scapper error getting {url}")
            #We are going to stop the process when we have more than 5 errors
            max_fails += 1
            if max_fails > 6:
                print(f"Scapper max error getted. Ending the process...")
                return False
        else:
            print(f"Success: Processing {url}")
            soup = response#BeautifulSoup(response.content, "html.parser")

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
            house_detail["latitude"] = None
            house_detail["longitude"] = None
            house_detail["distrito"] = "Not defined"

            #Get the zone

            try:
                 house_detail["title"] = soup.find_all("span",class_="main-info__title-main").pop().text.strip()
            except:
                 print(f"Error getting title {id_house}")
            
            #Price
            try:
                 price_html = soup.find_all("span",class_="info-data-price")
                 house_detail["price"] = int(price_html.pop().text.replace("€","").replace(".","").strip())
            except:
                 print(f"Error getting price {id_house}")
           

            try:
                more_info_html = soup.find_all("div",class_="detail-info-tags")
                if more_info_html:
                    house_detail["more_info"] = more_info_html[0].find("span").text.strip()
            except:
                print(f"Error getting more info {id_house}")

            #Location
            try:
                all_directions = soup.find_all("li",class_="header-map-list")
                if all_directions:
                    house_detail["address_1"] = all_directions[0].text.strip()
                    if len(all_directions) > 2:
                        house_detail["address_2"] = all_directions[1].text.strip()
                    house_detail["city"] = all_directions[-1].text.strip()
            except:
                print(f"Error getting address {id_house}")


            #Get all the features
            features = []
            try:
                caracteristics_html = soup.find_all("div",class_="details-property-feature-one")
                if caracteristics_html:
                     property_features = caracteristics_html[0].find_all("li")
                     for prop_feature in property_features:
                         features.append(prop_feature.text.strip())
            except:
                print(f"Error getting features {id_house}")


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
                print(f"Error getting features {id_house}")

            procces_features(features,house_detail)

            #Update date
            try:
                house_detail["update_date"] = soup.find("p",class_="stats-text").text.strip()
            except:
                print(f"Error getting update date {id_house}")
            
            #Get the latitude, longitude and distrito using the Google Maps API
            address = f"{house_detail['address_1']}, {house_detail['address_2']}"
            lat, lng = get_lat_long_from_address(address, house_detail['city'])
            if lat is None or lng is None:
                lat, lng = 0, 0
            house_detail["latitude"] = lat
            house_detail["longitude"] = lng
            district = "Not defined"
            if lat != 0 or lng != 0:
                district = get_neighbourhood_group(lat, lng)
                if district == None:
                    district = "Not defined"
            house_detail["distrito"] = district

            #Get distances to different transports
            dict_dist_stops = calcular_distancias_vivienda_transportes( lat, lng, all_transports )
            house_detail["distance_to_metro"] = dict_dist_stops["distancia_mode_4"]
            house_detail["distance_to_cercanias"] = dict_dist_stops["distancia_mode_5"]
            house_detail["distance_to_emt"] = dict_dist_stops["distancia_mode_6"]
            house_detail["distance_to_interurbanos"] = dict_dist_stops["distancia_mode_8"]
            house_detail["distance_to_mlo"] = dict_dist_stops["distancia_mode_10"]

            #Insert the house in the database
            try:
                insert_houses_db(house_detail)
            except Exception as e:
                print(f"Error inserting house {id_house} in database: {e}")
                #If error we finish the process
                return False      
    return True

async def houseLinks(zone:str, num_process:int,db_data_houses:set, text_filter_publicacion:str = ",publicado_ultimo-mes", all_transports = []):
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
        print(f"Error_00: {response.status_code} getting {url}")
        return False
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        num_houses = 0
        try:
            num_houses = soup.find("span", class_="breadcrumb-navigation-element-info").text
            num_houses = num_houses.split(" con tus criterios")[0]
            num_houses = int(re.sub(r'\D', '', num_houses))
        except:
            print(f"Error getting number of houses {zone}")
        if num_houses > 0:
            #Get pagination
            max_page = (59 if num_houses > 1800 else num_houses // 30)
            for page in range(1, max_page + 2):
                text_page = f"pagina-{page}.htm"
                url = f"https://www.idealista.com/venta-viviendas/{zone}-provincia/{text_filter_meter}{text_filter_publicacion}/{text_page}?ordenado-por=fecha-publicacion-desc"
                response = session.get(url)
                response = await response
                if response.status_code != 200:
                    print(f"Error_01: {response.status_code} getting {url}")
                    return False
                else:
                    soup = BeautifulSoup(response.content, "html.parser")
                    id_houses = set()
                    for ref in [a.get('data-element-id') for a in soup.find_all('article') if a.get('data-element-id') and a.get('data-online-booking')]:
                        id_houses.add(ref)
                    #TODO: Check if the house has changed the prices to consider ot not it again
                    # Now, if not condiring this, only if already exists in the database
                    diff_id_houses = id_houses.difference(db_data_houses)
                    if len(diff_id_houses) > 0:
                        all_house_processes_status = False
                        all_house_processes_status = await get_house_description(diff_id_houses, zone, all_transports)
                        if all_house_processes_status == False:
                            return False
            print(f"Process {num_process} finished")
            print(f"Number of houses processed: {num_houses}")
    #All the houses are processed fo process_number are processed
    return True

def get_all_db_houses():
    #Get all the houses from the database
    id_houses = set()
    print("Getting all houses from database")
    try:     
        rows = get_all_houses_id()
        for row in rows:
            id_houses.add(row[0])
        print(f"Number of houses in database: {len(id_houses)}")
    except Exception as e:
        print(f"Error getting all houses from database: {e}")
        raise
    return id_houses


def get_no_finished_processes():
    processed_set = set()
    try:        
        processes = get_proccessed_numbers()
        for process in processes:
            processed_set.add(process[0])
        if len(processed_set ) == 0:
            #Insert all the processes
            #Number of processes is associated to the number of filters
            for i in range(0, 15):
                insert_process_number(i)
            processed_set = set(range(0, 15))
    except Exception as e:
        print(f"Error getting unantended processes: {e}")
        raise
    return processed_set


def delete_process(num_process):
    try:
        conn = pymssql.connect(
            server=cred.server,
            port=cred.port,
            database=cred.database,
            user=cred.username,
            password=cred.password
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES WHERE PROCESS_NUMBER = %s", (num_process,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting process {num_process}: {e}")
        raise


async def update_inf_latlong_dist():
    """
    Update the new information in the database.
    This function is not used in this script, but it is useful for future updates.
    """
    #Get all the houses from the database with its like
    rows = get_all_houses_id_address()
    houses_latlong = dict()
    for row in rows:
        address = f"{row[1]}, {row[2]}"
        lat, lng = get_lat_long_from_address(address, row[3])
        if lat is None or lng is None:
            lat, lng = 0, 0
        houses_latlong[row[0]] = (lat, lng)

    print(f"Number of houses with latitude and longitude: {len(houses_latlong)}")
    return houses_latlong


def update_db_latlong_dist(houses_latlong):
    """
    Update the latitude and longitude in the database.
    This function is not used in this script, but it is useful for future updates.
    """
    try:
        for house_id, (lat, lon) in houses_latlong.items():
            district = "Not defined"
            if lat != 0 or lon != 0:
                district = get_neighbourhood_group(lat, lon)
                if district == None:
                    district = "Not defined"
            update_latlong(house_id, lat, lon, district)
    except Exception as e:
        print(f"Error updating latitude and longitude in database: {e}")
        raise


async def run():
    #Fixed paramaters
    zone = "madrid"
    text_filter_publicacion = ",publicado_ultima-semana"
    
    db_data_houses = get_all_db_houses()
    no_finished_process = get_no_finished_processes()
    all_transports = get_all_transports()
    print(f"Unattended processes: {no_finished_process}")
    for num_process in no_finished_process:
        status_process = False
        status_process = await houseLinks(zone, num_process,db_data_houses, text_filter_publicacion, all_transports)
        if status_process == False:
            print(f"Error in process {num_process}")
            break
        else:
            try:
                delete_process(num_process)
                print(f"Process {num_process} deleted")
            except Exception as e:
                print(f"Error deleting process {num_process}: {e}")
                break


# async def update_info():
#     #Fixed paramaters
#    try:
#        houses_latlong = await update_inf_latlong_dist()
#        if houses_latlong:
#           update_db_latlong_dist(houses_latlong)
#           print("Process finished")
#           print("Database updated with latitude and longitude information.")
#           return True
#        else:
#           print("No houses found to update.")
#           return False
#    except Exception as e:
#        print(f"Error updating information: {e}")
#        return False

# def test_calcular_distancias_to_transports():
#     all_transports = get_all_transports()
#     lat = 40.4734285
#     lng = -3.5796101
#     dict_distance_to = calcular_distancias_vivienda_transportes(lat,lng,all_transports)
#     return None

if __name__ == "__main__":
    #Principal
    asyncio.run(run())
    
    
    #test_calcular_distancias_to_transports()
    ##asyncio.run(update_info())
    #asyncio.run(get_house_description(['93595363'], 'Madrid')) #For Testing

    