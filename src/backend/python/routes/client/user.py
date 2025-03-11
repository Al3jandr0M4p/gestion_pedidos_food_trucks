"""
Modulo de gestion de usuarios de la aplicacion

Este modulo define la clase `UserApp` que configura y gestiona 
las rutas relacionadas con los usuarios en la aplicacion Flask

Ejemplo
-------
>>> from flask import Flask
>>> from src.backend.python.routes.user import UserApp
>>> app = Flask(__name__)
>>> UserApp(app)
"""

from flask import render_template, url_for, redirect, send_file, session, request
from io import BytesIO
import qrcode
import concurrent.futures

# Importaciones propias
from ....db.database import DBConfig, Error

class UserApp:
    """
    Clase para gestionar las rutas de usuario en la aplicacion Flask

    Esta clase configura las rutas para la generacion de codigos QR,
    asignacion de mesas y visualizacion de menus de foodtrucks

    Atributos
    ---------
    user : Flask
        Instancia de la aplicacion Flask donde se registran las rutas
    conn : mysql.connector.connection.MySQLConnection
        Conexion a la base de datos MySQL
    executor : concurrent.futures.ThreadPoolExecutor
        Executor para manejar tareas en segundo plano

    Metodos
    -------
    setup_routes()
        Configura las rutas de la aplicacion
    get_food_trucks()
        Obtiene la lista de foodtrucks de la base de datos
    assign_mesa_task()
        Asigna una mesa a un usuario en segundo plano
    """

    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask

        Parametros
        ----------
        app : Flask
            Instancia de la aplicacion Flask donde se configuraran las rutas
        """
        self.user = app
        self.setup_routes()

        # Configuracion de la DB
        db_config = DBConfig()
        self.conn = db_config.get_db_config()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def setup_routes(self):
        """
        Configura las rutas de la aplicacion

        Incluye la logica para generar codigos QR, asignar mesas 
        y mostrar el menu de foodtrucks

        Returns:
        -------
        None
        """

        @self.user.route('/')
        def qrcode_route():
            """
            Genera un codigo QR para la asignacion de mesas

            Returns:
            -------
            str
                Renderiza la plantilla 'client/user.html' con el 
                codigo QR y la URL de asignacion de mesa.
            """
            # target_url = "https://74zb1whg-5000.use2.devtunnels.ms/user/assign_mesa"
            target_url = "https://74zb1whg-5000.use2.devtunnels.ms/user/splash"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(target_url)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="qr.png")
            return "<b>Ya el qrcode ya fue entregado.<b>"
        
        @self.user.route('/user/menu/<mesa_id>')
        def menu_user(mesa_id):
            """
            Muestra el menu de foodtrucks para una mesa especifica

            Parametros:
            -----------
            mesa_id : str
                ID de la mesa

            Returns:
            --------
            str
                Renderiza la plantilla 'client/menu.html' con la 
                informacion de los foodtrucks
            """
            if not mesa_id.isdigit():
                return render_template('errors/404.html'), 404
            
            print("mesa_id:", mesa_id)
            
            foodtrucks = self.get_food_trucks()
            print("Foodtrucks:", foodtrucks)

            session['foodtrucks'] = foodtrucks

            return render_template('client/menu.html', mesa_id=int(mesa_id), foodtrucks=foodtrucks)
        
        @self.user.route('/user/menu/foodtruck/<int:foodtruck_id>')
        def menu_foodtruck(foodtruck_id):
            """
            Muestra el menú de un food truck específico

            Parámetros:
            -----------
            foodtruck_id : int
                ID del food truck

            Returns:
            --------
            str
                Renderiza la plantilla 'client/menu_foodtruck.html' con los productos del food truck
            """
            with self.conn.cursor(dictionary=True) as cursor:
                try:
                    query = """
                    SELECT * FROM productos WHERE truck_id = %s
                    """
                    cursor.execute(query, (foodtruck_id,))
                    productos = cursor.fetchall()
                    self.conn.commit()
                    
                    return render_template('client/menu_foodtruck.html', productos=productos)
                
                except Error as e:
                    print(f"Error al obtener productos: {e}")
                    return render_template('errors/500.html'), 500
        
        @self.user.route('/user/splash')
        def splash_screen():
            return render_template('client/splash.html')

        @self.user.route('/ver-carrito')
        def ver_carrito():
            return render_template('client/carrito.html')
        
        @self.user.route('/seleccionar-pago')
        def select_payment():
            return render_template('client/seleccionar_pago.html')

        @self.user.route('/user/assign_mesa')
        def assign_mesa():
            """
            Asigna una mesa a un usuario y redirige al menu

            Returns:
            --------
            str
                Redirige a la ruta del menu del usuario
            """
            mesa_asignada = session.get('mesa_asignada')
            if mesa_asignada:
                return redirect(url_for('menu_user', mesa_id=mesa_asignada))

            future = self.executor.submit(self.assign_mesa_task)
            mesa_id = future.result()

            if isinstance(mesa_id, int):
                session['mesa_asignada'] = mesa_id
                return redirect(url_for('menu_user', mesa_id=mesa_id))
            
            return mesa_id

    def assign_mesa_task(self):
        """
        Asigna una mesa a un usuario en segundo plano.

        Returns
        -------
        int or str
            ID de la mesa asignada o mensaje de error
        """
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute("CALL asignar_mesa();")
                mesa = cursor.fetchone()

                while cursor.nextset():
                    pass

                if mesa and 'mesa_asignada' in mesa:
                    self.conn.commit()
                    return mesa['mesa_asignada']
                else:
                    return "No hay mesas disponibles"

        except Error as e:
            if self.conn:
                self.conn.rollback()
            return f"Error en la asignación de la mesa: {str(e)}"
    
    # CRUD FOODTRUCKS
    def get_food_trucks(self):
        """
        Obtiene la lista de foodtrucks de la base de datos

        Returns
        -------
        list
            Lista de foodtrucks obtenidos de la base de datos
        """

        with self.conn.cursor(dictionary=True) as cursor:
            try:
                query = """
                SELECT * FROM trucks
                """
                cursor.execute(query)
                foodtrucks = cursor.fetchall()
                self.conn.commit()
                return foodtrucks

            except Error as e:
                print(f"Error en la forma de obtener los foodtrucks: {e}")
                return f"Error al obtener los foodtrucks: {e}"

            except Exception as e:
                print(f"Hubo un error en los foodtrucks: {e}")
                return e