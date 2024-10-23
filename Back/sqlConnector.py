import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crear una conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host = 'host',    # Cambia si tu base de datos está en otro servidor
            database ='museos',   # Nombre de la base de datos creada
            user = 'user',   # Reemplaza con tu usuario de MySQL
            password = 'password' # Reemplaza con tu contraseña de MySQL
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos 'museos'")
            return connection
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return None

def close_connection(connection):
    """Cerrar la conexión a la base de datos"""
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")

def crear_usuario_temporal(nombre, edad):
    """Crear un nuevo usuario temporal al escanear un QR"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO Visitante (Nombre, Edad, Puntuacion_trivia) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (nombre, edad, 0))  # Inicializamos la puntuación en 0
            connection.commit()
            print(f"Usuario temporal '{nombre}' creado con éxito.")
        except Error as e:
            print(f"Error al crear usuario temporal: {e}")
        finally:
            close_connection(connection)

def agregar_objeto_escaneado(id_visitante, id_objeto):
    """Registrar el escaneo de un objeto por parte de un usuario en la tabla Objetos_visitante"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO Objetos_visitante (ID_visitante, ID_objeto) VALUES (%s, %s)"
            cursor.execute(insert_query, (id_visitante, id_objeto))
            connection.commit()
            print(f"El objeto con ID {id_objeto} ha sido registrado para el visitante con ID {id_visitante}.")
        except Error as e:
            print(f"Error al registrar el objeto escaneado: {e}")
        finally:
            close_connection(connection)
