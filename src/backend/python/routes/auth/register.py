"""
Modulo de registro de usuarios de la aplicacion

Este modulo define la clase `RegisterApp` que configura y gestiona 
la ruta de registro de usuarios dentro de la aplicacion Flask

Ejemplo
-------
>>> from flask import Flask
>>> from src.backend.python.routes.register import RegisterApp
>>> app = Flask(__name__)
>>> RegisterApp(app)
"""

from flask import render_template, request, flash
from werkzeug.security import generate_password_hash

# Importaciones propias
from ....db.database import DBConfig, Error
from ....security.autentication import authentication_required

class RegisterApp:
    """
    Clase para gestionar el registro de usuarios en la aplicacion Flask

    Esta clase configura la ruta de registro y maneja la logica para
    crear un nuevo usuario en la base de datos

    Atributos
    ---------
    register : Flask
        Instancia de la aplicacion Flask donde se registra la ruta de registro
    conn : mysql.connector.connection.MySQLConnection
        Conexion a la base de datos MySQL

    Metodos
    -------
    setup_routes()
        Configura la ruta de registro
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask

        Parametros
        ----------
        app : Flask
            Instancia de la aplicacion Flask donde se configurara la ruta de registro
        """
        self.register = app
        self.setup_routes()

        db = DBConfig()
        self.conn = db.get_db_config()
    
    def setup_routes(self):
        """
        Configura la ruta de registro

        Incluye la logica para registrar un nuevo usuario y gestionar 
        los mensajes de exito o error

        Returns
        -------
        None
        """

        @self.register.route('/admin/register', methods=['POST', 'GET'])
        @authentication_required
        def register():
            """
            Maneja la logica de registro de usuarios

            Si la solicitud es POST intenta registrar un nuevo usuario
            con las credenciales proporcionadas y gestiona los mensajes
            de exito o error

            Returns
            -------
            str
                Renderiza la plantilla 'auth/register.html'
            """
            if request.method == "POST":
                name = request.form.get('name').lower()
                passwd = request.form.get('passwd')
                email = request.form.get('email')
                rol = request.form.get('rol')
                hashed_passwd = generate_password_hash(passwd, method='pbkdf2:sha256')
                
                try:
                    with self.conn.cursor(dictionary=True) as cursor:
                        query = """
                        INSERT INTO users (name, password, email, rol) 
                        VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(query, (name, hashed_passwd, email, rol))
                        self.conn.commit()
                        self.conn.close()
                        flash("Usuario registrado exitosamente", "success")
                except Error as e:
                    flash("Ocurrio un error al registrar el usuario intente nuevamente")
                    print(e)
                except Exception as e:
                    flash("Ocurrio un error inesperado", "error")
                    print(f"Error general: {e}")
                finally:
                    if self.conn:
                        self.conn.close()
            return render_template('auth/register.html')