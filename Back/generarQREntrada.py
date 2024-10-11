import hashlib
import qrcode
from sqlConnector import conectar_bd_usuarios, cerrar_conexion, obtener_usuarios

# Función para generar el hash basado en el ID del usuario
def generar_hash_usuario(id_usuario):
    id_str = str(id_usuario)
    hash_obj = hashlib.sha256(id_str.encode())
    return hash_obj.hexdigest()

# Función para generar el código QR de entrada
def generar_qr(hash_usuario, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_usuario)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)
    print('QR generado')

# Función principal que une todo
def main():
    # Conectar a la base de datos
    conexion_usuarios = conectar_bd_usuarios()
    
    if conexion_usuarios:
        # Obtener los usuarios de la base de datos
        usuarios = obtener_usuarios(conexion_usuarios)

        for usuario in usuarios:
            id_usuario = usuario['id']
            nombre_usuario = usuario['nombre']
            
            # Generar el hash basado en el ID
            hash_usuario = generar_hash_usuario(id_usuario)
            
            # Generar el QR con el hash
            nombre_archivo = f"qr_{nombre_usuario}_{id_usuario}.png"
            generar_qr(hash_usuario, nombre_archivo)

            print(f"QR generado para '{nombre_usuario}' (ID: {id_usuario}), guardado como {nombre_archivo}")
        
        # Cerrar la conexión con la base de datos
        cerrar_conexion(conexion_usuarios)

if __name__ == "__main__":
    main()
