"""
Modulo de cierre de sesion de la aplicacion

Este modulo define la clase `Logout` que configura y gestiona 
la ruta de cierre de sesion dentro de la aplicacion Flask.
"""

from flask import session, redirect, url_for, flash
import logging

class Logout:
    """
    Clase para gestionar el cierre de sesion en la aplicacion Flask

    Esta clase configura la ruta de cierre de sesion y maneja la 
    logica para limpiar la sesion del usuario.
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask.
        """
        self.logout = app
        self.setup_routes()

        # log del logout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler('logout.log')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def setup_routes(self):
        """
        Configura la ruta de cierre de sesion

        Registra la ruta `/logout` y define la logica para limpiar la session del usuario.
        """

        @self.logout.route('/logout')
        def logout():
            """
            Maneja la logica de cierre de sesion.
            """

            self.logger.debug("Ruta /logout accedida.")
            
            try:
                if 'user_id' in session:
                    user = session.get('user_name')
                    session.clear()
                    self.logger.info(f"Sesion cerrada por: {user}")
                    flash("Has cerrado session correctamente.", "success")
                else:
                    self.logger.warning("Intento de logout sin sesion activa.")
                    flash("No habia ninguna session activa.", "info")
            except Exception as e:
                self.logger.error(f"Error durante el cierre de session: {str(e)}")
                flash("Ocurrio un error al cerrar sesion. Intentalo mas tarde.", "error")

            return redirect(url_for('login'))