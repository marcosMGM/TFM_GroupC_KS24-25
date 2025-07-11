import sys
import os
import numpy as np

project_root = os.getcwd() #give us the actual directory

# Obtener el directorio padre de project_root to register credenciales_sqlserver.py
base_dir = os.path.abspath(os.path.join(project_root, ".."))
print(base_dir)
if base_dir not in sys.path:
    sys.path.append(base_dir)
print(sys.path)

import pandas as pd
import credenciales_sqlserver as cred
import utils.tfm_functions_bd_mac as tfbd
import utils.tfm_auxiliar_functions as tfmg


def pre_model_sequence():
    #Primero excluimos los registros que no tienen DISTRITO definido. Son registros de la comunidad de Madrid, pero no de la ciudad de Madrid.add()
    #No borramos estos registros, para que el Scrapping no los vuelva a recoger
    tfbd.update_processed_with_distrito_not_defined()
    df = pd.read_sql_query("SELECT * FROM HOUSES WHERE PROCESSED = 0", tfbd.get_connection())
    df = df[["HOUSE_ID","DISTRITO","HABITACIONES","BANOS","GARAJE","CALEFACCION","PISCINA","ASCENSOR","MOVILIDAD_REDUCIDA","TERRAZA","BALCON","AIRE_ACOND","LATITUDE","LONGITUDE","DISTANCE_TO_METRO","DISTANCE_TO_CERCANIAS","DISTANCE_TO_EMT","DISTANCE_TO_INTERURBANOS","DISTANCE_TO_MLO"]]
    # Tratamiento de la columna HABITACIONES -> bedrooms
    df.loc[df["HABITACIONES"] == "Sin habitación", "HABITACIONES"] = "1"
    df["bedrooms"] = df["HABITACIONES"].str.replace(" habitaciones", "").str.replace(" habitación", "").astype("int")
    # Tratamiento de columna BANOS -> bathrooms
    df.loc[df["BANOS"] == "Sin baños", "BANOS"] = "1"
    df["bathrooms"] = df["BANOS"].str.replace(" baños", "").str.replace(" baño", "").astype("int")
    # Tratamiento de Garaje
    df["GARAJE"] = df["GARAJE"].astype(int)
    # Tratamiento de Calefaccion
    df["CALEFACCION"].fillna(0,inplace=True)
    df.loc[df["CALEFACCION"] == "No dispone de calefacción", "CALEFACCION"] = 0
    df.loc[df["CALEFACCION"] != 0, "CALEFACCION"] = 1
    df["CALEFACCION"] = df["CALEFACCION"].astype(int)
    # Tratamiento de piscina
    df["PISCINA"] = df["PISCINA"].astype(int)
    # Tratamiento de Ascensor
    df["ASCENSOR"] = df["ASCENSOR"].astype(int)
    # Tratamiento Movilidad Reducida
    df.loc[df["MOVILIDAD_REDUCIDA"] != "1","MOVILIDAD_REDUCIDA"] = 0
    df["MOVILIDAD_REDUCIDA"] = df["MOVILIDAD_REDUCIDA"].astype("int")
    # Tratamiento de Terraza, Balcon y Aire Acond
    df["TERRAZA"] = df["TERRAZA"].astype("int")
    df["BALCON"] = df["BALCON"].astype("int")
    df["AIRE_ACOND"] = df["AIRE_ACOND"].astype("int")
    # Nueva Columna Distance_to_center
    center_lat, center_lon = 40.4168, -3.7038
    df['distance_to_center'] = np.sqrt((df['LATITUDE'] - center_lat)**2 + (df['LONGITUDE'] - center_lon)**2)
    # Nueva columna renta_bin
    df["DISTRITO"].value_counts()
    #Import data from Ayto de Madrid, rentas
    df_rentas = tfmg.get_df_rentas()#pd.read_csv('../data_import/ayto_madrid/Datos_Rentas_Madrid_2022.csv',delimiter=";")
    df["renta_bin"] = df['DISTRITO'].apply(lambda x: tfmg.get_renta_bin(x, df_rentas))
    df["renta_bin"].value_counts()
    df = df [['HOUSE_ID','GARAJE','CALEFACCION', 'PISCINA', 'ASCENSOR', 'MOVILIDAD_REDUCIDA', 'TERRAZA',
           'BALCON', 'AIRE_ACOND','DISTANCE_TO_METRO',
           'DISTANCE_TO_CERCANIAS', 'DISTANCE_TO_EMT', 'DISTANCE_TO_INTERURBANOS',
           'DISTANCE_TO_MLO', 'bedrooms', 'bathrooms',
           'distance_to_center', 'renta_bin']]

    df.rename(columns={'ASCENSOR': 'ascensor',
        'GARAJE': 'garaje',
        'PISCINA': 'pool',
        'CALEFACCION':'calefaccion',
        'TERRAZA': 'terraza',
        'BALCON': 'balcon',
        'MOVILIDAD_REDUCIDA':'movilidad_reducida',
        'AIRE_ACOND':'aire_acondicionado',
        'DISTANCE_TO_METRO':'distance_to_metro',
        'DISTANCE_TO_CERCANIAS':'distance_to_cercanias',
        'DISTANCE_TO_EMT':'distance_to_emt',
        'DISTANCE_TO_INTERURBANOS':'distance_to_interurbanos',
        'DISTANCE_TO_MLO':'distance_to_mlo'},
        inplace = True)
    return df



if __name__ == "__main__":
    df = pre_model_sequence()
    print(df)

