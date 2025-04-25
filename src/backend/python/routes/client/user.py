"""
Modulo de gestion de usuarios de la aplicacion

Este modulo define la clase `UserApp` que configura y gestiona 
las rutas relacionadas con los usuarios en la aplicacion Flask
"""
from flask import render_template, url_for, redirect, send_file, jsonify, flash, session, request
from io import BytesIO
from datetime import datetime

import os
import json, uuid
import qrcode, stripe
import concurrent.futures

# Importaciones propias
from ....db.database import DBConfig, Error
from ...utils.mail_utils import enviar_correo

class UserApp:
    """
    Clase para gestionar las rutas de usuario en la aplicacion Flask

    Esta clase configura las rutas para la generacion de codigos QR,
    asignacion de mesas y visualizacion de menus de foodtrucks
    """
    def __init__(self, app):
        """
        Inicializa la clase con la aplicacion Flask
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
        """
        @self.user.route('/')
        def qrcode_route():
            """
            Genera un codigo QR para la asignacion de mesas.
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
            return "<b style='text-align: center;'>Ya el qrcode ya fue entregado.<b>"
        
        @self.user.route('/user/menu/<mesa_id>')
        def menu_user(mesa_id):
            """
            Muestra el menu de foodtrucks para una mesa especifica.
            """
            if not mesa_id.isdigit():
                return render_template('errors/404.html'), 404
            
            print("mesa_id:", mesa_id)
            foodtrucks = self.get_food_trucks()
            print("Foodtrucks:", foodtrucks)

            return render_template(
                'client/menu.html',
                mesa_id=int(mesa_id),
                foodtrucks=foodtrucks
            )
        
        @self.user.route('/user/menu/foodtruck/<int:foodtruck_id>')
        def menu_foodtruck(foodtruck_id):
            """
            Muestra el menu de un food truck específico.
            """
            with self.conn.cursor(dictionary=True) as cursor:
                try:
                    query = """
                    SELECT * 
                    FROM productos 
                    WHERE truck_id = %s
                    """
                    cursor.execute(query, (foodtruck_id,))
                    productos = cursor.fetchall()
                    
                    return render_template('client/menu_foodtruck.html', productos=productos)
                
                except Error as e:
                    print(f"Error al obtener productos: {e}")
                    flash(f"Error al obtener productos: {e}", "error")
        
        @self.user.route('/user/splash')
        def splash_screen():
            """
            Muestra la pantalla de inicia (splash screen)
            de la aplicacion.
            """
            return render_template('client/splash.html')

        @self.user.route('/ver-carrito')
        def ver_carrito():
            """ 
            Muestra el contenido del carrito de compras.
            """
            return render_template('client/carrito.html')
        
        @self.user.route('/seleccionar-pago')
        def select_payment():
            """
            Muestra la pantalla de seleccion de
            metodo de pagos.
            """
            return render_template('client/seleccionar_pago.html')
        
        @self.user.route('/procesar-pago', methods=['POST'])
        def procesar_pago():
            """
            Procesa el pago segun el metodo seleccionado 
            por el usuario.
            """
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
            
            total = sum(item.get('precio', 0) * item.get('cantidad', 0)  for item in carrito)
            transaccion_id = str(uuid.uuid4())
            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d %H:%M:%S")

            try:
                if metodo_pago == "tarjeta":
                    return self.procesar_pago_tarjeta(mesa_id, carrito, total, transaccion_id, fecha)
                elif metodo_pago == 'transferencia':
                    return self.procesar_pago_transferencia(mesa_id, carrito, total, transaccion_id, fecha)
                else:
                    flash('Método de pago no valido')
                    return redirect(url_for('select_payment'))
            
            except Exception as e:
                print(f'Error al procesar el pago: {str(e)}')
                flash(f'Error al procesar el pago: {str(e)}', 'error')
                return redirect(url_for('select_payment'))
        
        @self.user.route('/comfirmacion-pago/<transaccion_id>')
        def confirmacion_pago(transaccion_id):
            """
            Muestra la confirmacion de pago para una transaccion
            especifica.
            """
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
                            datos_adiccionales = json.loads(transaccion['datos_adicionales'])
                        except json.JSONDecodeError:
                            datos_adiccionales = {}
                        
                    if metodo_pago == 'transferencia':
                        instrucciones = session.get('instrucciones_bancarias')
                        if not instrucciones and datos_adiccionales:
                            instrucciones = datos_adiccionales.get('instrucciones_bancarias')
                    
                    mesa_id = session.get('mesa_asignada')
                    if not mesa_id:
                        mesa_id = transaccion.get('mesa_id')

                        if mesa_id:
                            session['mesa_asignada'] = mesa_id

                    return render_template('client/confirmacion_pago.html', transaccion=transaccion, detalles=detalles, instrucciones=instrucciones,datos=datos_adiccionales, metodo_pago=metodo_pago,mesa_id=mesa_id)
                
            except Exception as e:
                print(f'Error al mostrar la confirmación: {str(e)}')
                flash(f'Error al mostrar la confirmación: {str(e)}')    
                return redirect(url_for('menu_user', mesa_id=mesa_id))
        
        @self.user.route('/user/confirmar-pago/<transaccion_id>/<token>')
        def confirmar_pago(transaccion_id, token):
            """
            Confirma un pago mediante un token de confirmacion.
            """
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT * FROM transacciones
                    WHERE id = %s AND token_confirmacion = %s
                    """
                    cursor.execute(query, (transaccion_id, token))
                    transaccion = cursor.fetchone()

                    if not transaccion:
                        print("Enlace de confirmacion invalido o expirado.")
                        return redirect(url_for('menu_user', mesa_id=session.get('mesa_asignada')))

                    if transaccion.get('estado') == "completado":
                        print("Este pago ya ha sido confirmado")
                        return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))

                    update_query = """ 
                    UPDATE transacciones
                    SET estado = 'completado', fecha_confirmacion = NOW()
                    WHERE id = %s
                    """
                    cursor.execute(update_query, (transaccion_id,))
                    self.conn.commit()

                    if transaccion.get('metodo_pago') == 'transferencia' and transaccion.get('datos_adicionales'):
                        datos = json.loads(transaccion['datos_adicionales'])
                        if 'stripe_payment_intent_id' in datos:
                            stripe.api_key = os.getenv('PRIVATE_KEY')
                    
                    if 'datos_adicionales' in transaccion and transaccion['datos_adicionales']:
                        datos = json.loads(transaccion['datos_adicionales'])
                        if 'nombre' in datos:
                            correo = datos.get('correo')
                            self.enviar_confirmacion_pago(correo, datos.get('nombre'), transaccion_id)
                    
                    mesa_id = transaccion.get('mesa_id')
                    if not mesa_id:
                        mesa_id = session.get('mesa_asignada')
                    else:
                        session['mesa_asignada'] = mesa_id
                    
                    print("Pago confirmado exitosamente")
                    return redirect(url_for('menu_user', mesa_id=mesa_id, transaccion_id=transaccion_id))
                
            except Exception as e:
                print(f"Error al confirmar pago: {str(e)}")
                return redirect(url_for('menu_user', mesa_id=session.get('mesa_asignada')))
        
        @self.user.route('/api/pedidos', methods=['GET'])
        def get_pedidos():
            """
            Retorno la lista de pedidos realizados.
            Para uso en el panel de administracion.
            """
            try:
                with self.conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT t.id, t.mesa_id, t.metodo_pago, t.monto, t.estado, 
                        t.fecha, t.fecha_confirmacion, 
                            JSON_OBJECT(
                                'detalles', (
                                    SELECT JSON_ARRAYAGG(
                                        JSON_OBJECT(
                                            'id', td.id, 
                                            'producto_id', td.producto_id, 
                                            'nombre_producto', p.nombre_producto,
                                            'cantidad', td.cantidad, 
                                            'precio_unitario', td.precio_unitario
                                        )
                                    )
                                    FROM transaccion_detalles td
                                    JOIN productos p ON td.producto_id = p.id
                                    WHERE td.transaccion_id = t.id
                                )
                            ) as detalles_json
                    FROM transacciones t
                    ORDER BY t.fecha DESC
                    """
                    cursor.execute(query)
                    pedidos = cursor.fetchall()

                    for pedido in pedidos:
                        if pedido['detalles_json']:
                            detalles_obj = json.loads(pedido['detalles_json'])
                            pedido['detalles'] = detalles_obj.get('detalles', [])
                            del pedido['detalles_json']
                        else:
                            pedido['detalles'] = []
                    
                    return jsonify(pedidos)
                
            except Error as e:
                print(f"Error al procesar api: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.user.route('/user/assign_mesa')
        def assign_mesa():
            """
            Asigna una mesa a un usuario y redirige al menu.
            """
            try:
                mesa_asignada = session.get('mesa_asignada')
                if mesa_asignada:
                    return redirect(url_for('menu_user', mesa_id=mesa_asignada))

                future = self.executor.submit(self.assign_mesa_task)
                mesa_id = future.result()

                try:
                    mesa_id = future.result(timeout=5)
                except concurrent.futures.TimeoutError:
                    return "Error: La asignacion de mesa tardo demasiado"
                except Exception as e:
                    return f"Error al asignar mesa: {str(e)}"
                
                if mesa_id is not None and isinstance(mesa_id, int) and mesa_id > 0:
                    session['mesa_asignada'] = mesa_id
                    return redirect(url_for('menu_user', mesa_id=mesa_id))
                
                return "No hay mesas disponibles"
            
            except Exception as e:
                return f"Error inesperado: {str(e)}"

    def assign_mesa_task(self):
        """
        Asigna una mesa a un usuario en segundo plano.
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
                    print(f"Error en assign_mesa_task")
                    return None

        except Error as e:
            self.conn.rollback()
            print(f"Error en la asignación de la mesa: {str(e)}")
            return None
    
    def procesar_pago_tarjeta(self, mesa_id, carrito, total, transaccion_id, fecha):
        """
        Procesa un pago con tarjeta de credito utilizando
        la api `Stripe`.
        """
        try:
            stripe.api_key = os.getenv('PRIVATE_KEY')

            if not stripe.api_key:
                print("ERROR: PRIVATE_KEY no esta configurada")
                return redirect(url_for('select_payment'))
            
            print(f"Todos los datos del formulario:", dict(request.form))

            token = request.form.get('stripeToken')
            nombre = request.form.get('nombreUsuario')
            correo = request.form.get('correo')
            monto = request.form.get('monto')

            print(f"Datos recibidos - Token: {token}, Nombre: {nombre}, Correo: {correo}, Monto: {monto}, Total: {total}")

            if not token:
                print('Error: No se recibio el token de pago')
                print("Datos del formulario: ", request.form)
                flash('Error: No se recibio el token de pago')
                return redirect(url_for('select_payment'))
            
            print(f"Intentando crear cargo por {total} USD")

            charge = stripe.Charge.create(
                amount=int(float(total) * 100),
                currency="usd",
                source=token,
                description=f"Pago de mesa {mesa_id} - Cliente {nombre}"
            )
            print(f"Cargo creado exitosamente: {charge.id}")

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
            
            if correo:
                print(f"Enviando factura a {correo}...")
                self.enviar_factura_por_correo(correo, nombre, mesa_id, carrito, total, transaccion_id, fecha)
            session.pop('carrito', None)

            print('Pago con tarjeta procesado exitosamente')
            flash('Pago con tarjeta procesado exitosamente. El carrito ha sido vaciado.')
            return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))
        
        except stripe.error.StripeError as e:
            self.conn.rollback()
            print(f'Error en el pago con tarjeta: {str(e)}')
            flash(f'Error en el pago con tarjeta: {str(e)}')
            return redirect(url_for('select_payment'))

        except Exception as e:
            self.conn.rollback()
            print(f'Error al procesar el pago: {str(e)}')
            flash(f'Error al procesar el pago: {str(e)}')
            return redirect(url_for('select_payment'))
    
    def procesar_pago_transferencia(self, mesa_id, carrito, total, transaccion_id, fecha):
        """
        Procesa un pago por transferencia bancaria
        utilizando la api `Stripe`.
        """
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
                payment_method_data={ "type": "customer_balance" },
                payment_method_options={
                    "customer_balance": 
                    {
                        "funding_type": "bank_transfer",
                        "bank_transfer": 
                        {
                            "type": "us_bank_transfer"
                        }
                    }
                }
            )

            payment_intent = stripe.PaymentIntent.retrieve(
                payment_intent.id,
                expand=["next_action"]
            )

            instrucciones_bancarias = getattr(
                payment_intent.next_action, 
                'display_bank_transfer_instructions', 
                None
            )
            
            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO transacciones (id, mesa_id, metodo_pago, monto, estado, fecha, datos_adicionales)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                datos_adicionales = json.dumps({
                    'nombre': nombre,
                    'correo': correo,
                    'stripe_payment_intent_id': payment_intent.id,
                    'stripe_customer_id': customer.id,
                    'instrucciones_bancarias': instrucciones_bancarias
                })

                session['instrucciones_bancarias'] = instrucciones_bancarias

                cursor.execute(query, (transaccion_id, mesa_id, 'tranferencia', total, 'pendiente', fecha, datos_adicionales))

                for item in carrito:
                    query_detalle = """ 
                    INSERT INTO transaccion_detalles (transaccion_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (transaccion_id, item.get('id'), item.get('cantidad'), item.get('precio')))
                self.conn.commit()

            session['payment_intent_id'] = payment_intent.id
            session.pop('carrito', None)

            if correo:
                print(f"Enviando factura a {correo}...")
                self.enviar_factura_por_correo(correo, nombre, mesa_id, carrito, total, transaccion_id, fecha)

            print('Transferencia registrada. Pendiente de verificación.')
            flash('Transferencia registrada. Pendiente de verificación.')
            return redirect(url_for('confirmacion_pago', transaccion_id=transaccion_id))
        
        except stripe.error.StripeError as e:
            self.conn.rollback()
            print(f'Error de Stripe al procesar transferencia: {str(e)}')
            flash(f'Error al procesar la transferencia: {str(e)}')
            return redirect(url_for('select_payment'))
        
        except Exception as e:
            self.conn.rollback()
            print(f'Error al procesar la transferencia: {str(e)}')
            flash(f'Error al procesar la transferencia: {str(e)}')
            return redirect(url_for('select_payment'))
    
    def enviar_factura_por_correo(self, correo, nombre, mesa_id, carrito, total, transaccion_id, fecha):
        """
        Envia una factura por correo electronico al cliente
        """
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

            confirmation_token = str(uuid.uuid4())
            with self.conn.cursor() as cursor:
                query = """ 
                UPDATE transacciones
                SET token_confirmacion = %s
                WHERE id = %s
                """
                cursor.execute(query, (confirmation_token, transaccion_id))
                self.conn.commit()

            ruta_base = "https://74zb1whg-5000.use2.devtunnels.ms/user"
            confirmation_url = f"{ruta_base}/confirmar-pago/{transaccion_id}/{confirmation_token}"

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
                    <div class="confirmation">
                        <p>Para confirmar su pago, haga clic en el siguiente enlace:</p>
                        <p><a href="{confirmation_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Confirmar Pago</a></p>
                        <p>Este enlace es válido por 24 horas.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            enviar_correo(transaccion_id, correo, factura_html)

        except Exception as e:
            print(f"Error al enviar la factura por correo: {str(e)}")
    
    def enviar_confirmacion_pago(self, correo, nombre, transaccion_id):
        """
        Envia una confirmacion del pago del cliente
        """
        try:
            confirmacion_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .confirmacion {{ border: 1px solid #ddd; padding: 20px; max-width: 600px; margin: 0 auto; }}
                    .header {{ text-align: center; margin-bottom: 20px; color: #4CAF50; }}
                </style>
            </head>
            <body>

                <div class="confirmacion">

                    <div class="header">
                        <h2>Confirmación de Pago</h2>
                    </div>
                    
                    <p>Estimado(a) {nombre},</p>
                    <p>
                        Nos complace informarle que su pago para la transacción <strong>{transaccion_id}</strong> ha sido confirmado exitosamente.
                    </p>
                    <p>Su pedido ya está siendo procesado y estará listo en breve.</p>
                    <p>¡Gracias por su preferencia!</p>
                    <p>Atentamente,<br> El equipo de FoodTrucks</p>

                </div>

            </body>
            </html>
            """
            enviar_correo(f"Confirmación de Pago - {transaccion_id}", correo, confirmacion_html)
            
        except Exception as e:
            print(f"Error al enviar la confirmación por correo: {str(e)}")

    def get_food_trucks(self):
        """
        Obtiene la lista de foodtrucks de la base de datos
        """
        with self.conn.cursor(dictionary=True) as cursor:
            try:
                query = """
                SELECT * FROM trucks
                WHERE estado_truck = 'activo'
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Error as e:
                print(f"Error al obtener los foodtrucks: {e}")
                return []