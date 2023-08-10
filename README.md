

# Trabajo Práctico Final Análisis de Datos

Grupo 6 : 

- Mercado, Isaac Pablo Rubén
- Melisa Marlen Benitez
- Juan Jose Juarez
- Ariel Solis
- Andrea Mellinger
- Juan Carlos Olmedo
- Melani Rodríguez
- Mauro Federico Rascón
- Miguel Adrian Holzer Egea
- Gastón Darío Pérez Parra


# Proyecto de Clima - Instrucciones

** Ve al sitio web de OpenWeatherMap (https://openweathermap.org/) y regístrate para obtener una API KEY gratuita.




## Nivel 1 
 
### Configuración de la API de OpenWeatherMap


1. Una vez que tengas tu API KEY, actualiza el valor de la variable api_key :

  
   api_key = 'tu_api_key_de_openweather'

 




## Nivel Medio 


### Configuración del Entorno Virtual

1. Primero, asegúrate de tener Python instalado en tu sistema.
2. Abre una terminal o línea de comandos y ve al directorio raíz del proyecto.
3. Crea un nuevo entorno virtual ejecutando el siguiente comando:

   
   python -m venv venv
   

4. Activa el entorno virtual. En Windows, ejecuta:

   
   venv\Scripts\activate
   

   En macOS y Linux, ejecuta:

   
   source venv/bin/activate
   

### Instalación de Dependencias

Una vez que el entorno virtual esté activado, instala las dependencias del proyecto desde el archivo `requirements.txt`. Ejecuta el siguiente comando:


pip install -r requirements.txt


### Configuración de la Base de Datos

1. Asegúrate de tener una base de datos creada en PostgreSQL donde se almacenarán los datos del clima. 

2. Abre el archivo `config.py` y actualiza los siguientes valores con los datos de tu base de datos:
 
   
   DB_USER = 'tu_usuario'
   DB_PASSWORD = 'tu_contraseña'
   DB_HOST = 'localhost'  # Cambia esto si tu base de datos está en otro host
   DB_PORT = '5432'  # Cambia esto si estás usando otro puerto
   DB_NAME = 'nombre_de_tu_base_de_datos'
   

3. Ejecuta el siguiente comando para crear las tablas en la base de datos:

   
   python create_tables.py
   

## Configuración de la API de OpenWeatherMap


1. Una vez que tengas tu API KEY, abre el archivo `config.py` nuevamente y actualiza el siguiente valor:

  
   API_KEY = 'tu_api_key_de_openweather'
   

## Puesta en marcha del Proyecto

¡El proyecto está listo para funcionar!

1. Asegúrate de que tu base de datos esté creada y las tablas estén creadas utilizando `create_tables.py`.

2. Ejecuta el siguiente comando para iniciar el programa:

   
   python main.py


Con esto, el programa descargará los datos del clima de los últimos 5 días de diferentes ciudades desde OpenWeatherMap, los procesará y los almacenará en la base de datos que has configurado.