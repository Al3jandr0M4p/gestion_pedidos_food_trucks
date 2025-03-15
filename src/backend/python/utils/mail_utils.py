from flask_mail import Message

def enviar_correo(transacion_id, correo, factura_hmtl):
        from ..app import FoodTrucks

        msg = Message(
            subject=f"Factura de compra - Transaccion {transacion_id}",
            recipients=[correo],
            html=factura_hmtl
        )
        
        food = FoodTrucks()
        with food.food.app_context():
            food.mail.send(msg)

        print(f"Factura enviada correctamente a {correo}")