"""
Configuracion de la applicacion.

Este modulo carga las variables de entorno desde un archivo `.env` y proporciona una clase
para gestionar la configuracion de la app.
"""

from dotenv import load_dotenv
import os

# Cargar variables de enetorno antes de la clase
env_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', '..', '..', '.env'
    )
)
load_dotenv(env_path)

class Config:
    """
    Clase de configuracion para la app.

    Carga y gestiona las variables de entorno necesaria para la app.    
    """

    # Variables basicas
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Base de datos
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    PASSWD = os.getenv('PASSWD')
    DB = os.getenv('DB')