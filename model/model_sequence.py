import sys
import os
import numpy as np
import pandas as pd
import skops.io as sio
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
#os.getcwd() get the current directory, where we are runnning the .py file
project_root = os.getcwd()
base_dir = os.path.abspath(os.path.join(project_root, "..")) #Should be the root directory of the project

#Adding the path to work with our modules
sys.path.append(base_dir)

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
    df["CALEFACCION"] = df["CALEFACCION"].fillna(0)
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
    # Create distance to El Retiro
    retiro_lat, retiro_lon = 40.415262, -3.6883366
    df['distance_to_retiro'] = np.sqrt((df['LATITUDE'] - retiro_lat)**2 + (df['LONGITUDE'] - retiro_lon)**2)
    # Create distance to Atocha
    atocha_lat, atocha_lon = 40.405383, -3.6914676
    df['distance_to_atocha'] = np.sqrt((df['LATITUDE'] - atocha_lat)**2 + (df['LONGITUDE'] - atocha_lon)**2)
    # Create distance to Chamartín
    chamartin_lat, chamartin_lon = 40.472103, -3.6852973
    df['distance_to_chamartin'] = np.sqrt((df['LATITUDE'] - chamartin_lat)**2 + (df['LONGITUDE'] - chamartin_lon)**2)
    # Nueva columna renta_bin
    df["DISTRITO"].value_counts()
    #Import data from Ayto de Madrid, rentas
    df_rentas = tfmg.get_df_rentas()#pd.read_csv('../data_import/ayto_madrid/Datos_Rentas_Madrid_2022.csv',delimiter=";")
    df["renta_bin"] = df['DISTRITO'].apply(lambda x: tfmg.get_renta_bin(x, df_rentas))
    df["renta_bin"].value_counts()
    df = df [['HOUSE_ID','DISTRITO','CALEFACCION', 'PISCINA', 'GARAJE','ASCENSOR', 'MOVILIDAD_REDUCIDA', 'TERRAZA',
           'BALCON', 'AIRE_ACOND','DISTANCE_TO_METRO',
           'DISTANCE_TO_CERCANIAS', 'DISTANCE_TO_EMT', 'DISTANCE_TO_INTERURBANOS',
           'DISTANCE_TO_MLO', 'bedrooms', 'bathrooms',
           'distance_to_center', 'distance_to_retiro','distance_to_atocha','distance_to_chamartin','renta_bin']]

    df.rename(columns={'ASCENSOR': 'ascensor',
        'DISTRITO': 'distrito',
        'PISCINA': 'piscina',
        'GARAJE': 'garaje',
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

    order_columns = ['HOUSE_ID','bedrooms', 'bathrooms','ascensor', 'piscina','garaje',
       'terraza', 'balcon', 'distance_to_center', 'aire_acondicionado',
       'movilidad_reducida', 'calefaccion', 'distance_to_metro',
       'distance_to_cercanias', 'distance_to_emt', 'distance_to_interurbanos',
       'distance_to_mlo','distance_to_retiro','distance_to_atocha','distance_to_chamartin','renta_bin','distrito']


    df = df[order_columns]
    print(df.info())
    return df


def get_predicts(df):

    #Verifications
    print("Type:", type(df))
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Any nulls:\n", df.isnull().sum())

    model_path = "model_tfm.skops"
    untrusted = sio.get_untrusted_types(file=model_path)
    try:
        model = sio.load(model_path, trusted=untrusted)
        #print(model)
        data = df.drop(columns=['HOUSE_ID'])
        
        test_predictions = model.predict(data)
        predictions = pd.DataFrame({'Id': df['HOUSE_ID'], 'Predicted': test_predictions})
        #Update the BD with the predictions and marking them to processed to 2
        predictions_tuple = list(zip(predictions['Id'].tolist(), predictions['Predicted'].tolist()))
        for predict in predictions_tuple:
            tfbd.update_predicted_price(predict[0],predict[1])
            print(f"House_id:{predict[0]} Predicted:{predict[1]}")
    except Exception as e:
        print("❌ Error during model prediction:")
        print(type(e).__name__, e)
        import traceback
        traceback.print_exc()




if __name__ == "__main__":
    df = pre_model_sequence()
    get_predicts(df)

