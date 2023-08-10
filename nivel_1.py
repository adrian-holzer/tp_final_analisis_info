from datetime import datetime, timedelta
import requests
import pandas as pd
from pandas import json_normalize
import os

# Función para obtener y guardar los datos meteorológicos en formato CSV
def obtener_datos_meteorologicos_ciudades():
    # Claves de la API de OpenWeatherMap y la URL base
    api_key = 'API_KEY'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    # Lista de ciudades y coordenadas para buscar
    cityList = ["Londres", "Nueva York", "Córdoba", "Taipei", "Buenos Aires", "Ciudad de México", "Dublín", "Resistencia", "Bogotá", "Tokio"]
    coordList = ["lat=51.5074&lon=-0.1278", "lat=40.7128&lon=-74.0060", "lat=-31.4173&lon=-64.1836", "lat=25.0330&lon=121.5654", "lat=-34.6037&lon=-58.3816", "lat=19.4326&lon=-99.1332", "lat=53.3498&lon=-6.2603", "lat=-27.45&lon=-58.98333", "lat=4.7110&lon=-74.0721", "lat=35.6895&lon=139.6917"]

    # Ruta base para guardar los archivos
    base_path = 'data_analytics/openweather/'

    # Crear el directorio base si no existe
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Obtener la fecha actual en formato yyyymmdd
    fecha_actual = datetime.now().strftime("%Y%m%d")

    # Realizar solicitudes para cada ciudad y guardar los datos en archivos CSV
    for i in range(len(cityList)):
        ciudad = cityList[i]
        coordenadas = coordList[i]

        # Hacer la solicitud a la API
        url = f"{base_url}?q={ciudad}&{coordenadas}&appid={api_key}&units=metric"
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            
            # Normalizar los datos principales (excepto weather)
            normalized_data = json_normalize(data)
            weather_data = data['weather']
            
            # Normalizar los datos del clima (weather)
            normalized_weather = json_normalize(weather_data)

            # Combinar los DataFrames de los datos principales y el clima
            result_df = pd.concat([normalized_data, normalized_weather], axis=1)

            # Eliminar columnas innecesarias
            keys_to_remove = ['weather', 'base', 'timezone', 'id', 'name', 'cod']
            for key in keys_to_remove:
                result_df.drop(key, axis=1, inplace=True)

            # Renombrar las columnas para mejorar los encabezados
            nuevo_nombre_columnas = {
                'visibility': 'visibilidad',
                'main.temp': 'temperatura',
                'main.feels_like': 'sensacion_termica',
                'main.temp_min': 'temperatura_minima',
                'main.temp_max': 'temperatura_maxima',
                'main.pressure': 'presion',
                'main.humidity': 'humedad',
                'main.sea_level': 'nivel_mar',
                'main.grnd_level': 'nivel_suelo',
                'wind.speed': 'velocidad_viento',
                'wind.deg': 'direccion_viento',
                'wind.gust': 'rafaga_viento',
                'clouds.all': 'nubosidad',
                'coord.lon': 'longitud',
                'coord.lat': 'latitud',
                'sys.type': 'tipo_sys',
                'sys.id': 'id_sys',
                'sys.country': 'pais',
                'sys.sunrise': 'amanecer_unix',
                'sys.sunset': 'atardecer_unix',
                'dt': 'tiempo_unix',  # Renombrar dt a tiempo_unix
                'description': 'descripcion_clima',
                'icon': 'icono_clima'
            }
            result_df.rename(columns=nuevo_nombre_columnas, inplace=True)

            # Convertir los valores de amanecer, atardecer y dt de tiempo Unix a formato Datetime
            result_df['amanecer'] = pd.to_datetime(result_df['amanecer_unix'], unit='s') + timedelta(seconds=data['timezone'])
            result_df['amanecer'] = result_df['amanecer'].dt.strftime('%Y-%m-%d %H:%M:%S')

            result_df['atardecer'] = pd.to_datetime(result_df['atardecer_unix'], unit='s') + timedelta(seconds=data['timezone'])
            result_df['atardecer'] = result_df['atardecer'].dt.strftime('%Y-%m-%d %H:%M:%S')

            result_df['Fecha_Hora_Actualizacion'] = pd.to_datetime(result_df['tiempo_unix'], unit='s') + timedelta(seconds=data['timezone'])
            result_df['Fecha_Hora_Actualizacion'] = result_df['Fecha_Hora_Actualizacion'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Eliminar las columnas de amanecer, atardecer y dt en formato de tiempo Unix
            result_df.drop(['amanecer_unix', 'atardecer_unix', 'tiempo_unix'], axis=1, inplace=True)

            # Crear el nombre del archivo con la fecha actual y la ciudad
            nombre_archivo = f"{base_path}{ciudad.lower().replace(' ', '_')}_{fecha_actual}.csv"
            
            # Guardar el DataFrame en el archivo CSV
            result_df.to_csv(nombre_archivo, index=False)

            print(f"Datos meteorológicos para {ciudad} guardados en: {nombre_archivo}")
        else:
            print(f"Error al obtener los datos para {ciudad}. Código de estado: {response.status_code}")

# Llamar a la función para obtener y guardar los datos meteorológicos de las ciudades
obtener_datos_meteorologicos_ciudades()




