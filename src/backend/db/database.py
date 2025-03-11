"""
Modulo de configuracion y conexion a la base de datos.

Este modulo proporciona la clase `DBConfig` para manejar la configuracion y
la conexion a la base de datos utilozando `mysql-connector-python`.

Ejemplo:
-------
>>> from src.db.database import DBConfig
>>> db = DBConfig()
>>> connection = db.get_db_config()
>>> if connection:
>>>     print("Conexion exitosa")
"""

from mysql.connector import connect, Error
from ..config.config import Config

class DBConfig:
    """
    Clase para gestionar la configuracion y conexion a la base de datos.

    Atributos
    --------
    host : str or None
        Dirección del servidor de la base de datos.
    user : str or None
        Usuario de la base de datos.
    passwd : str or None
        Contraseña del usuario de la base de datos.
    db : str or None
        Nombre de la base de datos.
    
    Metodos
    -------
    get_db_config()
        Establece y retorna una conexion a la base de datos.
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

        Returns
        -------
        mysql.connector.connection.MySQLConnection or str
            Devuelve un objeto de conexion si es exitosa, o un mensaje de error en caso contrario.
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