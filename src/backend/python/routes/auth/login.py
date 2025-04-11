"""
Modulo de inicio de sesion de la aplicacion.

Este modulo define la clase `Login`, que configura y gestiona 
la ruta de inicio de sesion dentro de la aplicacion Flask.
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
    """
    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask
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
        """

        @self.login.route('/login', methods=['GET', 'POST'])
        def login():
            """
            Maneja la logica de inicio de sesion.
            """
            if request.method == "POST":
                name = request.form.get('name').lower()
                passwd = request.form.get('passwd')

                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM users WHERE name = %s
                    """
                    cursor.execute(query, (name,))
                    employee = cursor.fetchone()

                    print("Employee: ", employee)

                    try:
                        if employee:
                            if employee['estado'] == 'inactivo':
                                flash("Tu cuenta ha sido deshabilitada. Contacta con el administrador", "error")
                                return redirect(url_for('login'))
                            
                        if check_password_hash(employee['password'], passwd):

                            flash("Usuario logueado exitosamente", "success")
                            session['user_id'] = employee['id']
                            session['user_name'] = employee['name']
                            session['rol'] = employee['rol']

                            if session['rol'] == 'admin':
                                return redirect(url_for('admin_dashboard'))
                        else:
                            flash("Credenciales incorrectas intentalo denuevo", "error")

                    except Error as e:
                        flash("Ocurrio un error. Por favor, intente nuevamente.", "error")
                        print("Ocurrio un error. Por favor, intente nuevamente.", str(e))

            return render_template('auth/login.html')