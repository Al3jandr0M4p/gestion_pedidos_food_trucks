# routes/route.py

"""
Modulo de configuracion de rutas de la aplicacion.

Este modulo define la clase `ConfigurationRoutesApp`, que configura
y registra todas las rutas de la app Flask.
"""

# Importaciones propias

# Authorized
from .auth.login import Login
from .auth.register import RegisterApp
from .auth.logout import Logout

# administration
from .admin.admin import AdminApp

# Users
from .client.user import UserApp

class ConfigurationRoutesApp:
    """
    Clase para configurar las rutas de la aplicacion Flask.

    Esta clase se encarga de registrar las rutas relacionadas con
    autenticacion, administracion y usuarios dentro de la aplicacion.

    Atributos:
    ---------
    routes : Flask
        Instancia de la aplicacion Flask donde se registran las rutas.
    
    Metodos:
    -------
    setup_routes_app()
        Registra las rutas en la aplicacion Flask.
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask.

        Parametros:
        -----------
        app : Flask
            Instancia de la aplicacion Flask donde se configuran las rutas.
        """
        self.routes = app
        self.setup_routes_app()
    
    def setup_routes_app(self):
        """
        Registra las rutas de la aplicacion Flask.

        Incluye rutas para autenticacion, administracion y usuarios.
        """
        
        # Authorized
        Logout(self.routes)
        RegisterApp(self.routes)
        Login(self.routes)
        
        # Administration
        AdminApp(self.routes)

        # User
        UserApp(self.routes)