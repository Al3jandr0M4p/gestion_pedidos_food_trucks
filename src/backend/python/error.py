# python/error.py

"""
Modulo de manejo de errores para la aplicacion Flask.

Este modulo define la clase `Errors`, que configura el manejo de errores
personalizados dentro de la aplicacion, registrando los errores y
mostrando plantillas HTML especificas.

Ejemplo:
-------
>>> from flask import Flask
>>> from src.backend.python.error import Errors
>>> app = Flask(__name__)
>>> error_logger = app.logger
>>> Errors(app, error_logger).setup_error_handlers()
"""

from flask import render_template, session, request
from werkzeug.exceptions import HTTPException

class Errors:
    """
    Clase para gestionar el manejo de errores en la aplicacion Flask.

    Esta clase configura los handlers para capturar excepciones HTTP 
    y errores especificos, registrandolos en el sistema de logs 
    y mostrando páginas de error personalizadas.

    Atributos
    ---------
    error : Flask
        Instancia de la aplicacion Flask.
    logger : logging.Logger
        Logger utilizado para registrar los errores.

    Metodos
    -------
    setup_error_handlers()
        Configura los manejadores de errores personalizados para la aplicacion.
    """

    def __init__(self, app, error_logger):
        """
        Inicializa la clase con la aplicacion Flask y logger de errores.

        Parametros
        ---------
        app : Flask
            Instancia de la aplicacion Flask.
        error_logger : logging.Logger
            Logger utilizado para registrar los errores.
        """
        self.error = app
        self.logger = error_logger
    
    def setup_error_handlers(self):
        """
        Configura los manejadores de errores de la aplicacion.

        Captura y maneja diferentes codigos de error HTTP, registrando la
        informacion relevante y renderiizando plantillas HTML personalizadas.

        Errores manejados:
        - 400 (Bad Request)
        - 403 (Forbidden)
        - 404 (Not Found)
        - 500 (Internal Server Error)
        - Excepciones HTTP generales

        Returns:
        -------
        None
        """

        @self.error.errorhandler(HTTPException)
        def handle_http_exception(error):
            """
            Maneja expciones HTTP genericas.
            """

            self.logger.error((f"HTTP Exception: {error}"))
            return render_template('errors/httpException.html', error=error)
        
        @self.error.errorhandler(400)
        def bad_request(e):
            """
            Maneja el error 400 (Solicitudes incorrecta).
            """

            self.logger.error(f"Solicitud incorrecta: {request.url} - Error: {e}", exc_info=True)
            return render_template('errors/400.html', request_url=request.url)
        
        @self.error.errorhandler(404)
        def not_found(e):
            """
            Maneja el error 404 (Pagina no encontrada).
            """

            self.logger.error(f"Pagina no encontrada: {request.url} - Error: {e}", exc_info=True)
            mesa_asignada = session.get('mesa_asignada')
            return render_template('errors/404.html', mesa_asignada=mesa_asignada, user_id=session.get('user_id'))
        
        @self.error.errorhandler(403)
        def forbidden(e):
            """
            Maneja el error 403 (Acceso denegado).
            """

            self.logger.error(f"Acceso denegado: {request.url} - Error: {e}", exc_info=True)
            return render_template('errors/403.html', request_url=request.url)
        
        @self.error.errorhandler(500)
        def internal_server_error(e):
            """
            Maneja el error 500 (Error interno del servidor).
            """

            self.logger.error(f"Error interno del servidor: {request.url} - Error: {e}", exc_info=True)
            return render_template('errors/500.html')