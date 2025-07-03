import requests as rq
from bs4 import BeautifulSoup
import datetime as dt
import re

import httpx
import asyncio
import pymssql


import sys
import os
project_root = os.path.abspath(os.path.join(os.getcwd()+"/TFM_GroupC_KS24-25"))

# Add to sys.path if not already added
if project_root not in sys.path:
    sys.path.append(project_root)
print(sys.path)

from urllib.parse import urlparse, parse_qs
from data_import.idealista.utils.tfm_auxiliar_functions import *
from data_import.idealista.utils.tfm_functions_bd_mac import *



# BASE_HEADERS = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-language": "en-US;en;q=0.9",
#     "accept-encoding": "gzip, deflate, br",
# }

BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cookie': 'ttcsid_C5OI33SVNBDLN9M57490=1751465540234::yY557PzHE3jTxB6JVqOY.1.1751465670225; datadome=uQN_mQH2wZ3lzgQnP9aZasQfIPr2mD2cAuOwcfH4A1wZQsZumOumSLQkoe_2LyWp02tXuNHdpf3RYRV6VX8YxBu9hQfjsJHfo2bkk7PjI1OT5EOihntkGxvN6~31SRVV; _clsk=fqp68e%7C1751465641447%7C44%7C0%7Ca.clarity.ms%2Fcollect; ABTasty=uid=sy057h5bfxtqg8gs; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.idealista.com%252Finmueble%252F93595363%252F; _tt_enable_cookie=1; _ttp=01JZ5QPEM8T6Z00WHKZNWFCBWF_.tt.1; _uetsid=9b694360574e11f082ce772aefa08864; _uetvid=9b698260574e11f09357e78d2d04d875; utag_main__pn=2%3Bexp-session; utag_main__prevEventLink=; utag_main__prevEventView=005-idealista/portal > portal > adDetail > > > > > viewAdDetail%3Bexp-1751469240761; utag_main__prevLevel2=005-idealista/portal%3Bexp-1751469240761; utag_main__se=9%3Bexp-session; utag_main__sn=1; utag_main__ss=0%3Bexp-session; utag_main__st=1751467440758%3Bexp-session; utag_main_ses_id=1751465528302%3Bexp-session; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22I2ZjALOIMlN63JKWmgyo%22%2C%22expiryDate%22%3A%222026-07-02T14%3A14%3A00.843Z%22%7D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-07-02T14%3A14%3A00.843Z%22%7D; contact39576d83-8954-4afc-a49d-1ec22d798995="{\'maxNumberContactsAllow\':10}"; ttcsid=1751465540235::eXlf7suzQG43oOJaL-wH.1.1751465638360; _clck=15il7e1%7C2%7Cfx9%7C0%7C2009; dicbo_id=%7B%22dicbo_fetch%22%3A1751465540518%7D; didomi_token=eyJ1c2VyX2lkIjoiMTk3Y2I3YjAtYjZhOC02MjU2LWJiYzAtOWNlYzkxY2NjNGFiIiwiY3JlYXRlZCI6IjIwMjUtMDctMDJUMTQ6MTI6MDguMTcwWiIsInVwZGF0ZWQiOiIyMDI1LTA3LTAyVDE0OjEyOjE5Ljk2N1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQT7KEAQT7KEAAHABBENBxFsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgtWUgAwABBashABgACC1Y6ADAAEFqwkAGAAILVgAA.f_wAAAAAAAAA; utag_main__prevTsCampaign=organicTrafficByTm%3Bexp-1751469128305; utag_main__prevTsProvider=%3Bexp-1751469128305; utag_main__prevTsReferrer=https://www.idealista.com/inmueble/93595363/%3Bexp-1751469128305; utag_main__prevTsSource=Portal sites%3Bexp-1751469128305; utag_main__prevTsUrl=https%3A%2F%2Fwww.idealista.com%2Finmueble%2F93595363%2F%3Bexp-1751469128305; _pcid=%7B%22browserId%22%3A%22mcm1cqz9q8ld7fxr%22%2C%22_t%22%3A%22msaga8h2%7Cmcm1cr52%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbCIQDmhABwALACwAffgGN%2BARnkwArFJABfIA; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1zYWdhOGJifG1jbTFjcXpiIn0%3D; SESSION=43d96ceac90fd93d~39576d83-8954-4afc-a49d-1ec22d798995; userUUID=4081f2e2-77fb-4540-bc44-c05c074664fa',
    "accept-encoding": "gzip, deflate, br"
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


async def get_house_description(ids_houses, zone):
    #Get the description of the house
    for id_house in ids_houses:
        url = f"https://www.idealista.com/inmueble/{id_house}/"
        response = session.get(url)
        response = await response
        if response.status_code != 200:
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
            if lat != 0 or lng != 0:
                district = get_neighbourhood_group(lat, lng)
                if district == None:
                    district = "Not defined"
            house_detail["distrito"] = district


            #Insert the house in the database
            try:
                insert_houses_db(house_detail)
            except Exception as e:
                print(f"Error inserting house {id_house} in database: {e}")
                #If error we finish the process
                return False      
    return True

async def houseLinks(zone:str, num_process:int,db_data_houses:set, text_filter_publicacion:str = ",publicado_ultimo-mes"):
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
                        all_house_processes_status = await get_house_description(diff_id_houses, zone)
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
    print(f"Unattended processes: {no_finished_process}")
    for num_process in no_finished_process:
        status_process = False
        status_process = await houseLinks(zone, num_process,db_data_houses, text_filter_publicacion)
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

if __name__ == "__main__":
    #Principal
    #asyncio.run(run())
    
    
    ##asyncio.run(update_info())
    asyncio.run(get_house_description(['93595363'], 'Madrid'))

    