"""
Modulo de administracion de la aplicacion.

Este modulo define la clase `AdminApp`, que configura y gestiona
las rutas de administracion dentro de la aplicacion Flask.
"""

from flask import render_template, flash, redirect, url_for, send_file, jsonify, session, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from io import BytesIO
import requests
import os
import pdfkit

# importaciones propias
from ....security.autentication import authentication_required
from ....db.database import DBConfig, Error
from ...utils.report_utils import obtener_reportes_generales

class AdminApp:
    # carpeta donde se guardaran las imagenes y las extenciones permitidas
    UPLOAD_FOLDER = r'static\uploads'
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

    def __init__(self, app):
        """
        Inicializa AdminApp con Flask app.

        :param app: Flask app instancia.
        """
        self.admin = app

        # configuracion de la db
        db = DBConfig()
        self.conn = db.get_db_config()

        # Correr las rutas de la app
        self.setup_routes()
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
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
            return render_template('admin/admin.html', name=session.get('user_name'), section="dashboard")
        
        @self.admin.route('/admin/reports')
        @authentication_required
        def admin_reports():
            """
            Muestra la pagina de reportes administrativos.
            Redenriza la plantilla 'admin/reportes.html'.
            """
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                data = obtener_reportes_generales()
                print("data", data)
                return jsonify(data)
            
            data = obtener_reportes_generales()
            return render_template('admin/admin.html', section="reports", data=data)
        
        @self.admin.route('/admin/reports/pdf')
        @authentication_required
        def descargar_reporte_pdf():
            rendered = render_template("admin/reportes_pdf.html", data=obtener_reportes_generales())

            try:
                path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)   
            except OSError as e:
                return f"Error generando PDF: {e}", 500         

            pdf = pdfkit.from_string(rendered, False, configuration=config)
            return send_file(BytesIO(pdf), as_attachment=True, download_name="reporte_ventas.pdf")
        
        @self.admin.route('/admin/pedidos')
        @authentication_required
        def admin_pedidos():
            try:
                response = requests.get(f"{request.host_url}api/pedidos")
                pedidos = response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"Error al obtener pedidos: {str(e)}")
                pedidos = []

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template('admin/pedidos.html', pedidos=pedidos)
            return render_template('admin/admin.html', section="pedidos", pedidos=pedidos)

        # CRUD de FoodTrucks
        @self.admin.route('/admin/foodtrucks')
        @authentication_required
        def foodtrucks():
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM trucks
                    """
                    cursor.execute(query)
                    trucks = cursor.fetchall()

                    disabled_trucks = """
                    SELECT *
                    FROM trucks_desabilitados
                    """
                    cursor.execute(disabled_trucks)
                    disabled_foodtrucks = cursor.fetchall()
            
            except Error as e:
                print(f"Error al obtener los foodtrucks: {e}")
                flash(f"Error al obtener a los empleados: {e}", "error")
                return redirect(url_for('foodtrucks'))
            
            return render_template('admin/admin.html', section="foodtrucks", trucks=trucks, disabled_foodtrucks=disabled_foodtrucks)
        
        @self.admin.route('/admin/foodtrucks/create_trucks', methods=['GET', 'POST'])
        @authentication_required
        def create_trucks():
            if request.method == "POST":

                nombre_truck = request.form.get('nombreTrucks')
                imagen_trucks = request.files.get('imagenTrucks')
                info_truck = request.form.get('informacionTrucks')
                especialidad_truck = request.form.get('especialidadTrucks')

                if imagen_trucks and self.allowed_file(imagen_trucks.filename):
                    filename = secure_filename(imagen_trucks.filename)
                    os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
                    filepath = os.path.join(self.UPLOAD_FOLDER, filename)
                    imagen_trucks.save(filepath)

                    try:
                        with self.conn.cursor() as cursor:
                            query = """ 
                            INSERT INTO trucks (nombre_truck, imagen_foodtruck, info_foodtruck, especialidad)
                            VALUES (%s, %s, %s, %s)
                            """
                            cursor.execute(query, (nombre_truck, filepath, info_truck, especialidad_truck))
                            self.conn.commit()
                        
                        flash("Food trucks creado exitosamente!", "success")
                        return redirect(url_for('foodtrucks'))
                    
                    except Error as e:
                        print("No se pudo crear el food trucks")
                        flash(f"No se pudo crear el food trucks {str(e)}", "error")
            
            return render_template('/admin/admin.html', section="create_trucks")
        
        @self.admin.route('/admin/foodtrucks/update_trucks/<int:id>', methods=['GET', 'POST'])
        @authentication_required
        def update_trucks(id):
            with self.conn.cursor(dictionary=True) as cursor:
                query = """
                SELECT *
                FROM trucks
                WHERE id = %s
                """
                cursor.execute(query, (id,))
                trucks = cursor.fetchone()

                if not trucks:
                    flash("Truck no encontrado", "error")
                    return redirect(url_for('foodtrucks'))

                if request.method == "POST":

                    nombre_truck = request.form.get('nombreTrucks')
                    imagen_trucks = request.form.get('imagenTrucks')
                    info_truck = request.form.get('informacionTrucks')
                    especialidad_truck = request.form.get('especialidadTrucks')
                    
                    if imagen_trucks and self.allowed_file(imagen_trucks.filename):
                        filename = secure_filename(imagen_trucks.filename)
                        filepath = os.path.join(self.UPLOAD_FOLDER, filename)
                        imagen_trucks.save(filepath)

                        try:
                            with self.conn.cursor() as update_cursor:
                                query = """
                                UPDATE trucks 
                                SET nombre_truck = %s, imagen_foodtrucks = %s, info_foodtruck = %s, especialidad = %s
                                WHERE id = %s
                                """
                                update_cursor.execute(query, (nombre_truck, filepath, info_truck, especialidad_truck))
                                self.conn.commit()
                            
                            flash("Truck actualizado exitosamente!", "success")
                            return redirect(url_for('foodtrucks'))
                        
                        except Error as e:
                            print(f"Error al actualizar el truck!: {str(e)}")
                            flash(f"Error al actualizar el truck!: {str(e)}", "error")

            return render_template('/admin/admin.html', section="update_trucks", trucks=trucks)

        @self.admin.route('/admin/foodtrucks/desabilitar_trucks/<int:id>', methods=['GET', 'POST'])
        @authentication_required
        def deshabilitar_trucks(id):
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    select_query = """
                    SELECT id, nombre_truck, imagen_foodtruck, info_foodtruck, especialidad
                    FROM trucks
                    WHERE id = %s
                    """
                    cursor.execute(select_query, (id,))
                    truck = cursor.fetchone()

                    if not truck:
                        flash("Truck no encontrado", "error")
                        return redirect(url_for('foodtrucks'))
                    
                    insert_query = """
                    INSERT INTO trucks_desabilitados (id, nombre_truck, imagen_foodtruck, info_foodtruck, especialidad)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (truck["id"], truck["nombre_truck"], truck["imagen_foodtruck"], truck["info_foodtruck"], truck["especialidad"]))
                    
                    delete_query = """
                    DELETE FROM trucks WHERE id = %s
                    """
                    cursor.execute(delete_query, (id,))
                    
                self.conn.commit()
                flash("Truck deshabilitado exitosamente!", "success")
            except Error as e:
                print(f"Error al habilitar el truck!: {str(e)}")
                flash(f"Error al habilitar el truck!: {str(e)}", "error")

            return redirect(url_for('foodtrucks'))

        @self.admin.route('/admin/foodtrucks/habilitar_trucks/<int:id>', methods=['GET', 'POST'])
        @authentication_required
        def habilitar_trucks(id):
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    select_query = """
                    SELECT id, nombre_truck, imagen_foodtruck, info_foodtruck, especialidad
                    FROM trucks_desabilitados
                    WHERE id = %s
                    """
                    cursor.execute(select_query, (id,))
                    truck = cursor.fetchone()
                    
                    if not truck:
                        flash("Truck no encontrado en la lista de deshabilitados", "error")
                        return redirect(url_for('foodtrucks'))
                    
                    insert_query = """
                    INSERT INTO trucks (id, nombre_truck, imagen_foodtruck, info_foodtruck, especialidad, estado_truck)
                    VALUES (%s, %s, %s, %s, %s, 'activo')
                    """
                    cursor.execute(insert_query, (truck["id"], truck["nombre_truck"], truck["imagen_foodtruck"], truck["info_foodtruck"], truck["especialidad"]))
                    
                    delete_query = """
                    DELETE FROM trucks_desabilitados WHERE id = %s
                    """
                    cursor.execute(delete_query, (id,))
                    self.conn.commit()
                flash("Truck habilitado exitosamente!", "success")

            except Error as e:
                print(f"Error al habilitar el truck!: {str(e)}")
                flash(f"Error al habilitar el truck!: {str(e)}", "error")
            
            return redirect(url_for('foodtrucks'))
        
        # CRUD de productos
        @self.admin.route('/admin/products/<int:truck_id>')
        @authentication_required
        def products(truck_id):
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query_truck = """
                    SELECT * FROM trucks
                    """
                    cursor.execute(query_truck)
                    trucks = cursor.fetchall()

                    if truck_id:
                        query = """
                        SELECT * FROM productos WHERE truck_id = %s
                        """
                        cursor.execute(query, (truck_id,))
                        productos = cursor.fetchall()

                        query_truck = """
                        SELECT * FROM trucks WHERE id = %s
                        """
                        cursor.execute(query_truck, (truck_id,))
                        trucks = cursor.fetchall()
                    else:
                        query_truck = """
                        SELECT * FROM trucks
                        """
                        cursor.execute(query_truck)
                        trucks = cursor.fetchall()

                        query = """
                        SELECT * FROM productos
                        """
                        cursor.execute(query)
                        productos = cursor.fetchall()

            except Error as e:
                print(f"Error al obtener los productos: {str(e)}")
                flash(f"Error al obtener los productos: {str(e)}", "error")
                return redirect(url_for('products'))

            return render_template(
                'admin/admin.html', 
                section="products", 
                productos=productos,
                trucks=trucks,
                truck_id_selected=truck_id
            )

        @self.admin.route('/admin/products/create_product/<int:id>', methods=['GET', 'POST'])
        @authentication_required
        def create_products(id):
            if request.method == "POST":
                nombre_products = request.form.get("productName")
                imagen_products = request.form.get('imagenProducts')
                descripcion_products = request.form.get("descriptionProducts")
                products_price = request.form.get("PrecioProducts")
                truck_id = id

                if imagen_products and self.allowed_file(imagen_products.filename):
                    filename = secure_filename(imagen_products.filename)
                    filepath = os.path.join(self.UPLOAD_FOLDER, filename)
                    imagen_products.save(filepath)

                    with self.conn.cursor(dictionary=True) as cursor:
                        query = """
                        INSERT INTO (nombre_producto, descripcion, precio, imagen_producto, truck_id)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (nombre_products, descripcion_products, products_price, filepath, truck_id))
                        self.conn.commit()
                    
                    flash("Productos creado exitosamente!", "success")
                    return redirect(url_for("products"))

            return render_template(
                'admin/admin.html',
                section='create_products'
            )
        
        @self.admin.route('/admin/products/update_product/<int:id>', methods=['GET', 'POST'])
        def update_products(id):
            pass

        @self.admin.route('/admin/products/disabled_products/<int:id>', methods=['GET', 'POST'])
        def disabled_products(id):
            pass

        @self.admin.route('/admin/products/allowed_products/<int:id>', methods=['GET', 'POST'])
        def allowed_products(id):
            pass

        @self.admin.route('/admin/products/descuentos_products/<int:id>', methods=['GET', 'POST'])
        def descuestos_products(id):
            pass

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

            return render_template(
                'admin/admin.html', 
                section="employees", 
                employees=employees, 
                employees_disabled=employees_disabled
            )
        
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

            return render_template(
                'admin/admin.html', 
                section="create_employee"
            )

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
                    
                    return render_template(
                        'admin/admin.html', 
                        section="edit_employee", 
                        employee=employee
                    )
            
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
                    cursor.execute(insert_disabled, (employee['id'],employee['name'],employee['password'],employee['email'],employee['rol']))

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