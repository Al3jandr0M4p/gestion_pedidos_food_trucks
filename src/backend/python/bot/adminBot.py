from flask import request, jsonify
from datetime import datetime, timedelta
from flask_mail import Message

import numpy as np
import pandas as pd
from scipy import stats

# modulos propios
from ...db.database import DBConfig
from ...security.autentication import authentication_required
from ..utils.factura_utils import generar_factura_pdf
import os

class AdminBots:
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)

    db = DBConfig()

    def __init__(self, app, mail):
        self.bot_admin = app
        self.mail = mail
        self.bot_routes()

        self.conn = self.db.get_db_config()
    
    def bot_routes(self):
        
        @self.bot_admin.route('/admin/chatbot', methods=['POST'])
        @authentication_required
        def chatbot_admin():
            data = request.get_json()
            pregunta = str(data.get('pregunta', '')).lower()

            if "producto" in pregunta and "mas vendido" in pregunta:

                return jsonify({
                    "respuesta": self.producto_mas_vendido_semana()
                })
            
            elif "food truck" in pregunta and "ganancias" in pregunta:

                return jsonify({
                    "respuesta": self.truck_mas_ganancias()
                })
            
            elif "combo" in pregunta or "promocionar" in pregunta:

                return jsonify({
                    "respuesta": self.combo_promocional()
                })
            
            return jsonify({
                "respuesta": "No entendi tu pregunta. Proba con otra."
            })
        
        @self.bot_admin.route('/reportes/ia/anormalias')
        @authentication_required
        def reportes_anomalias():
            
            with self.conn.cursor() as cursor:
                query = """
                SELECT 
                    p.id AS producto_id, 
                    p.nombre_producto,
                    t.nombre_truck,
                    SUM(td.cantidad) AS ventas_diarias
                FROM productos p
                LEFT JOIN trucks t ON p.truck_id = t.id
                LEFT JOIN transaccion_detalles td ON p.id = td.producto_id
                LEFT JOIN transacciones tx ON td.transaccion_id = tx.id
                WHERE tx.fecha >= NOW() - INTERVAL 7 DAY
                GROUP BY p.id, p.nombre_producto, t.nombre_truck
                """
                cursor.execute(query)
                result = cursor.fetchall()
                data = pd.DataFrame(result, columns=['producto_id', 'nombre_producto', 'nombre_truck', 'ventas_diarias'])

                data['ventas_diarias'] = pd.to_numeric(data['ventas_diarias'], errors='coerce')

                data = data.dropna(subset=['ventas_diarias'])

                z_score = stats.zscore(data['ventas_diarias'])
                umbral = 1
                data['anomalias'] = np.abs(z_score) >= umbral

                anomalias = data[data['anomalias'] == True]

                if not anomalias.empty:
                    pdf_name = "factura_anomalias.pdf"

                    generar_factura_pdf(pdf_name, anomalias)

                    mensaje = "🔔 *Se detectaron anomalías en ventas. Se adjunta la factura.*"
                    self.enviar_alarma_email(mensaje, archivo_pdf=os.path.join(os.getcwd(), 'facturas', pdf_name))
                
                return jsonify(anomalias.to_dict(orient="records"))
    
    def enviar_alarma_email(self, mensaje, archivo_pdf=None):
        with self.conn.cursor() as cursor:
            query = """
            SELECT email 
            FROM users 
            WHERE rol = 'admin' AND estado = 'activo'
            """
            cursor.execute(query)
            result = cursor.fetchall()

            correos = [row[0] for row in result]

        msg = Message(
            subject="Reportes de la app - Administradores",
            recipients=correos,
            html=mensaje
        )

        if archivo_pdf:
            with open(archivo_pdf, 'rb') as f:
                msg.attach(
                    filename="factura_anomalias.pdf",
                    content_type="application/pdf",
                    data=f.read()
                ) 

        if self.mail:
            self.mail.send(msg)
        
    def producto_mas_vendido_semana(self):

        with self.conn.cursor() as cursor:

            query = """
            SELECT p.nombre_producto, SUM(td.cantidad) as total
            FROM transaccion_detalles td
            JOIN productos p ON td.producto_id = p.id
            JOIN transacciones t ON td.transaccion_id = t.id
            WHERE t.fecha >= %s
            GROUP BY p.nombre_producto
            ORDER BY total DESC
            LIMIT 1;
            """
            cursor.execute(query, (self.hace_7_dias,))
            resultado = cursor.fetchone()

            if resultado:
                return f"📈 El producto mas vendido esta semana fue: {resultado[0]}"
            
            return "No hay datos de venta esta semana"
    
    def truck_mas_ganancias(self):

        with self.conn.cursor() as cursor:

            query = """
            SELECT t.nombre_truck, SUM(td.precio_unitario * td.cantidad) as ganancias
            FROM transaccion_detalles td
            JOIN productos p ON td.producto_id = p.id
            JOIN trucks t ON p.truck_id = t.id
            JOIN transacciones tr ON td.transaccion_id = tr.id
            WHERE tr.fecha >= %s
            GROUP BY t.nombre_truck
            ORDER BY ganancias DESC
            LIMIT 1;
            """
            cursor.execute(query, (self.hace_7_dias,))
            resultado = cursor.fetchone()

            if resultado:
                return f"💰 El food truck con más ganancias fue {resultado[0]} con ${resultado[1]:.2f}"
            
            return "No hay datos suficientes de ganancias"
    
    def combo_promocional(self):

        with self.conn.cursor() as cursor:

            query = """
            SELECT p.nombre_producto
            FROM productos p
            ORDER BY RAND()
            LIMIT 2;
            """
            cursor.execute(query)
            productos = cursor.fetchall()

            if len(productos) == 2:
                return f"🔥 Promocioná el combo: {productos[0][0]} + {productos[1][0]}"
            
            return "No hay suficientes productos para sugerir un combo"