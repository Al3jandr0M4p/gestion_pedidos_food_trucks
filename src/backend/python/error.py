# python/error.py

"""
Modulo de manejo de errores para la aplicacion Flask.

Este modulo define la clase `Errors`, que configura el manejo de errores
personalizados dentro de la aplicacion, registrando los errores y
mostrando plantillas HTML especificas.
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

    def __init__(self, app):
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
        """

        @self.error.errorhandler(HTTPException)
        def handle_http_exception(error):
            """
            Maneja expciones HTTP genericas.
            """
            mesa_asignada = session.get("mesa_asignada")
            return render_template('errors/httpException.html', error=error, mesa_asignada=mesa_asignada, user_id=session.get('user_id'))
        
        @self.error.errorhandler(400)
        def bad_request(e):
            """
            Maneja el error 400 (Solicitudes incorrecta).
            """
            return render_template('errors/400.html', request_url=request.url)
        
        @self.error.errorhandler(404)
        def not_found(e):
            """
            Maneja el error 404 (Pagina no encontrada).
            """
            mesa_asignada = session.get('mesa_asignada')
            return render_template('errors/404.html', mesa_asignada=mesa_asignada, user_id=session.get('user_id'))
        
        @self.error.errorhandler(403)
        def forbidden(e):
            """
            Maneja el error 403 (Acceso denegado).
            """
            return render_template('errors/403.html', request_url=request.url)
        
        @self.error.errorhandler(500)
        def internal_server_error(e):
            """
            Maneja el error 500 (Error interno del servidor).
            """
            return render_template('errors/500.html')