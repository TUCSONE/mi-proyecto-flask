import os
import qrcode

# Asegúrate de que la carpeta existe, si no la crea
if not os.path.exists("codigos_qr"):
    os.makedirs("codigos_qr")

# Lista de invitados
invitados = ["Adriano Quiroga", "Juan Perez", "Maria Lopez"]

# URL base de la aplicación Flask (esto puede ser un localhost si lo estás probando localmente)
base_url = "http://127.0.0.1:5000/verificado/"

# Generar un código QR por cada invitado
for invitado in invitados:
    # Crear un enlace único para cada invitado
    qr_data = base_url + invitado.replace(" ", "_")  # reemplazar espacios por guiones bajos
    
    # Crear el código QR
    qr = qrcode.make(qr_data)
    
    # Guardar el código QR en la carpeta 'codigos_qr'
    qr.save(f"codigos_qr/{invitado}.png")
