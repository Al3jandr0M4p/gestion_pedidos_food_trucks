'''
Módulo de envío de correos electrónicos en la aplicación FoodTrucks.

Este módulo proporciona la función `enviar_correo`, que permite enviar
facturas en formato HTML por correo electrónico utilizando `flask_mail`.

Ejemplo de uso:
---------------
>>> from src.backend.python.mail_service import enviar_correo
>>> enviar_correo(12345, 'cliente@example.com', '<h1>Factura</h1>')
'''

from flask_mail import Message

def enviar_correo(transaccion_id, correo, factura_html):
    '''
    Envía una factura por correo electrónico utilizando Flask-Mail.

    Parámetros:
    -----------
    transaccion_id : int
        Identificador único de la transacción asociada a la factura.
    correo : str
        Dirección de correo electrónico del destinatario.
    factura_html : str
        Contenido HTML de la factura.
    '''
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