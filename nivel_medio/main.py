


import requests
import pandas as pd
from datetime import datetime, timedelta
from config import Config
from pandas import json_normalize
from  create_tables import WeatherData, Session



config = Config()


def guardar_datos_ciudad_to_bd(ciudad_nombre, latitud, longitud, fecha_unix):
    


   
    url = f"{config.BASE_URL}{latitud}&{longitud}&dt={fecha_unix}&appid={config.API_KEY}"
    response = requests.get(url)
    

    if response.status_code == 200:

        data = response.json()['current']

        # Normalizar los datos principales (excepto weather)
        normalized_data = json_normalize(data)
        weather_data = data['weather']

        # Normalizar los datos del clima (weather)
        normalized_weather = json_normalize(weather_data)

        # Combinar los DataFrames de los datos principales y el clima
        result_df = pd.concat([normalized_data, normalized_weather], axis=1)

        # * Eliminar columnas innecesarias *
        keys_to_remove = ['weather']

        # -  Verifica si la columna 'rain.1h' existe en result_df
        if 'rain.1h' in result_df.columns:
            keys_to_remove.append('rain.1h')

        # -  Remover columnas innecesarias
        for key in keys_to_remove:
            result_df.drop(key, axis=1, inplace=True)


    
        result_df["Nombre_Ciudad"] = ciudad_nombre
        result_df['Fecha_Hora'] = pd.to_datetime(result_df['dt'], unit='s')
        

      # Renombrar las columnas para mejorar los encabezados


        nuevo_nombre_columnas = {
            'Nombre_Ciudad' : 'Nombre_Ciudad',
            'Fecha_Hora' : 'Fecha_Hora',
            'dt':  'tiempo_unix',  
            'sunrise': 'amanecer_unix',
            'sunset':  'atardecer_unix',
            'temp': 'temperatura',
            'feels_like': 'sensacion_termica',
            'pressure': 'presion',
            'humidity':  'humedad',
            'dew_point':  'rocio',
            'clouds':  'nubes',
            'visibility': 'visibilidad',
            'wind_speed': 'velocidad_viento',
            'wind_deg': 'direccion_viento',
            'description': 'descripcion_clima'
        }

        result_df.rename(columns=nuevo_nombre_columnas, inplace=True)
        

        # Convertir los valores de amanecer, atardecer y dt de tiempo Unix a formato Datetime
        result_df['amanecer'] = pd.to_datetime(result_df['amanecer_unix'], unit='s') 
        result_df['amanecer'] = result_df['amanecer'].dt.strftime('%Y-%m-%d %H:%M:%S')


        result_df['atardecer'] = pd.to_datetime(result_df['atardecer_unix'], unit='s') 
        result_df['atardecer'] = result_df['atardecer'].dt.strftime('%Y-%m-%d %H:%M:%S')



        # Eliminar las columnas de amanecer, atardecer y dt en formato de tiempo Unix
        result_df.drop(['amanecer_unix', 'atardecer_unix', 'tiempo_unix'], axis=1, inplace=True)



        # Almacenamiento de los datos en la base de datos
        ## Creo el Objeto WeatherData y lo guardo
     
        session = Session()
        
        weather_data = WeatherData(nombre_ciudad=ciudad_nombre,presion= int(result_df['presion'][0]), temperatura= float(result_df['temperatura'][0]),
                                   fecha_hora=result_df['Fecha_Hora'][0]
                                   , amanecer= result_df['amanecer'][0] , atardecer= result_df['atardecer'][0],
                                   sensacion_termica= float(result_df['sensacion_termica'][0]),
                                   humedad= int(result_df['humedad'][0]), 
                                   visibilidad= int(result_df['visibilidad'][0]), velocidad_viento= float(result_df['velocidad_viento'][0]),direccion_viento= int(result_df['direccion_viento'][0]),
                                 descripcion_clima= result_df['descripcion_clima'][0]
                                   )
        session.add(weather_data)
        session.commit()


        return response.json()
    else:
        print(
            f"Error al obtener los datos para {ciudad_nombre}. Código de respuesta: {response.status_code}")
        return None
    



def main():

    # Implementa el código principal del programa 
    # Define una lista de ciudades con sus respectivas coordenadas y fechas unix.
    
    ciudades = ["Londres", "Nueva York", "Córdoba", "Taipei", "Buenos Aires", "Ciudad de México", "Dublín", "Resistencia", "Bogotá", "Tokio"]
    coordenadas = ["lat=51.5074&lon=-0.1278", "lat=40.7128&lon=-74.0060", "lat=-31.4173&lon=-64.1836", "lat=25.0330&lon=121.5654", "lat=-34.6037&lon=-58.3816", "lat=19.4326&lon=-99.1332", "lat=53.3498&lon=-6.2603", "lat=-27.45&lon=-58.98333", "lat=4.7110&lon=-74.0721", "lat=35.6895&lon=139.6917"]


    # Obtener fecha actual
    fecha_actual = datetime.now()


    # Iterar por cada ciudad y descargar los datos para los últimos 5 días

    for j, ciudad in enumerate(ciudades):
        print(ciudad)
        for i in range(5):
            fecha = fecha_actual - timedelta(days=i)
            fecha_unix = int(fecha.timestamp())
            guardar_datos_ciudad_to_bd(ciudad, coordenadas[j].split(
                '&')[0], coordenadas[j].split('&')[1], fecha_unix)

            

if __name__ == "__main__":
    main()
