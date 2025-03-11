"""
Modulo de cierre de sesion de la aplicacion

Este modulo define la clase `Logout` que configura y gestiona 
la ruta de cierre de sesion dentro de la aplicacion Flask

Ejemplo
-------
>>> from flask import Flask
>>> from src.backend.python.routes.logout import Logout
>>> app = Flask(__name__)
>>> Logout(app)
"""

from flask import session, redirect, url_for, flash

class Logout:
    """
    Clase para gestionar el cierre de sesion en la aplicacion Flask

    Esta clase configura la ruta de cierre de sesion y maneja la 
    logica para limpiar la sesion del usuario

    Atributos
    ---------
    logout : Flask
        Instancia de la aplicacion Flask donde se registra la ruta de cierre de sesion

    Metodos
    -------
    setup_routes()
        Configura la ruta de cierre de sesion.
    
    logout()
        Maneja la logica de cierre de session.
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask

        Parametros
        ----------
        app : Flask
            Instancia de la aplicacion Flask donde se configurara la ruta de cierre de sesion
        """
        self.logout = app
        self.setup_routes()

    def setup_routes(self):
        """
        Configura la ruta de cierre de sesion

        Registra la ruta `/logout` y define la logica para limpiar la session del usuario.

        Returns
        -------
        None
        """

        @self.logout.route('/logout')
        def logout():
            """
            Maneja la logica de cierre de sesion.

            - Si el usuario tiene una session activa, la borra y lo redirige al login.
            - Si no hay session activa, simplemente lo redirige.
            - Muestra un mensaje de notificacion usando `flash`.

            Returns
            -------
            Response
                Redirige a la ruta de inicio de sesion con un mensaje.
            """
            if 'user_id' in session:
                session.clear()
                flash("Has cerrado session correctamente.", "success")
            else:
                flash("No habia ninguna session activa.", "info")
            return redirect(url_for('login'))