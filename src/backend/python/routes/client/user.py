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

from flask import render_template, url_for, redirect, send_file, jsonify, flash, session, request
from io import BytesIO
from datetime import datetime

import concurrent.futures
import qrcode
import os
import uuid
import json
import stripe

# Importaciones propias
from ....db.database import DBConfig, Error
from ...utils.mail_utils import enviar_correo


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
        
        @self.user.route('/procesar-pago', methods=['POST'])
        def procesar_pago():
            metodo_pago = request.form.get('metodo_pago')
            mesa_id = session.get('mesa_asignada')
            carrito = request.form.get('carrito')

            if not mesa_id:
                flash('Error: No hay mesas asignada')
                return redirect(url_for('ver_carrito'))
            
            if not carrito:
                carrito = session.get('carrito', '[]')
            
            if isinstance(carrito, str):
                carrito = json.loads(carrito)
            
            total = sum(item.get('precio', 0) * item.get('cantidad', 0) for item in carrito)

            transaccion_id = str(uuid.uuid4())
            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d %H:%M:%S")

            try:
                if metodo_pago == "tarjeta":
                    return self.procesar_pago_tarjeta(mesa_id, carrito, total, transaccion_id, fecha)
                elif metodo_pago == 'transferencia':
                    return self.procesar_pago_transferencia(mesa_id, carrito, total, transaccion_id, fecha)
                elif metodo_pago == 'criptos':
                    return self.procesar_pago_cripto(mesa_id, carrito, total, transaccion_id, fecha)
                elif metodo_pago == 'efectivo':
                    return self.procesar_pago_efectivo(mesa_id, carrito, total, transaccion_id, fecha)
                else:
                    flash('Método de pago no válido')
                    return redirect(url_for('select_payment'))
            
            except Exception as e:
                flash(f'Error al procesar el pago: {str(e)}')
                return redirect(url_for('select_payment'))
        
        @self.user.route('/comfirmacion-pago/<transaccion_id>')
        def confirmacion_pago(transaccion_id):

            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM transacciones 
                    WHERE id = %s
                    """
                    cursor.execute(query, (transaccion_id,))
                    transaccion = cursor.fetchone()

                    if not transaccion:
                        print('Transacción no encontrada')
                        flash('Transacción no encontrada')
                        return redirect(url_for('menu_user', mesa_id=session.get('mesa_asignada')))
                    
                    query_detalles = """ 
                    SELECT td.*, p.nombre_producto as nombre_completo
                    FROM transaccion_detalles td
                    JOIN productos p ON td.producto_id = p.id
                    WHERE td.transaccion_id = %s
                    """
                    cursor.execute(query_detalles, (transaccion_id,))
                    detalles = cursor.fetchall()

                    metodo_pago = transaccion.get('metodo_pago')
                    instrucciones = None
                    datos_adiccionales = None

                    if transaccion.get('datos_adicionales'):
                        try:
                            datos_adicionales = json.loads(transaccion['datos_adicionales'])
                        except json.JSONDecodeError:
                            datos_adiccionales = {}
                        
                    if metodo_pago == 'transferencia':
                        instrucciones = session.get('instrucciones_bancarias')
                        if not instrucciones and datos_adiccionales:
                            instrucciones = datos_adiccionales.get('instrucciones_bancarias')
                    elif metodo_pago == 'cripto':
                        instrucciones = session.get('instrucciones_crypto')
                        if not instrucciones and datos_adicionales:
                            instrucciones = datos_adicionales.get('instrucciones_crypto')

                    return render_template(
                        'client/confirmacion_pago.html',transaccion=transaccion, 
                        detalles=detalles, instrucciones=instrucciones,
                        datos=datos_adiccionales, 
                        metodo_pago=metodo_pago
                    )
                
            except Exception as e:
                print(f'Error al mostrar la confirmación: {str(e)}')
                flash(f'Error al mostrar la confirmación: {str(e)}')
                return redirect(url_for('menu_user', mesa_id=session.get('mesa_asignada')))

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
    
    def procesar_pago_tarjeta(self, mesa_id, carrito, total, transaccion_id, fecha):
        try:
            stripe.api_key = os.getenv('PRIVATE_KEY')

            token = request.form.get('stripeToken')
            nombre = request.form.get('nombreUsuario')

            if not token:
                print('Error: No se recibió el token de pago')
                flash('Error: No se recibió el token de pago')
                return redirect(url_for('seleccionar_pago'))
            
            charge = stripe.Charge.create(
                amount=int(total * 100),
                currency="usd",
                source=token,
                description=f"Pago de mesa {mesa_id}"
            )

            with self.conn.cursor() as cursor:
                query = """ 
                INSERT INTO transacciones (id, mesa_id, metodo_pago, monto, estado, fecha)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (transaccion_id, mesa_id, 'tarjeta', total, 'completado', fecha))

                for item in carrito:
                    query_detalle = """
                    INSERT INTO transaccion_detalles (transaccion_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (transaccion_id, item.get('id'), item.get('cantidad'), item.get('precio')))

                self.conn.commit()
            
            session.pop('carrito', None)

            print('Pago con tarjeta procesado exitosamente')
            flash('Pago con tarjeta procesado exitosamente')
            return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))
        
        except stripe.error.StripeError as e:
            self.conn.rollback()
            print(f'Error en el pago con tarjeta: {str(e)}')
            flash(f'Error en el pago con tarjeta: {str(e)}')
            return redirect(url_for('seleccionar_pago'))

        except Exception as e:
            self.conn.rollback()
            print(f'Error al procesar el pago: {str(e)}')
            flash(f'Error al procesar el pago: {str(e)}')
            return redirect(url_for('seleccionar_pago'))
    
    def procesar_pago_transferencia(self, mesa_id, carrito, total, transaccion_id, fecha):
        try:
            stripe.api_key = os.getenv("PRIVATE_KEY")

            nombre = request.form.get('nombreUsuario')
            correo = request.form.get('correo')

            customer = stripe.Customer.create(
                name=nombre,
                email=correo,
                description=f"Cliente para mesa {mesa_id}"
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency="usd",
                customer=customer.id,
                payment_method_types=["customer_balance"],
                payment_method_data={
                    "type": "customer_balance",
                },
                payment_method_options={
                    "customer_balance": {
                        "funding_type": "bank_transfer",
                        "bank_transfer": {
                            "type": "us_bank_transfer"
                        }
                    }
                }
            )

            payment_intent = stripe.PaymentIntent.retrieve(
                payment_intent.id,
                expand=["next_action"]
            )
            
            instrucciones_bancarias = None
            if (hasattr(payment_intent, 'next_action') and 
            payment_intent.next_action is not None and 
            hasattr(payment_intent.next_action, 'display_bank_transfer_instructions')):
                instrucciones_bancarias = payment_intent.next_action.display_bank_transfer_instructions
            
            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO transacciones (id, mesa_id, metodo_pago, monto, estado, fecha, datos_adicionales)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                bank_instructions = None
                if (hasattr(payment_intent, 'next_action') and 
                payment_intent.next_action is not None and 
                hasattr(payment_intent.next_action, 'display_bank_transfer_instructions')):
                    bank_instructions = payment_intent.next_action.display_bank_transfer_instructions

                datos_adicionales = json.dumps({
                    'nombre': nombre,
                    'stripe_payment_intent_id': payment_intent.id,
                    'stripe_customer_id': customer.id,
                    'instrucciones_bancarias': (
                        payment_intent.next_action.display_bank_transfer_instructions 
                        if hasattr(payment_intent, 'next_action') and hasattr(payment_intent.next_action, 'display_bank_transfer_instructions')
                        else None
                    )
                })

                session['instrucciones_bancarias'] = (
                    payment_intent.next_action.display_bank_transfer_instructions 
                    if hasattr(payment_intent, 'next_action') and hasattr(payment_intent.next_action, 'display_bank_transfer_instructions')
                    else None
                )

                cursor.execute(query, (transaccion_id, mesa_id, 'tranferencia', total, 'pendiente', fecha, datos_adicionales))

                for item in carrito:
                    query_detalle = """ 
                    INSERT INTO transaccion_detalles (transaccion_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (transaccion_id, item.get('id'), item.get('cantidad'), item.get('precio')))
                
                self.conn.commit()

            session['payment_intent_id'] = payment_intent.id
            session['instrucciones_bancarias'] = payment_intent.next_action.display_bank_transfer_instructions if hasattr(payment_intent, 'next_action') else None
            session.pop('carrito', None)

            if correo:
                self.enviar_factura_por_correo(correo, nombre, mesa_id, carrito, total, transaccion_id, fecha)

            print('Transferencia registrada. Pendiente de verificación.')
            flash('Transferencia registrada. Pendiente de verificación.')
            return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))
        
        except stripe.error.StripeError as e:
            self.conn.rollback()
            print(f'Error de Stripe al procesar transferencia: {str(e)}')
            flash(f'Error al procesar la transferencia: {str(e)}')
            return redirect(url_for('seleccionar_pago'))
        
        except Exception as e:
            self.conn.rollback()
            print(f'Error al procesar la transferencia: {str(e)}')
            flash(f'Error al procesar la transferencia: {str(e)}')
            return redirect(url_for('seleccionar_pago'))
    
    def procesar_pago_cripto(self, mesa_id, carrito, total, transaccion_id, fecha):
        try:

            stripe.api_key = os.getenv("PRIVATE_KEY")

            nombre = request.form.get('nombreUsuario', 'Cliente')
            correo = request.form.get('correo')
            cripto_seleccionada = request.form.get('crypto', 'bitcoin')

            customer = stripe.Customer.create(
                name=nombre,
                email=correo,
                description=f"Cliente para mese {mesa_id} - Pago cripto"
            )

            cripto_mapping = {
                'bitcoin': 'bitcoin',
                'ethereum': 'ethereum',
                'litecoin': 'litecoin',
                'usdc': 'usdc'
            }

            cripto_stripe = cripto_mapping.get(cripto_seleccionada.lower(), 'bitcoin')

            payment_intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency="usd",
                customer=customer.id,
                payment_method_types=['crypto'],
                payment_method_data={
                    'type': "crypto",
                    "crypto": {
                        "currency": cripto_stripe
                    }
                },
                payment_method_options={
                    "crypto": {
                        "currency": cripto_stripe
                    }
                }
            )

            payment_intent = stripe.PaymentIntent.retrieve(
                payment_intent.id,
                expand=["next_action"]
            )

            comprobante_url = None
            if 'proof' in request.files:
                archivo = request.files['proof']
                if archivo and archivo.filename:
                    filename = f"{transaccion_id}_{archivo.filename}"
                    filepath = os.path.join('static/uploads/comprobantes', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    archivo.save(filepath)
                    comprobante_url = f"/static/uploads/comprobantes/{filename}"

            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO transacciones (id, mesa_id, metodo_pago, monto, estado, fecha, datos_adicionales)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                crypto_instructions = None
                if (hasattr(payment_intent, 'next_action') and payment_intent.next_action is not None and hasattr(payment_intent.next_action, 'crypto_deposit')):
                    crypto_instructions = payment_intent.next_action.crypto_deposit

                datos_adicionales = json.dumps({
                    'cripto': cripto_seleccionada,
                    'stripe_payment_intent_id': payment_intent.id,
                    'stripe_customer_id': customer.id,
                    'comprobante': comprobante_url,
                    'instrucciones_crypto': crypto_instructions
                })

                cursor.execute(query, (transaccion_id, mesa_id, 'cripto', total, 'pendiente', fecha, datos_adicionales))

                for item in carrito:
                    query_detalle = """
                    INSERT INTO transaccion_detalles (transaccion_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (transaccion_id, item.get('id'), item.get('cantidad'), item.get('precio')))
                
                self.conn.commit()
            
            session['payment_intent_id'] = payment_intent.id
            session['instrucciones_crypto'] = (
                payment_intent.next_action.crypto_deposit
                if hasattr(payment_intent, 'next_action') and hasattr(payment_intent.next_action, 'crypto_deposit') 
                else None
            )
            session.pop('carrito', None)

            print('Pago con criptomoneda registrado. Pendiente de verificación.')
            flash('Pago con criptomoneda registrado. Pendiente de verificación.')
            return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))
        
        except stripe.error.StripeError as e:
            self.conn.rollback()
            print(f'Error de Stripe al procesar pago con criptomoneda: {str(e)}')
            flash(f'Error al procesar el pago con criptomoneda: {str(e)}')
            return redirect(url_for('seleccionar_pago'))
                                   
        except Exception as e:
            self.conn.rollback()
            print(f'Error al procesar el pago con criptomoneda: {str(e)}')
            flash(f'Error al procesar el pago con criptomoneda: {str(e)}')
            return redirect(url_for('seleccionar_pago'))

    def procesar_pago_efectivo(self, mesa_id, carrito, total, transaccion_id, fecha):
        try:

            with self.conn.cursor() as cursor:

                query = """ 
                INSERT INTO transacciones (id, mesa_id, metodo_pago, monto, estado, fecha)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (transaccion_id, mesa_id, 'efectivo', total, 'pendiente', fecha))

                for item in carrito:

                    query_detalle = """ 
                    INSERT INTO transaccion_detalles (transaccion_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (transaccion_id, item.get('id'), item.get('cantidad'), item.get('precio')))

                self.conn.commit()

                print('Pago en efectivo registrado. Por favor paga en la caja.')
                flash('Pago en efectivo registrado. Por favor paga en la caja.')
                return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))

        except Exception as e:
            self.conn.rollback()
            print(f'Error al registrar el pago en efectivo: {str(e)}')
            flash(f'Error al registrar el pago en efectivo: {str(e)}')
            return redirect(url_for('seleccionar_pago'))
    
    def enviar_factura_por_correo(self, correo, nombre, mesa_id, carrito, total, transaccion_id, fecha):
        try:

            productos_con_nombre = []
            with self.conn.cursor(dictionary=True) as cursor:
                for item in carrito:
                    query = """ 
                    SELECT nombre_producto FROM productos WHERE id = %s
                    """
                    cursor.execute(query, (item.get('id'),))
                    producto = cursor.fetchone()
                    if producto:
                        productos_con_nombre.append({
                            'id': item.get('id'),
                            'nombre': producto['nombre_producto'],
                            'cantidad': item.get('cantidad'),
                            'precio': item.get('precio'),
                            'subtotal': item.get('cantidad') * item.get('precio')
                        })
            factura_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .factura {{ border: 1px solid #ddd; padding: 20px; max-width: 600px; margin: 0 auto; }}
                    .header {{ text-align: center; margin-bottom: 20px; }}
                    .detalle {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    .detalle th, .detalle td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    .detalle th {{ background-color: #f2f2f2; }}
                    .total {{ text-align: right; font-weight: bold; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="factura">
                    <div class="header">
                        <h2>Factura de Compra</h2>
                        <p>Transacción: {transaccion_id}</p>
                        <p>Fecha: {fecha}</p>
                    </div>
                    
                    <p><strong>Cliente:</strong> {nombre}</p>
                    <p><strong>Mesa:</strong> {mesa_id}</p>
                    <p><strong>Método de pago:</strong> Transferencia Bancaria</p>
                    
                    <table class="detalle">
                        <tr>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Precio Unit.</th>
                            <th>Subtotal</th>
                        </tr>
            """

            for producto in productos_con_nombre:
                factura_html += f""" 
                    <tr>
                        <td>{producto['nombre']}</td>
                        <td>{producto['cantidad']}</td>
                        <td>${producto['precio']:.2f}</td>
                        <td>${producto['subtotal']:.2f}</td>
                    </tr>
                """
            
            factura_html += f""" 
                    </table>
                    
                    <div class="total">
                        <p>Total: ${total:.2f}</p>
                    </div>
                    
                    <p>¡Gracias por su compra!</p>
                    <p>Estado: Pendiente de verificación</p>
                    <p>Recibirá una confirmación cuando su pago sea verificado.</p>
                </div>
            </body>
            </html>
            """

            enviar_correo(transaccion_id, correo, factura_html)

        except Exception as e:
            print(f"Error al enviar la factura por correo: {str(e)}")

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