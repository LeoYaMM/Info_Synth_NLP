import mysql.connector
from mysql.connector import Error

def conectar_bd_museo():
    try:
        # Establece la conexión con la base de datos
        conexion = mysql.connector.connect(
            host='127.0.0.1',         
            database='museo',         
            user='root',        
            password='Blow85**'  
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return None

def conectar_bd_usuarios():
    try:
        # Establece la conexión con la base de datos
        conexion = mysql.connector.connect(
            host='127.0.0.1',         
            database='usuarios',         
            user='root',        
            password='Blow85**'  
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return None

def cerrar_conexion(conexion):
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada.")

def obtener_exposiciones(conexion):
    try:
        cursor = conexion.cursor(dictionary=True)  # Para que devuelva los resultados en formato de diccionario
        cursor.execute("SELECT * FROM Exposiciones")

        exposiciones = cursor.fetchall()
        return exposiciones

    except Error as e:
        print(f"Error al obtener los datos: {e}")

# Ejemplo de uso del script
# conexion = conectar_bd_museo()

# if conexion:
#     exposiciones = obtener_exposiciones(conexion)
#     for exposicion in exposiciones:
#         print(f"ID: {exposicion['id']}, Nombre: {exposicion['nombre']}, Descripción: {exposicion['descripcion']}, Sala: {exposicion['sala']}")

#     # Cerrar la conexión al finalizar
#     cerrar_conexion(conexion)
# El output resultante: ID, Elemento expuesto, Descripcion, Sala
