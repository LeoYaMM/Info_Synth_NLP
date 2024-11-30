# Description: Este script se encarga de generar códigos QR para las exposiciones del museo, basados en el ID de la exposición y almacenarlos en archivos PNG.
#* Status: Complete

import hashlib
import qrcode
from .sqlConnector import *

# Función para generar el hash basado en el ID de la exposición
def generar_hash_exposicion(id_exposicion):
    id_str = str(id_exposicion)
    hash_obj = hashlib.sha256(id_str.encode())
    return hash_obj.hexdigest()

# Función para generar el código QR
def generar_qr(hash_exposicion, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_exposicion)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)

def obtener_exposiciones(conexion):
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_objeto, Nombre_objeto FROM objeto_historico")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener las exposiciones: {e}")
        return []

def main():
    # Conectar a la base de datos
    conexion_museo = create_connection()
    
    if conexion_museo:
        # Obtener las exposiciones de la base de datos
        exposiciones = obtener_exposiciones(conexion_museo)

        for exposicion in exposiciones:
            id_exposicion = exposicion['id_objeto']
            nombre_exposicion = exposicion['Nombre_objeto']
            
            # Generar el hash basado en el ID
            hash_exposicion = generar_hash_exposicion(id_exposicion)
            guardar_hash(hash_exposicion, id_exposicion)
            
            # Generar el QR con el hash
            nombre_archivo = f"qr_{nombre_exposicion}_{id_exposicion}.png"
            generar_qr(hash_exposicion, nombre_archivo)

            print(f"QR generado para '{nombre_exposicion}' (ID: {id_exposicion}), guardado como {nombre_archivo}")
        
        # Cerrar la conexión con la base de datos
        close_connection(conexion_museo)

if __name__ == "__main__":
    main()
