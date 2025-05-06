# routes/route.py

"""
Modulo de configuracion de rutas de la aplicacion.

Este modulo define la clase `ConfigurationRoutesApp`, que configura
y registra todas las rutas de la app Flask.
"""

# Importaciones propias

# Authorized
from .auth.login import Login
from .auth.logout import Logout

# administration
from .admin.admin import AdminApp

# Users
from .client.user import UserApp
from ..bot.userBot import NotificationBot

class ConfigurationRoutesApp:
    """
    Clase para configurar las rutas de la aplicacion Flask.

    Esta clase se encarga de registrar las rutas relacionadas con
    autenticacion, administracion y usuarios dentro de la aplicacion.
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask.
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
        Login(self.routes)
        
        # Administration
        AdminApp(self.routes)

        # User
        UserApp(self.routes)
        NotificationBot(self.routes)