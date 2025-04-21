from flask import jsonify, request
import random
import re
import os
import json

# modulos propios
from ...db.database import DBConfig

class NotificationBot:

    def __init__(self, app):
        self.bot = app
        self.setup_bot_routes()

        db = DBConfig()
        self.conn = db.get_db_config()

        self.path_response_bot = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', '..', '..', '..', 'bot_responses.json'
            )
        )
        with open(self.path_response_bot, 'r', encoding='utf-8') as f:
            self.bot_responses = json.load(f)
    
    def setup_bot_routes(self):

        @self.bot.route('/notificaciones')
        def notificaciones():
            recomenciones = self.get_recomendations_bot()
            
            # contar cuantas veces aparece cada producto
            contador = dict()
            for r in recomenciones:
                clave = r['nombre_producto']
                contador[clave] = contador.get(clave, 0) + 1

            mensajes = list()
            for r in recomenciones:
                veces = contador[r['nombre_producto']]
                mensajes.append(self.generar_mensaje_aleatorio(r, veces))
            
            mensajes_combo = self.generar_mensaje_combo()
            mensajes_finales = mensajes + mensajes_combo
            random.shuffle(mensajes_finales)
            
            print("Mensajes: ", mensajes_finales)
            return jsonify(mensajes_finales)

        @self.bot.route('/chatbot', methods=['POST'])
        def chatbot():
            data = request.get_json()

            if not data or 'mensaje' not in data:
                return jsonify({
                    "respuesta": "Lo siento no entendi tu mensaje. Puedes intentarlo de nuevo?"
                })
            
            user_message = data['mensaje'].lower()
            response = self.get_bot_response(user_message)

            return jsonify({
                "respuesta": response
            })
    
    def get_bot_response(self, user_message):

        for pattern, responses in self.bot_responses.items():
            if re.search(pattern, user_message, re.IGNORECASE):
                response = random.choice(responses)

                if '{top_product}' in response:
                    top_products = self.get_recomendations_bot()
                    if top_products:
                        top_product = top_products[0]['nombre_producto']
                        top_truck = top_products[0]['nombre_truck']
                        response = response.format(top_product=top_product, top_truck=top_truck)
                    
                    else:
                        response = "Tenemos muchos productos deliciosos! Te invito a explorar nustrps food trucks."

                return response
        
        food_type_match = re.search(r"vegetariano|vegano|sin gluten|saludable|postres|bebidas|asiático|sushi", user_message, re.IGNORECASE)
        
        if food_type_match:
            food_type = food_type_match.group(0).lower()
            return self.get_food_type_response(food_type)
        
        default_responses = [
            "Lo siento, no entendi tu pregunta. ¿Puedes reformularla?",
            "No estoy seguro de lo que buscas. ¿Puedes ser mas especifico?",
            "Disculpa, pero no tengo información sobre eso. ¿Puedo ayudarte con algo mas?",
            "¿Que tal si me preguntas sobre nuestros menus, recomendaciones o como hacer un pedido?"
        ]

        return random.choice(default_responses)
    
    def get_food_type_response(self, food_type):
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', '..', '..', '..', 'types.json'
            )
        )

        with open(path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        if food_type in responses:
            return random.choice(responses[food_type])
        else:
            return f"Tenemos varios food trucks que ofrecen {food_type}. Te invito a explorar nuestro menu completo en la aplicacion."
    
    def generar_mensaje_combo(self):
        mensaje_combo = []

        with self.conn.cursor() as cursor:
            query = """
            SELECT p.nombre_producto, COUNT(td.producto_id) AS ventas
            FROM productos p
            JOIN transaccion_detalles td ON p.id = td.producto_id
            GROUP BY p.id
            ORDER BY ventas DESC
            LIMIT 4;
            """
            cursor.execute(query)
            top_productos = cursor.fetchall()
            mensajes_posibles = [
                "🔥 ¡{p1} y {p2} son la pareja perfecta para tu antojo!",
                "😋 ¿Probaste {p1} con {p2}? ¡Combo irresistible!",
                "🍽️ {p1} + {p2} = el dúo ganador de la semana",
                "👀 Muchos están pidiendo {p1} con {p2}. ¡No te lo pierdas!",
            ]

            for i in range(0, len(top_productos) - 1, 2):
                producto1 = top_productos[i][0]
                producto2 = top_productos[i + 1][0]
                plantilla = random.choice(mensajes_posibles)

                mensaje_combo.append(
                    plantilla.format(p1=producto1, p2=producto2)
                )
            
        return mensaje_combo
    
    def generar_mensaje_aleatorio(self, recomendaciones, repeticiones=1):

        producto = recomendaciones['nombre_producto']
        truck = recomendaciones['nombre_truck']

        plantillas = [
            "🔥 ¡Top ventas! El producto más pedido es {producto} de {truck}.",
            "✨ ¿Ya probaste el famoso {producto} de {truck}? ¡Todo el mundo lo está pidiendo!",
            "👀 ¡Ojo! {producto} de {truck} está arrasando hoy.",
            "💥 Boom! {producto} de {truck} fue uno de los más vendidos.",
            "😋 {producto} de {truck} no para de salir. ¡Un clásico!",
            "🚚 El food truck {truck} no da abasto con su {producto} 🔥",
            "⭐ Recomendado del día: {producto} de {truck}. ¡Éxito total!"
        ]

        if repeticiones >= 2:
            especialidades = [
                "😲 Otra vez {producto} de {truck}? ¡La están rompiendo!",
                "🔥 ¡{producto} de {truck} no para de salir! ¡Sigue rompiéndola!",
                "🥵 La gente no se cansa de pedir {producto} de {truck}!"
            ]
            mensaje = random.choice(especialidades)
        else:
            mensaje = random.choice(plantillas)

        return mensaje.format(producto=producto, truck=truck)
    
    def get_recomendations_bot(self):
        with self.conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT p.nombre_producto, t.nombre_truck, SUM(td.cantidad) AS total_vendidos
            FROM transaccion_detalles td
            JOIN productos p ON td.producto_id = p.id
            JOIN trucks t ON p.truck_id = t.id
            GROUP BY p.nombre_producto, t.nombre_truck
            ORDER BY total_vendidos DESC
            LIMIT 5;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            print("Resultado de la consulta:", result)
            return result