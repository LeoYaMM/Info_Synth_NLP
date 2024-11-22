# Description: Aqui se encuentran las funciones que se encargan de la conexión con la base de datos
#! Status: In Progress

import mysql.connector
from mysql.connector import Error

# Funcion para crear la conexión a la base de datos
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

# Funcion para crear la conexión a la base de datos
def close_connection(connection):
    """Cerrar la conexión a la base de datos"""
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")

# Funcion para crear un nuevo usuario temporal, no retorna nada
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

#Funcion para guardar el HASH generado en la base de datos, no retorna nada
def guardar_hash(hash_qr, id_objeto):
    """Guardar el HASH generado en la base de datos para un objeto específico"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = "UPDATE objeto_historico SET hash = %s WHERE ID_objeto = %s"
            cursor.execute(update_query, (hash_qr, id_objeto))
            connection.commit()
            print(f"Hash '{hash_qr}' guardado con éxito para el objeto ID {id_objeto}.")
        except Error as e:
            print(f"Error al guardar el hash: {e}")
        finally:
            close_connection(connection)

# Funcion para obtener el HASH generado para un objeto específico dado el HASH, retorna el id_objeto
def obtener_id_objeto(hash_qr):
    """Obtener el ID del objeto histórico asociado a un HASH específico"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT ID_objeto FROM objeto_historico WHERE hash = %s"
            cursor.execute(select_query, (hash_qr,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Error as e:
            print(f"Error al obtener el ID del objeto: {e}")
        finally:
            close_connection(connection)

# Funcion para obtener el id del visitante, retorna el id del visitante
def obtener_id_visitante(nombre, edad):
    """Obtener el ID de un visitante en la tabla Visitante"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT ID_visitante FROM Visitante WHERE Nombre = %s AND Edad = %s"
            cursor.execute(select_query, (nombre, edad))

            id_visitante = cursor.fetchone()
            if id_visitante is not None:
                print(f"ID del visitante '{nombre}' encontrado")
                return id_visitante
            else:
                print(f"No se encontró un visitante con el nombre '{nombre}'.")
        except Error as e:
            print(f"Error al obtener el ID del visitante: {e}")
        finally:
            close_connection(connection)

# Agrega un objeto escaneado por un usuario asociado con su ID de visitante, no retorna nada
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

# Obtiene la informacion de un objeto escaneado por un usuario a traves de el ID del objeto, retorna la informacion del objeto en la base de datos
def obtener_informacion_objeto(id_objeto):
    """Obtener la información de un objeto en la tabla Objetos"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Information FROM objeto_historico WHERE ID_objeto = %s"
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

# Obtiene la edad del usuario, retorna un entero
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

# Obtiene el id de la sala, retorna un entero
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

# Guarda el resumen, no retorna nada
def guarda_resumen_usuario(id_visitante, resumen, id_objeto):
    """Guardar el resumen generado por el modelo en la tabla Resumen"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO Resumen (ID_visitante, Texto,  ID_objeto) VALUES (%s, %s, %s)"

            cursor.execute(insert_query, (id_visitante, resumen, id_objeto))
            connection.commit()
            print(f"Resumen del objeto {id_objeto} guardado para el visitante {id_visitante}.")
        except Error as e:
            print(f"Error al guardar el resumen: {e}")
        finally:
            close_connection(connection)

# Obtiene los resumenes generados para un visitante, retorna una lista de los resumenes por usuario
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

# Obtiene el resumen generado para un objeto específico, retorna el resumen correspondiente al id_objeto
def obtener_resumen_objeto(id_objeto, id_visitante):
    """Obtener el resumen generado para un objeto en la tabla Resumen"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Texto FROM Resumen WHERE ID_objeto = %s AND ID_visitante = %s"
            cursor.execute(select_query, (id_objeto, id_visitante))
            resumen = cursor.fetchone()  # Usamos fetchone porque esperamos solo un resumen para el objeto
            if resumen:
                print(f"Resumen generado para el objeto con ID {id_objeto} para el visitante {id_visitante} obtenido con éxito")
                return resumen[0]  # Retorna el contenido del resumen directamente
            else:
                print(f"No se encontró un resumen para el objeto con ID {id_objeto}.")
                return None
        except Error as e:
            print(f"Error al obtener el resumen de un objeto: {e}")
        finally:
            close_connection(connection)

# Agrega el nombre del visitante a la base de datos, no retorna nada
def agregar_nombre_visitante(id_visitante, nombre):
    """Agregar el nombre de un visitante a la tabla Visitante"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = "UPDATE Visitante SET Nombre = %s WHERE ID_visitante = %s"
            cursor.execute(update_query, (nombre, id_visitante))
            connection.commit()
            print(f"Nombre del visitante con ID {id_visitante} actualizado con éxito.")
        except Error as e:
            print(f"Error al agregar el nombre del visitante: {e}")
        finally:
            close_connection(connection)

# Guarda la pregunta generada por el modelo, no retorna nada
def guarda_pregunta_trivia(id_visitante, pregunta):
    """Guardar la pregunta generada por el modelo en la tabla Trivia"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO Trivia (ID_visitante, Pregunta) VALUES (%s, %s)"
            cursor.execute(insert_query, (id_visitante, pregunta))
            connection.commit()
            print(f"Pregunta de trivia guardada para el visitante {id_visitante}.")
        except Error as e:
            print(f"Error al guardar la pregunta de trivia: {e}")
        finally:
            close_connection(connection)

# Guarda la respuesta del usuario a una pregunta de trivia, no retorna nada
def guarda_respuesta_trivia(id_visitante, respuesta, pregunta):
    """Guardar la respuesta del usuario a una pregunta de trivia en la tabla Trivia"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = "UPDATE Trivia SET Respuesta_usuario = %s WHERE ID_visitante = %s AND pregunta = %s"
            cursor.execute(update_query, (respuesta, id_visitante, pregunta))
            connection.commit()
            print(f"Respuesta de trivia guardada para el visitante {id_visitante}.")
        except Error as e:
            print(f"Error al guardar la respuesta de trivia: {e}")
        finally:
            close_connection(connection)

# Obtiene las preguntas de trivia generadas para un visitante, retorna una lista de las preguntas por usuario
def obtener_preguntas_trivia(id_visitante):
    """Obtener las preguntas de trivia generadas para un visitante en la tabla Trivia"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Pregunta FROM Trivia WHERE ID_visitante = %s"
            cursor.execute(select_query, (id_visitante,))
            preguntas = cursor.fetchall()
            if preguntas:
                print(f"Preguntas de trivia generadas para el visitante con ID {id_visitante} obtenidas con éxito.")
                return preguntas
            else:
                print(f"No se encontraron preguntas de trivia para el visitante con ID {id_visitante}.")
        except Error as e:
            print(f"Error al obtener las preguntas de trivia de un visitante: {e}")
        finally:
            close_connection(connection)

# Obtiene las respuestas de trivia dadas por un visitante, retorna una lista de las respuestas por usuario
def obtener_respuestas_trivia(id_visitante):
    """Obtener las respuestas de trivia dadas por un visitante en la tabla Trivia"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT Respuesta_usuario FROM Trivia WHERE ID_visitante = %s"
            cursor.execute(select_query, (id_visitante,))
            respuestas = cursor.fetchall()
            if respuestas:
                print(f"Respuestas de trivia dadas por el visitante con ID {id_visitante} obtenidas con éxito.")
                return respuestas
            else:
                print(f"No se encontraron respuestas de trivia para el visitante con ID {id_visitante}.")
        except Error as e:
            print(f"Error al obtener las respuestas de trivia de un visitante: {e}")
        finally:
            close_connection(connection)

def agregar_edad_visitante(id_visitante, edad):
    """Agregar la edad de un visitante a la tabla Visitante"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = "UPDATE Visitante SET Edad = %s WHERE ID_visitante = %s"
            cursor.execute(update_query, (edad, id_visitante))
            connection.commit()
            print(f"Edad del visitante con ID {id_visitante} actualizada con éxito.")
        except Error as e:
            print(f"Error al agregar la edad del visitante: {e}")
        finally:
            close_connection(connection)