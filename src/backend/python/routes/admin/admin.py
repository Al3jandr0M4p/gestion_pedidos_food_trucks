"""
Modulo de administracion de la aplicacion.

Este modulo define la clase `AdminApp`, que configura y gestiona
las rutas de administracion dentro de la aplicacion Flask.
"""

from flask import render_template, flash, redirect, url_for, session, request
from werkzeug.security import generate_password_hash

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
            return render_template('admin/admin.html')
        
        @self.admin.route('/admin/reports')
        @authentication_required
        def admin_reports():
            """
            Muestra la pagina de reportes administrativos.
            Redenriza la plantilla 'admin/reportes.html'.
            """
            return render_template('admin/reportes.html')

        # Seccion de Gestion
        @self.admin.route('/admin/gestion')
        @authentication_required
        def admin_gestion():
            """
            Muestra la pagina de gestion administrativa.
            Renderiza la plantilla 'admin/gestion.html'.
            """
            return render_template('admin/gestion.html')
        
        # CRUD de FoodTrucks

        # CRUD de Empleados
        @self.admin.route('/admin/employees')
        def employees():
            render_employees = self.get_employees()
            return render_template('/admin/employees.html', employees=render_employees)
        
        @self.admin.route('/admin/employees/create', methods=['GET', 'POST'])
        def create_employee():
            if request.method == "POST":
                nombre = request.form.get('nombre')
                password = request.form.get('password')
                email = request.form.get('email')
                rol = request.form.get('rol')

                result = self.insert_employee(nombre, password, email, rol)
                if result:
                    flash("Empleado creado exitosamente", "success")
                    return redirect(url_for('employees'))
                else:
                    flash("Error al crear el empleado", "danger")

            return render_template('/admin/crear_employees.html')
        
        @self.admin.route('/admin/employees/edit/<int:id>', methods=['GET', 'POST'])
        def edit_employee(id):
            if request.method == "POST":
                nombre = request.form.get('nombre')
                password = request.form.get('password')
                email = request.form.get('email')
                rol = request.form.get('rol')

                result = self.update_employee(id, nombre, password, email, rol)
                if result:
                    flash("Empleado actualizado con exito", "success")
                    return redirect(url_for("employees"))
                else:
                    flash("Error al actualizar al empleado", "danger")
            
            employee = self.get_employees_by_id(id)
            if employees:
                return render_template('/admin/edit_employee.html', employee=employee)

            flash("Empleado no encontrado", "danger")
            return redirect(url_for("employees"))
        
        @self.admin.route('/admin/employees/delete/<int:id>', methods=['POST'])
        def disable_employee(id):
            result = self.disable_employee(id)
            if result:
                flash("Empleado eliminado con exito", "success")
            else:
                flash("Error al eliminar el empleado", "danger")
            
            return redirect(url_for("employees"))
        
    def get_employees(self):
        try:

            with self.conn.cursor(dictionary=True) as cursor:
                query = """ 
                SELECT * FROM users
                """
                cursor.execute(query)
                employees = cursor.fetchall()
                return employees
            
        except Error as e:
            print(f"Error al obtener los usuarios: {e}")
    
    def get_employee_by_id(self, id):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                query = """
                SELECT * FROM users WHERE id = %s
                """
                cursor.execute(query, (id,))
                employee = cursor.fetchone()
                return employee
        
        except Error as e:
            print(f"Error al obtener el empleado: {str(e)}")
            return None

    def insert_employee(self, nombre, password, email, rol):
        try:
            with self.conn.cursor() as cursor:
                hashed_passsword = generate_password_hash(password)
                query = """
                INSERT INTO users (name, password, email, rol)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, hashed_passsword, email, rol))
                self.conn.commit()
                return True
        except Error as e:
            print(f"Error al insertar el empleado: {str(e)}")
            return False
    
    def update_employee(self, id, nombre, password, email, rol):
        try:
            with self.conn.cursor() as cursor:
                if password and password.strip():
                    hashed_password = generate_password_hash(password)
                    query = """
                    UPDATE users 
                    SET name = %s, password = %s, email = %s, rol = %s 
                    WHERE = %s
                    """
                    cursor.execute(query, (nombre, hashed_password, email, rol, id))
                else:
                    query = """
                    UPDATE users 
                    SET name = %s, email = %s, rol = %s 
                    WHERE = %s
                    """
                    cursor.execute(query, (nombre, email, rol, id))
                
                self.conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar el empleado: {str(e)}")
            return False
    
    def disable_employee(self, id):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                select_query = """
                SELECT * FROM users
                WHERE id = %s
                """
                cursor.execute(select_query, (id,))
                user_data = cursor.fetchone()

                if not user_data:
                    return False
                
                self.conn.start_transaction()

                insert_query = """
                INSERT INTO user_desabilitados (id, name, password, email, rol, updated_at, disabled_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (
                    user_data['id'],
                    user_data['name'],
                    user_data['password'],
                    user_data['email'],
                    user_data['rol'],
                    user_data.get('created_at'),
                    user_data.get('updated_at')
                ))

                delete_query = """
                DELETE FROM users
                WHERE id = %s
                """
                cursor.execute(delete_query, (id,))
                self.conn.commit()
                return True
        
        except Error as e:
            self.conn.rollback()
            print(f"Error al deshabilitar el empleado: {str(e)}")
            return False