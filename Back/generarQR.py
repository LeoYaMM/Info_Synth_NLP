import hashlib
import qrcode
from sqlConnector import conectar_bd, cerrar_conexion, obtener_exposiciones

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

# Función principal que une todo
def main():
    # Conectar a la base de datos
    conexion = conectar_bd()
    
    if conexion:
        # Obtener las exposiciones de la base de datos
        exposiciones = obtener_exposiciones(conexion)

        for exposicion in exposiciones:
            id_exposicion = exposicion['id']
            nombre_exposicion = exposicion['nombre']
            
            # Generar el hash basado en el ID
            hash_exposicion = generar_hash_exposicion(id_exposicion)
            
            # Generar el QR con el hash
            nombre_archivo = f"qr_{nombre_exposicion}_{id_exposicion}.png"
            generar_qr(hash_exposicion, nombre_archivo)

            print(f"QR generado para '{nombre_exposicion}' (ID: {id_exposicion}), guardado como {nombre_archivo}")
        
        # Cerrar la conexión con la base de datos
        cerrar_conexion(conexion)

if __name__ == "__main__":
    main()
