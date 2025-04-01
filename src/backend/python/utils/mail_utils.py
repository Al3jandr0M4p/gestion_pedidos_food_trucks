'''
Módulo de envío de correos electrónicos en la aplicación FoodTrucks.

Este módulo proporciona la función `enviar_correo`, que permite enviar
facturas en formato HTML por correo electrónico utilizando `flask_mail`.
'''

from flask_mail import Message

def enviar_correo(transaccion_id, correo, factura_html):
    """
    Envía una factura por correo electrónico utilizando Flask-Mail.
    """
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