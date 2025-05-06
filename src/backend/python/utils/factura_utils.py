from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
import os
from datetime import datetime
import qrcode
from io import BytesIO
import random
import locale
import tempfile

def generar_factura_pdf(nombre_archivo, datos_anomalias, info_cliente=None):
    try:
        # Configuración regional para formato de números
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except locale.Error:
            # Fallback a la configuración predeterminada si no está disponible 'es_ES.UTF-8'
            try:
                locale.setlocale(locale.LC_ALL, 'es_ES')
            except locale.Error:
                locale.setlocale(locale.LC_ALL, '')  # Usar configuración del sistema
    
        # Crear directorio si no existe
        carpeta_destino = os.path.join(os.getcwd(), 'facturas')
        os.makedirs(carpeta_destino, exist_ok=True)
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
        
        # Tamaño de ticket más estrecho (58mm estándar para tickets)
        ancho_ticket = 220
        alto_ticket = 600  # Aumentado para más contenido
        
        # Crear el canvas
        c = canvas.Canvas(ruta_completa, pagesize=(ancho_ticket, alto_ticket))
        
        # Número de factura
        num_factura = f"F-{random.randint(10000, 99999)}"
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Información del cliente
        if info_cliente is None:
            info_cliente = {
                "nombre": "Cliente General",
                "direccion": "Av. Principal #123",
                "telefono": "809-555-1234",
                "email": "cliente@ejemplo.com"
            }
        
        # Logo y encabezado
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(ancho_ticket/2, alto_ticket-30, "FOODORDER")
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(ancho_ticket/2, alto_ticket-45, "FACTURA OFICIAL")
        
        # Información de la empresa
        c.setFont("Helvetica", 8)
        y = alto_ticket - 65
        empresa_info = [
            "FoodOrder Inc.",
            "Santo Domingo, República Dominicana", 
            "Tel: +1 809-456-7890", 
            "Email: facturacion@foodorder.com", 
            f"RNC: 1-31-56789-0"
        ]
        
        for linea in empresa_info:
            c.drawCentredString(ancho_ticket/2, y, linea)
            y -= 12
        
        # Línea separadora
        c.line(10, y-5, ancho_ticket-10, y-5)
        y -= 15
        
        # Información de factura
        c.setFont("Helvetica-Bold", 8)
        c.drawString(10, y, f"FACTURA: {num_factura}")
        c.drawString(10, y-12, f"FECHA: {fecha_actual}")
        y -= 30
        
        # Información del cliente
        c.setFont("Helvetica-Bold", 8)
        c.drawString(10, y, "CLIENTE:")
        y -= 12
        c.setFont("Helvetica", 8)
        c.drawString(10, y, info_cliente["nombre"])
        y -= 10
        c.drawString(10, y, info_cliente["direccion"])
        y -= 10
        c.drawString(10, y, f"Tel: {info_cliente['telefono']}")
        y -= 10
        c.drawString(10, y, f"Email: {info_cliente['email']}")
        y -= 15
        
        # Línea separadora
        c.line(10, y-5, ancho_ticket-10, y-5)
        y -= 15
        
        # Cabecera de la tabla
        c.setFont("Helvetica-Bold", 8)
        c.drawString(10, y, "PRODUCTO")
        c.drawString(110, y, "TRUCK")
        c.drawRightString(ancho_ticket-10, y, "VENTAS")
        y -= 5
        
        # Línea separadora
        c.line(10, y-3, ancho_ticket-10, y-3)
        y -= 10
        
        # Contenido de la tabla
        c.setFont("Helvetica", 7)
        total_ventas = 0
        items = 0
        
        for _, row in datos_anomalias.iterrows():
            items += 1
            producto = row['nombre_producto']
            truck = row['nombre_truck']
            ventas = int(row['ventas_diarias'])
            
            # Alternar color de fondo para mejor legibilidad
            if items % 2 == 0:
                c.setFillColorRGB(0.95, 0.95, 0.95)
                c.rect(10, y-8, ancho_ticket-20, 10, fill=True, stroke=False)
                c.setFillColorRGB(0, 0, 0)  # Volver a negro para el texto
            
            c.drawString(10, y, producto[:15] + ('...' if len(producto) > 15 else ''))
            c.drawString(110, y, truck[:12] + ('...' if len(truck) > 12 else ''))
            c.drawRightString(ancho_ticket-10, y, f"{ventas:,}")
            
            total_ventas += ventas
            y -= 15
        
        # Línea separadora
        c.line(10, y-3, ancho_ticket-10, y-3)
        y -= 15
        
        # Totales
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10, y, "SUBTOTAL:")
        c.drawRightString(ancho_ticket-10, y, f"{total_ventas:,}")
        y -= 15
        
        impuesto = total_ventas * 0.18
        c.drawString(10, y, "ITBIS (18%):")
        c.drawRightString(ancho_ticket-10, y, f"{int(impuesto):,}")
        y -= 15
        
        total_final = total_ventas + impuesto
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, y, "TOTAL RD$:")
        c.drawRightString(ancho_ticket-10, y, f"{int(total_final):,}")
        
        # Método de pago
        y -= 25
        c.setFont("Helvetica", 8)
        c.drawString(10, y, "MÉTODO DE PAGO: Efectivo")
        y -= 10
        c.drawString(10, y, "ATENDIDO POR: Operador #42")
        
        # Línea separadora
        y -= 15
        c.line(10, y-3, ancho_ticket-10, y-3)
        y -= 15
        
        # Generar código QR con los datos de la factura
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=1,
        )
        qr.add_data(f"Factura: {num_factura}\nFecha: {fecha_actual}\nTotal: RD${int(total_final):,}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Corregimos el error utilizando un archivo temporal real en lugar de BytesIO
        temp_file_path = os.path.join(tempfile.gettempdir(), f"qr_temp_{num_factura}.png")
        img.save(temp_file_path)
        c.drawImage(temp_file_path, ancho_ticket/2 - 25, y - 50, width=50, height=50)
        
        # Eliminar el archivo temporal después de usarlo
        try:
            os.remove(temp_file_path)
        except:
            pass  # Ignorar errores al eliminar el archivo temporal
            
        y -= 60
        
        # Mensaje final
        c.setFont("Helvetica", 7)
        c.drawCentredString(ancho_ticket/2, y, "GRACIAS POR SU PREFERENCIA")
        y -= 10
        c.drawCentredString(ancho_ticket/2, y, "www.foodorder.com")
        y -= 10
        c.drawCentredString(ancho_ticket/2, y, "Esta factura tiene validez fiscal")
        
        # Términos y condiciones
        y -= 20
        c.setFont("Helvetica", 6)
        c.drawCentredString(ancho_ticket/2, y, "TÉRMINOS Y CONDICIONES")
        y -= 8
        terminos = [
            "Esta factura es un documento legal.",
            "Conserve este documento para cualquier reclamación.",
            "No se aceptan devoluciones después de 15 días."
        ]
        
        for termino in terminos:
            c.drawCentredString(ancho_ticket/2, y, termino)
            y -= 7
        
        c.save()
        return ruta_completa
    
    except Exception as e:
        # Registrar el error pero continuar
        print(f"Error al generar factura PDF: {str(e)}")
        # Intento de generación simplificada en caso de error
        try:
            # Crear un PDF simple sin QR en caso de error
            c = canvas.Canvas(ruta_completa, pagesize=(ancho_ticket, alto_ticket))
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(ancho_ticket/2, alto_ticket-30, "FOODORDER")
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(ancho_ticket/2, alto_ticket-45, "FACTURA OFICIAL")
            c.setFont("Helvetica", 8)
            c.drawCentredString(ancho_ticket/2, alto_ticket-65, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawCentredString(ancho_ticket/2, alto_ticket-85, "*** REPORTE DE ANOMALÍAS ***")
            
            y = alto_ticket - 110
            c.setFont("Helvetica-Bold", 8)
            c.drawString(10, y, "PRODUCTO")
            c.drawString(110, y, "TRUCK")
            c.drawRightString(ancho_ticket-10, y, "VENTAS")
            y -= 15
            
            c.setFont("Helvetica", 7)
            total = 0
            for _, row in datos_anomalias.iterrows():
                producto = row['nombre_producto']
                truck = row['nombre_truck']
                ventas = int(row['ventas_diarias'])
                c.drawString(10, y, str(producto)[:15])
                c.drawString(110, y, str(truck)[:12])
                c.drawRightString(ancho_ticket-10, y, str(ventas))
                total += ventas
                y -= 12
            
            c.drawString(10, y-20, "TOTAL:")
            c.drawRightString(ancho_ticket-10, y-20, str(total))
            
            c.save()
            return ruta_completa
        except Exception as e2:
            print(f"Error en generación simplificada: {str(e2)}")
            return None