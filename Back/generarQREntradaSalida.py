import hashlib
import qrcode
from sqlConnector import *

# Función para generar el hash basado en el id_sala
def generar_hash_sala(id_sala):
    id_str = str(id_sala)
    hash_obj = hashlib.sha256(id_str.encode())
    return hash_obj.hexdigest()

# Función para generar el código QR de entrada
def generar_qr_entrada(hash_sala, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_sala)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)
    print('QR de entrada generado')

# Función principal
def main():
    # Generar el hash basado en el id_sala
    for id_sala in obtener_id_salas():
        hash_sala = generar_hash_sala(id_sala)
        # Generar el QR de entrada
        nombre_archivo_entrada = f"qr_entrada_{id_sala}.png"
        generar_qr_entrada(hash_sala, nombre_archivo_entrada)

if __name__ == "__main__":
    main()