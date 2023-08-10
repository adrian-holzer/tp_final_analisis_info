
class Config:
    # Configuración de la conexión a la base de datos PostgreSQL
    DB_USER = "tu_usuario"
    DB_PASSWORD = "tu_contraseña"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "nombre_de_tu_base_de_datos"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

    
    # Configuración para trabajar con la API de OpenWeatherMap

    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"

    API_KEY='tu_api_key'

    




