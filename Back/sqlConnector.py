# Description: Aqui se encuentran las funciones que se encargan de la conexión con la base de datos

import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crear una conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host = '127.0.0.1',
            database ='museo',  
            user = 'root',  
            password = 'Blow85**'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos 'museo'")
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
            insert_query = "INSERT INTO Visitante (Nombre, Edad, Puntuacion_trivia) VALUES (%s, %s, %s)" # Información dada desde el frontend
            cursor.execute(insert_query, (nombre, edad, 0))
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

def obtener_informacion_objeto(id_objeto):
    """Obtener la información de un objeto en la tabla Objetos"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Informacion FROM objeto_historico WHERE ID_objeto = %s"
            cursor.execute(select_query, (id_objeto,))
            objeto = cursor.fetchone()
            if objeto is not None:
                print(f"Información encontrada del objeto con ID {id_objeto}")
                return objeto
            else:
                print(f"No se encontró un objeto con ID {id_objeto}.")
        except Error as e:
            print(f"Error al obtener información del objeto: {e}")
        finally:
            close_connection(connection)

def obtener_edad_usuario(id_visitante):
    """Obtener la edad de un usuario en la tabla Visitante"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Edad FROM Visitante WHERE ID_visitante = %s"
            cursor.execute(select_query, (id_visitante,))
            edad = cursor.fetchone()
            if edad is not None:
                print(f"Edad del usuario con ID {id_visitante} encontrada")
                return edad
            else:
                print(f"No se encontró un usuario con ID {id_visitante}.")
        except Error as e:
            print(f"Error al obtener la edad del usuario: {e}")
        finally:
            close_connection(connection)

def obtener_id_salas():
    """Obtener los IDs de las salas en la tabla Sala"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT ID_sala FROM Sala"
            cursor.execute(select_query)
            salas = cursor.fetchall()
            if salas:
                print("IDs de las salas:")
                print(salas)
                return salas
            else:
                print("No se encontraron salas.")
        except Error as e:
            print(f"Error al obtener los IDs de las salas: {e}")
        finally:
            close_connection(connection)

def guarda_resumen_usuario(id_visitante, resumen):
    """Guardar el resumen generado por el modelo en la tabla Resumen"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO Resumen (ID_visitante, Texto) VALUES (%s, %s)"
            cursor.execute(insert_query, (id_visitante, resumen))
            connection.commit()
            print(f"Resumen guardado para el visitante con ID {id_visitante}.")
        except Error as e:
            print(f"Error al guardar el resumen: {e}")
        finally:
            close_connection(connection)

def obtener_resumenes_visitantes(id_visitante):
    """Obtener los resúmenes generados para un visitante en la tabla Resumen"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Texto FROM Resumen WHERE ID_visitante = %s"
            cursor.execute(select_query, (id_visitante,))
            resumenes = cursor.fetchall()
            if resumenes:
                print(f"Resúmenes generados para el visitante con ID {id_visitante} tomado con éxito")
                return resumenes
            else:
                print(f"No se encontraron resúmenes para el visitante con ID {id_visitante}.")
        except Error as e:
            print(f"Error al obtener los resúmenes de un visitante: {e}")
        finally:
            close_connection(connection)