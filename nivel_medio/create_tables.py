
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    nombre_ciudad = Column(String)
    temperatura = Column(Float)
    presion = Column(Integer)
    fecha_hora = Column(DateTime)
    amanecer = Column(DateTime)
    atardecer = Column(DateTime)
    sensacion_termica = Column(Float)
    humedad= Column(Integer)
    visibilidad = Column(Integer)
    velocidad_viento = Column(Float)
    direccion_viento = Column(Integer)
    descripcion_clima = Column(String)

# Leer las credenciales de conexión a la base de datos desde el archivo config.py
config = Config()

# Establecer la conexión a la base de datos PostgreSQL utilizando SQLalchemy
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)