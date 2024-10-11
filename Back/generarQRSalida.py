import hashlib
import qrcode
import time

# Función para generar el hash basado en el tiempo
def generar_hash_tiempo():
    tiempo = str(time.time())
    hash_obj = hashlib.sha256(tiempo.encode())
    return hash_obj.hexdigest()

# Función para generar el código QR
def generar_qr(hash_tiempo, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_tiempo)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)
    print('QR de salida generado')

# Función principal que une todo
def main():
    # Generar el hash basado en el tiempo
    hash_tiempo = generar_hash_tiempo()
    
    # Generar el QR con el hash
    nombre_archivo = f"qr_salida.png"
    generar_qr(hash_tiempo, nombre_archivo)

if __name__ == "__main__":
    main()