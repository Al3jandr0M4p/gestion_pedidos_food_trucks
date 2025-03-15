# python/app.py

"""
Modulo principal de la aplicacion FoodTrucks.

Este modulo define la clase `FoodTrucks`, que inicializa y configura
la aplicacion Flask, gestiona el registro de los logs y define el manejo
de errores.

Ejemplo:
-------
>>> from src.backend.python.app import FoodTrucks
>>> app = Foodtrucks()
>>> app.run_app()
"""

# Importaciones de flask
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail

# importaciones del logging
import logging
from rich.logging import RichHandler
import os

# importaciones propias
from ..config.config import Config
from .routes.route import ConfigurationRoutesApp
from .error import Errors

class FoodTrucks:
    """
    Clase principal de la aplicacion FoodTrucks.

    Este clase configura la aplicacion Flask, inicializa las rutas,
    configura el manejo de errores y establece el sistema de logging.

    Atributos:
    ---------
    food : Flask
        Instancia de la aplicación Flask.
    cache : flask_caching.Cache
        Configuración de caché de la aplicación.
    general_logger : logging.Logger
        Logger principal de la aplicación.
    error_logger : logging.Logger
        Logger para errores de la aplicación.
    http_logger : logging.Logger
        Logger para registrar peticiones HTTP.
    
    Metodos:
    -------
    start_logging()
        Configura el sistema de logging de la aplicacion.
    run_app()
        Inicia la aplicacion Flask en el host `0.0.0.0`.
    """

    def __init__(self):
        """
        Inicializa la aplicación Flask con su configuración, rutas y sistema de logging.
        """
        self.food = Flask(
            __name__,
            template_folder=os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), '..', '..', 'frontend', 'templates'
                )
            ),
            static_folder=os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), '..', '..', 'frontend', 'static'
                )
            )
        )
        self.food.config['SECRET_KEY'] = Config.SECRET_KEY
        self.food.config['MAIL_SERVER'] = 'smtp.gmail.com'
        self.food.config['MAIL_PORT'] = 587
        self.food.config['MAIL_USE_TLS'] = True
        self.food.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
        self.food.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
        self.food.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_DEFAULT_SENDER')
        self.mail = Mail(self.food)
        CORS(self.food)
        self.cache = Cache(self.food, config={'CACHE_TYPE': 'simple'})
    
        # configuracion de las rutas de la app
        ConfigurationRoutesApp(self.food)

        # Configuracion del logging
        self.start_logging()

        # Handler de los errores de la app
        Errors(self.food, self.error_logger).setup_error_handlers()
    
    def start_logging(self):
        """
        Configuracion el sistema de logging de la aplicacion.

        Crea y configura los siguientes loggers:
        - `general`: 
            - Logger principal para informacion general.
        - `errors`: 
            - Logger para registrar errores criticos.
        - `http`: 
            - Logger para registrar las peticiones HTTP.
        - `console`: 
            - Logger de consola con formato enriquecido de `RichHandler`.
        """

        # Logger General
        self.general_logger = logging.getLogger('general')
        self.general_logger.setLevel(logging.INFO)
        general_handler = logging.FileHandler('logs/general.log', encoding='utf-8')
        general_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.general_logger.addHandler(general_handler)

        # Logger Errores
        self.error_logger = logging.getLogger("errors")
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler("logs/errors.log", encoding="utf-8")
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(error_handler)

        # Logger para peticiones HTTP
        self.http_logger = logging.getLogger("http")
        self.http_logger.setLevel(logging.DEBUG)
        http_handler = logging.FileHandler("logs/http.log", encoding="utf-8")
        http_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.http_logger.addHandler(http_handler)

        # Logger para la consola con Rich
        console_handler = RichHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.general_logger.addHandler(console_handler)
        self.error_logger.addHandler(console_handler)
        self.http_logger.addHandler(console_handler)

        self.general_logger.info("Configuracion de logging completada")

    def run_app(self):
        """
        Inicia la aplicacion Flask en el o-host `0.0.0.0`.

        Registra un mensaja en los logs antes de iniciar la aplicacion.
        En caso de error durante el inicio, el error se registra en el logger de errores.
        """
        self.general_logger.info("Iniciando aplicacion en  '0.0.0.0'")
        try:
            self.food.run(debug=True, host="0.0.0.0")
        except Exception as e:
            self.error_logger.error(f"Error al iniciar la aplicacion: {str(e)}")