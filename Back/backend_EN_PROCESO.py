# Description: Este script se encarga de conectarse con el front y el back para realizar la lectura de los QRs y la generación de preguntas de trivia.
#! Status: In Progress

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlConnector import *
import hashlib

app = FastAPI()

# Función para desencriptar el hash (ejemplo simple con hashlib)
def desencriptar_hash(hash_qr: str) -> str:
    try:
        # Aquí se realiza la lógica de desencriptación
        # Por ejemplo, simplemente un hash reverso (esto solo es ilustrativo)
        decoded_data = hashlib.sha256(hash_qr.encode()).hexdigest()  # Ejemplo de hash
        return decoded_data
    except Exception as e:
        print(f"Error al desencriptar hash: {e}")
        return None

# Pydantic model para las peticiones del QR
class QRRequest(BaseModel):
    qr_data: str  # Este es el hash escaneado

# Ruta que recibe el QR y consulta la base de datos
@app.post("/scan_qr/")
async def scan_qr(qr_request: QRRequest):
    qr_data = qr_request.qr_data
    # Desencriptamos el hash
    desencriptado = desencriptar_hash(qr_data)
    
    if desencriptado is None:
        raise HTTPException(status_code=400, detail="Error al desencriptar el hash.")
    
    # Aquí realizar la validación con la base de datos
    connection = create_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos.")
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Visitante WHERE ID_visitante = %s"  # Ajusta según tu necesidad
        cursor.execute(query, (desencriptado,))
        result = cursor.fetchone()

        if result:
            # Si existe el visitante, devolvemos sus datos
            return {"status": "success", "data": result}
        else:
            raise HTTPException(status_code=404, detail="Visitante no encontrado.")
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {e}")
    finally:
        close_connection(connection)

# Para correr el servidor de FastAPI: uvicorn main:app --reload