"""
Modulo de inicio de sesion de la aplicacion.

Este modulo define la clase `Login`, que configura y gestiona 
la ruta de inicio de sesion dentro de la aplicacion Flask.

Ejemplo:
--------
>>> from flask import Flask
>>> from src.backend.python.routes.login import Login
>>> app = Flask(__name__)
>>> Login(app)
"""

from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash

# Importaciones propias
from ....db.database import DBConfig, Error

class Login:
    """
    Clase para gestionar el inicio de sesion en la aplicacion Flask.

    Esta clase configura la ruta de inicio de sesion y maneja la
    logica para autenticar a los usuarios.

    Atributos
    ---------
    login : Flask
        Instancia de la aplicacion Flask donde se registra la ruta de inicio de sesion.
    conn : mysql.connector.connection.MySQLConnection
        Conexion a la base de datos MySQL.

    Metodos
    -------
    setup_routes()
        Configura la ruta de inicio de sesion.
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask.

        Parametros
        ----------
        app : Flask
            Instancia de la aplicacion Flask donde se configurara la ruta de inicio de sesion.
        """
        self.login = app
        self.setup_routes()

        # Configuracion db
        db = DBConfig()
        self.conn = db.get_db_config()
        

    def setup_routes(self):
        """
        Configura la ruta de inicio de sesion.

        Incluye la logica para autenticar a los usuarios y gestionar 
        los mensajes de exito o error.

        Returns
        -------
        None
        """

        @self.login.route('/login', methods=['GET', 'POST'])
        def login():
            """
            Maneja la logica de inicio de sesion.

            Si la solicitud es POST, intenta autenticar al usuario con las
            credenciales proporcionadas. En caso de exito, redirige al
            dashboard correspondiente; de lo contrario, muestra un mensaje
            de error.

            Returns
            -------
            str
                Renderiza la plantilla 'auth/login.html'.
            """
            if request.method == "POST":
                name = request.form.get('name').lower()
                passwd = request.form.get('passwd')

                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM users WHERE name = %s
                    """
                    cursor.execute(query, (name,))
                    USER = cursor.fetchone()

                    try:
                        if USER and check_password_hash(USER['password'], passwd):
                            flash("Usuario logueado exitosamente", "success")
                            session['user_id'] = USER['id']
                            session['user_name'] = USER['name']
                            session['rol'] = USER['rol']

                            if session['rol'] == 'admin':
                                return redirect(url_for('admin_dashboard'))
                        else:
                            flash("Credenciales incorrectas intentalo denuevo", "error")
                    except Error as e:
                        flash("Ocurrio un error. Por favor, intente nuevamente.", "error")
                        print(e)
                
                self.conn.close()

            return render_template('auth/login.html')