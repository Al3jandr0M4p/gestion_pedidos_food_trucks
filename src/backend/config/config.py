"""
Configuracion de la applicacion.

Este modulo carga las variables de entorno desde un archivo `.env` y proporciona una clase
para gestionar la configuracion de la app.

Ejemplo:
-------
>>> from config import Config
>>> print(Config.DEBUG)
>>> print(Config.DB)

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

    Atributos
    ---------
    SECRET_KEY : str or None
        Clave secreta utilizada por flask para sessiones y seguridad.
    DEBUG : bool
        Indeica si la app se ejecuta en modo depuracion.
    FLASK_ENV : str
        Entorno de ejecucion de FLask (e.g 'development', 'production').
    
    Base de Datos
    -------------
    HOST : str or None
        Direccion del servidor de la base de datos.
    USER : str or None
        Usuario de la base de datos.
    PASSWD : str or None
        Contraseña del usuario de la base de datos.
    DB : str or None
        Nombre de la base de datos.
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