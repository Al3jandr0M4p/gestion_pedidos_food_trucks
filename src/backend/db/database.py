"""
Modulo de configuracion y conexion a la base de datos.

Este modulo proporciona la clase `DBConfig` para manejar la configuracion y
la conexion a la base de datos utilozando `mysql-connector-python`.
"""

from mysql.connector import connect, Error
from ..config.config import Config

class DBConfig:
    """
    Clase para gestionar la configuracion y conexion a la base de datos.
    """

    def __init__(self):
        """
        Inicializa la configuracion de la base de datos con los valores de Config.
        """
        self.host = Config.HOST
        self.user = Config.USER
        self.passwd = Config.PASSWD
        self.db = Config.DB

    def get_db_config(self):
        """
        Establece una conexion a la base de datos.
        """

        try:

            conn = connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                db=self.db
            )
            return conn

        except Error as e:
            print(f"Error en la conexion de la db: {e}")
            return f"Error en la db: {e}"