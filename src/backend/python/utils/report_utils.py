from ...db.database import DBConfig

def obtener_reportes_generales():
    db_config = DBConfig()
    connection = db_config.get_db_config()
    
    with connection.cursor(dictionary=True) as cursor:
        metodo_pago_query = """
        SELECT metodo_pago AS metodo, SUM(monto) AS total
        FROM transacciones
        GROUP BY metodo_pago
        """

        ventas_trucks_query = """
        SELECT t.nombre_truck, SUM(td.precio_unitario * td.cantidad) AS total
        FROM transaccion_detalles td
        JOIN productos p ON td.producto_id = p.id
        JOIN trucks t ON p.truck_id = t.id
        JOIN transacciones tr ON tr.id = td.transaccion_id
        WHERE tr.estado = 'completado'
        GROUP BY t.id
        """

        ventas_productos_query = """
        SELECT p.nombre_producto, SUM(td.precio_unitario * td.cantidad) AS total, SUM(td.cantidad) AS ventas
        FROM transaccion_detalles td
        JOIN productos p ON td.producto_id = p.id
        JOIN transacciones tr ON tr.id = td.transaccion_id
        WHERE tr.estado = 'completado'
        GROUP BY p.id
        """

        transacciones_trucks_query = """
        SELECT t.nombre_truck, COUNT(DISTINCT tr.id) AS numero_transacciones
        FROM transacciones tr
        JOIN transaccion_detalles td ON tr.id = td.transaccion_id
        JOIN productos p ON td.producto_id = p.id
        JOIN trucks t ON p.truck_id = t.id
        WHERE tr.estado = 'completado'
        GROUP BY t.id
        """

        ventas_hora_query = """
        SELECT HOUR(tr.fecha) AS hora, SUM(tr.monto) AS total
        FROM transacciones tr
        WHERE tr.estado = 'completado'
        GROUP BY HOUR(tr.fecha)
        ORDER BY hora
        """

        estado_mesas_query = """
        SELECT estado, COUNT(id) AS total
        FROM mesas
        GROUP BY estado
        """

        total_ventas_query = """
        SELECT SUM(monto) AS total_ventas
        FROM transacciones
        WHERE estado = 'completado'
        """

        total_transacciones_query = """
        SELECT COUNT(id) AS total_transacciones
        FROM transacciones
        WHERE estado = 'completado'
        """

        cursor.execute(metodo_pago_query)
        metodo_pago = cursor.fetchall()

        cursor.execute(ventas_trucks_query)
        ventas_trucks = cursor.fetchall()

        cursor.execute(ventas_productos_query)
        ventas_productos = cursor.fetchall()

        cursor.execute(transacciones_trucks_query)
        transacciones_trucks = cursor.fetchall()

        cursor.execute(ventas_hora_query)
        ventas_hora = cursor.fetchall()

        cursor.execute(estado_mesas_query)
        estado_mesas = cursor.fetchall()

        cursor.execute(total_ventas_query)
        total_ventas = cursor.fetchone()['total_ventas']

        cursor.execute(total_transacciones_query)
        total_transacciones_data = cursor.fetchone()

        if total_transacciones_data:
            total_transacciones = total_transacciones_data['total_transacciones']
        else:
            total_transacciones = 0

        promedio_transaccion = total_ventas / total_transacciones if total_transacciones > 0 else 0

        return {
            "metodo_pago": metodo_pago,
            "ventas_trucks": ventas_trucks,
            "ventas_productos": ventas_productos,
            "transacciones_trucks": transacciones_trucks,
            "ventas_hora": ventas_hora,
            "estado_mesas": estado_mesas,
            "total_ventas": total_ventas,
            "promedio_transaccion": promedio_transaccion,
            "total_transacciones": total_transacciones
        }