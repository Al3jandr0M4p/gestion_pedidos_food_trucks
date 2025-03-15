"""
Modulo de administracion de la aplicacion.

Este modulo define la clase `AdminApp`, que configura y gestiona
las rutas de administracion dentro de la aplicacion Flask.
"""

from flask import render_template, jsonify, session, request

# importaciones propias
from ....security.autentication import authentication_required
from ....db.database import DBConfig, Error

class AdminApp:
    """
    Clase para gestionar la administracion de la aplicacion Flask.

    Esta clase configura las rutas del panel de administracion,
    la gestion de empleados y el sistema de reportes.

    Atributos:
    ----------
    admin : Flask
        Instancia de la aplicacion Flask donde se registran las rutas.
    conn : mysql.connector.connection.MySQLConnection
        Conexion a la base de datos MySQL.

    Metodos:
    -------
    setup_routes()
        Configura las rutas del panel de administracion
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask.

        Parametros:
        ----------
        app = Flask
            Instancia de la aplicacion Flask donde se configuraran las rutas.
        """
        self.admin = app
        self.setup_routes()

        db = DBConfig()
        self.conn = db.get_db_config()
    
    def setup_routes(self):
        """
        Confifura las rutas del panel de administracion.
        Incluye rutas para el dashboard, reportes, gestion y CRUD de empleados.
        """

        @self.admin.route('/admin')
        @authentication_required
        def admin_dashboard():
            """
            Muestra el dashboard de administracion.
            Renderiza la plantilla 'admin/admin.html'.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/dashboard.html')
            return render_template('admin/admin.html', name=session.get('user_name'))
        
        @self.admin.route('/admin/reports')
        @authentication_required
        def admin_reports():
            """
            Muestra la pagina de reportes administrativos.
            Redenriza la plantilla 'admin/reportes.html'.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/reportes.html')
            return render_template('admin/admin.html', name=session.get('user_name'))

        # Seccion de Gestion
        @self.admin.route('/admin/gestion')
        @authentication_required
        def admin_gestion():
            """
            Muestra la pagina de gestion administrativa.
            Renderiza la plantilla 'admin/gestion.html'.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/gestion.html')
            return render_template('admin/admin.html', name=session.get('user_name'))

        # CRUD de los empleados
        @self.admin.route('/admin/gestion/employees')
        @authentication_required
        def admin_gestion_employees():
            """
            Obtiene y muestra la lista de empleados desde la base de datos.

            Returns:
            --------
            str
                Renderiza la plantilla 'admin/employees.html' con la lista de empleados.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                try:
                    with self.conn.cursor(dictionary=True) as cursor:
                        cursor.execute("SELECT * FROM users")
                        employees = cursor.fetchall()
                except Error as e:
                    print(f"Error al obtener los datos: {e}")
                return render_template('admin/employees.html', employees=employees)
            return render_template('admin/admin.html', name=session.get('user_name'))

        # Delete / Desactivar
        @self.admin.route('/admin/gestion/employees/toggle_status/<int:user_id>', methods=['POST'])
        @authentication_required
        def toggle_employee_status(user_id):
            """
            Cambia el estado de un empleado (activo/inactivo).

            Parametros:
            ----------
            user_id : int
                ID del empleado cuyo estado se cambiara.
            
            Returns:
            --------
            Response
                Respuesta en formato JSON indicando exito o error.
            """

            try:
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT estado FROM users WHERE id = %s", (user_id,))
                    self.conn.commit()
                    employee = cursor.fetchone()

                    if not employee:
                        return jsonify({"success": False, "error": "Empleado no encontrado"}), 404

                    new_status = "inactivo" if employee[0] == "activo" else "activo"

                    cursor.execute("UPDATE users SET estado = %s WHERE id = %s", (new_status, user_id))
                    self.conn.commit()

                return jsonify({"success": True, "new_status": new_status})

            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
            
            except Error as e:
                print(f"Error al actualizar los datos del los empleados/Usuarios: {e}")