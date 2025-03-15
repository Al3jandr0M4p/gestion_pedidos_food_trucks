from flask import Flask
from flask_mail import Message, Mail
import os

def enviar_correo(transacion_id, correo, factura_hmtl):
        temp_app = Flask(__name__)
        temp_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        temp_app.config['MAIL_PORT'] = 587
        temp_app.config['MAIL_USE_TLS'] = True
        temp_app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
        temp_app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
        temp_app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_DEFAULT_SENDER')
        mail = Mail(temp_app)

        msg = Message(
            subject=f"Factura de compra - Transaccion {transacion_id}",
            recipients=[correo],
            html=factura_hmtl
        )

        with temp_app.app_context():
            mail.send(msg)
        return f"Factura enviada correctamente a {correo}"