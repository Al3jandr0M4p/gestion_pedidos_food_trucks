'''
Módulo principal de la aplicación FoodTrucks.

Este módulo define la clase `FoodTrucks`, que inicializa y configura
la aplicación Flask, gestiona el registro de logs y define el manejo
de errores.
'''

# Importaciones de Flask
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail

import os

# Importaciones propias
from ..config.config import Config
from .routes.route import ConfigurationRoutesApp
from .error import Errors

class FoodTrucks:
    '''
    Clase principal de la aplicación FoodTrucks.

    Esta clase configura la aplicación Flask, inicializa las rutas,
    maneja errores y establece el sistema de logging.
    '''

    def __init__(self):
        '''
        Inicializa la aplicación Flask con su configuración, rutas y sistema de logging.
        '''
        self.food = Flask(
            __name__,
            template_folder=os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'templates')
            ),
            static_folder=os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static')
            )
        )
        
        # Configuración de la aplicación
        self.food.config['SECRET_KEY'] = Config.SECRET_KEY
        self.food.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=587,
            MAIL_USE_TLS=True,
            MAIL_USERNAME=os.getenv('EMAIL_USER'),
            MAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
            MAIL_DEFAULT_SENDER=os.getenv('EMAIL_DEFAULT_SENDER')
        )
        
        self.mail = Mail(self.food)
        CORS(self.food)
        self.cache = Cache(self.food, config={'CACHE_TYPE': 'simple'})
        
        # Configuración de las rutas
        ConfigurationRoutesApp(self.food)

        # Configuración del manejo de errores
        Errors(self.food).setup_error_handlers()
    
    def run_app(self):
        '''
        Inicia la aplicación Flask en el host `0.0.0.0`.

        Registra un mensaje en los logs antes de iniciar la aplicación.
        En caso de error durante el inicio, el error se registra en el logger de errores.
        '''
        self.food.run(debug=True, host="0.0.0.0")