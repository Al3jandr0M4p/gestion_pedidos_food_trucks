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
    def __init__(self, app):
        """
        Inicializa AdminApp con Flask app.

        :param app: Flask app instancia.
        """
        self.admin = app

        db = DBConfig()
        self.conn = db.get_db_config()
        self.setup_routes()
    
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
            return render_template('admin/admin.html', section="dashboard")
        
        @self.admin.route('/admin/reports')
        @authentication_required
        def admin_reports():
            """
            Muestra la pagina de reportes administrativos.
            Redenriza la plantilla 'admin/reportes.html'.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/reportes.html')
            return render_template('admin/admin.html', section="reports")
        
        @self.admin.route('/admin/pedidos')
        def admin_pedidos():
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/pedidos.html')
            return render_template('admin/admin.html', section="pedidos")
        

        # CRUD de FoodTrucks
        @self.admin.route('/admin/foodtrucks')
        def foodtrucks():

            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM trucks
                    """
                    cursor.execute(query)
                    trucks = cursor.fetchall()
            
            except Error as e:
                print(f"Error al obtener los foodtrucks: {e}")
                flash(f"Error al obtener a los empleados: {e}", "error")
                return redirect(url_for('foodtrucks'))
            
            return render_template('admin/admin.html', section="foodtrucks", trucks=trucks)

        # CRUD de productos
        # Proximamente crud de productosn

        # CRUD de Empleados
        @self.admin.route('/admin/employees')
        @authentication_required
        def employee():

            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """ 
                    SELECT * FROM users WHERE estado = 'activo'
                    """
                    cursor.execute(query)
                    employees = cursor.fetchall()

                    query_disabled = """ 
                    SELECT * FROM user_desabilitados
                    """
                    cursor.execute(query_disabled)
                    employees_disabled = cursor.fetchall()
                    
            except Error as e:
                print(f"Error al obtener a los empleados: {e}")
                flash(f"Error al obtener a los empleados: {e}", "error")
                return redirect(url_for('employee'))

            return render_template('admin/admin.html', section="employees", employees=employees, employees_disabled=employees_disabled)
        
        @self.admin.route('/admin/employees/create_employee', methods=['GET', 'POST'])
        @authentication_required
        def create_employee():

            if request.method == "POST":

                name = request.form.get('nombre')
                password = request.form.get('password')
                email = request.form.get('email')
                rol = request.form.get('rol')
                password_hash = generate_password_hash(password, method='pbkdf2:sha256')

                try:
                    with self.conn.cursor() as cursor:
                        query = """
                        INSERT INTO users (name, password, email, rol)
                        VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(query, (name, password_hash, email, rol))
                        self.conn.commit()
                    
                    flash("Empleado creado exitosamente", "success")
                    return redirect(url_for('employee'))
                
                except Error as e:
                    flash(f"Error creando el empleado: {str(e)}", "error")

            return render_template('admin/admin.html', section="create_employee")

        @self.admin.route('/admin/employees/update_employee/<int:id>', methods=['GET', 'POST'])
        @authentication_required
        def update_employee(id):
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT id, name, email, rol
                    FROM users
                    WHERE id = %s
                    """
                    cursor.execute(query, (id,))
                    employee = cursor.fetchone()

                    if not employee:
                        flash("Empleado no encontrado", "error")
                        return redirect(url_for('employee'))

                    if request.method == "POST":
                        name = request.form.get('nombre')
                        password = request.form.get('password')
                        email = request.form.get('email')
                        rol = request.form.get('rol')

                        try:
                            with self.conn.cursor() as update_cursor:
                                if password:
                                    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
                                    query = """
                                    UPDATE users SET name = %s, password = %s, email = %s, rol = %s
                                    WHERE id = %s
                                    """
                                    update_cursor.execute(query, (name, password_hash, email, rol, id))
                                else:
                                    query = """
                                    UPDATE users 
                                    SET name = %s, email = %s, rol = %s
                                    WHERE id = %s
                                    """
                                    update_cursor.execute(query, (name, email, rol, id))

                                self.conn.commit()
                                flash("Usuario actualizado exitosamente", "success")
                                return redirect(url_for('employee'))
                        
                        except Error as e:
                            self.conn.rollback()
                            print(f"Error al actualizar el usuario: {e}")
                            flash(f"Error al actualizar el usuario: {e}", "error")
                    
                    return render_template('admin/admin.html', section="edit_employee", employee=employee)
            
            except Error as e:
                print(f"Error al obtener datos del empleado: {e}")
                flash(f"Error al obtener datos del empleado: {e}", "error")
                return redirect(url_for('employee'))
        
        @self.admin.route('/admin/employees/disable_employee/<int:id>')
        @authentication_required
        def disable_employee(id):
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query_employee = """
                    SELECT id, name, password, email, rol
                    FROM users
                    WHERE id = %s AND estado = 'activo'
                    """ 
                    cursor.execute(query_employee, (id,))
                    employee = cursor.fetchone()

                    if not employee:
                        flash("Empleado no encontrado o ya desabilitado", "error")
                        return redirect(url_for('employee'))
                    
                    insert_disabled = """
                    INSERT INTO user_desabilitados (id, name, password, email, rol, disabled_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                    """
                    cursor.execute(insert_disabled, (
                        employee['id'],
                        employee['name'],
                        employee['password'],
                        employee['email'],
                        employee['rol']
                    ))

                    update_user_status = """
                    UPDATE users
                    SET estado = 'inactivo'
                    WHERE id = %s
                    """
                    cursor.execute(update_user_status, (id,))

                    self.conn.commit()
                    flash("Empleado deshabilitado exitosamente", "success")
                    return redirect(url_for('employee'))
            except Error as e:
                self.conn.rollback()
                print(f"Error al intentar desabilitar un usuario: {e}")
                flash(f"Error al intentar desabilitar un usuario: {e}", "error")
                return redirect(url_for('employee'))
        
        @self.admin.route('/admin/employees/habilitar_employee/<int:id>')
        @authentication_required
        def habilitar_employee(id):
            try:

                with self.conn.cursor(dictionary=True) as cursor:
                    query_disabled = """ 
                    SELECT id, name, password, email, rol
                    FROM user_desabilitados
                    WHERE id = %s
                    """
                    cursor.execute(query_disabled, (id,))
                    employee_disabled = cursor.fetchone()

                    if not employee_disabled:
                        flash("Empleado no encontrado o ya habilitado", "success")

                    update_user_status = """
                    UPDATE users
                    SET estado = 'activo'
                    WHERE id = %s
                    """
                    cursor.execute(update_user_status, (id,))

                    delete_disabled = """
                    DELETE FROM user_desabilitados
                    WHERE id = %s
                    """
                    cursor.execute(delete_disabled, (id,))

                    self.conn.commit()
                    flash("Empleado habilitado exitosamente", "success")
                    return redirect(url_for('employee'))
                
            except Error as e:
                self.conn.rollback()
                print(f"Error al intentar habilitar un usuario: {e}")
                flash(f"Error al intentar habilitar un usuario: {e}", "error")
                return redirect(url_for('employee'))