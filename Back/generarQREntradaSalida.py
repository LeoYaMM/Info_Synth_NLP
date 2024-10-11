import hashlib
import qrcode
import time
import random

# Función para generar el hash aleatorio basado en el tiempo
def generar_hash_tiempo():
    # Generar un número aleatorio
    numero_aleatorio = random.randint(0, 1000)
    
    # Obtener el tiempo actual
    tiempo_actual = time.time()
    
    # Convertir el tiempo a una cadena
    tiempo_str = str(tiempo_actual)
    
    # Concatenar el tiempo y el número aleatorio
    texto = tiempo_str + str(numero_aleatorio)
    
    # Crear un objeto hash
    hash_obj = hashlib.sha256(texto.encode())
    
    # Devolver el hash en formato hexadecimal
    return hash_obj.hexdigest()

# Función para generar el código QR de entrada
def generar_qr_entrada(hash_tiempo, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_tiempo)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)
    print('QR de entrada generado')

# Función para generar el código QR de salida
def generar_qr_salida(hash_tiempo, nombre_archivo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(hash_tiempo)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(nombre_archivo)
    print('QR de salida generado')

# Función principal que une todo
def main():
    # Generar el hash basado en el tiempo
    hash_tiempo_entarda = generar_hash_tiempo()
    hash_tiempo_salida = generar_hash_tiempo()
    
    # Generar el QR con el hash
    nombre_archivo = f"qr_entrada.png"
    generar_qr_entrada(hash_tiempo_entarda, nombre_archivo)
    nombre_archivo = f"qr_salida.png"
    generar_qr_salida(hash_tiempo_salida, nombre_archivo)

if __name__ == "__main__":
    main()