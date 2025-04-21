'''
Módulo de envío de correos electrónicos en la aplicación FoodTrucks.

Este módulo proporciona la función `enviar_correo`, que permite enviar
facturas en formato HTML por correo electrónico utilizando `flask_mail`.
'''

from flask_mail import Message
from flask import current_app as app

def enviar_correo(transaccion_id, correo, factura_html):
    """
    Envía una factura por correo electrónico utilizando Flask-Mail.
    """
    
    try:
        from ..app import FoodTrucks

        msg = Message(
            subject=f"Factura de compra - Transacción {transaccion_id}",
            recipients=[correo],
            html=factura_html
        )
        
        food = FoodTrucks()
        with food.food.app_context():
            food.mail.send(msg)
        
        print(f"Factura enviada correctamente a {correo}")
    
    except Exception as e:
        app.logger.error(f"Error al enviar la factura a {correo}: {str(e)}")
        print(f"Hubo un error al enviar la factura a {correo}. Por favor intente de nuevamente.")