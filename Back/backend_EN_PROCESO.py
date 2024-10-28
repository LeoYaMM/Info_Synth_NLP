# Description: Este script se encarga de conectarse con el front y el back para realizar la lectura de los QRs y la generación de preguntas de trivia.
#! Status: In Progress

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlConnector import *
import hashlib
from LlamaAPIResumen import resumen_Llama

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

# Ruta que recibe el QR
@app.post("/scan_qr/")
async def scan_qr(qr_request: QRRequest):
    qr_data = qr_request.qr_data
    # Desencriptamos el hash
    id_objeto = desencriptar_hash(qr_data)
    
    if id_objeto is None:
        raise HTTPException(status_code=400, detail="Error al desencriptar el hash.")
    
    # Pasa el ID del objeto a LlamaAPIResumen para obtener el resumen
    

# Endpoint para obtener el resumen según el topic_id
@app.get("/get_summary/{topic_id}")
async def get_summary(topic_id: int):
    # Obtener el resumen de la base de datos
    summary = obtener_resumen_objeto(id_objeto, id_visitante)
    
    # Si el resumen no existe, devolver un mensaje de error
    if not summary:
        return {"error": "Resumen no encontrado"}
    
    return {"summary": summary}

# Para correr el servidor de FastAPI: uvicorn main:app --reload