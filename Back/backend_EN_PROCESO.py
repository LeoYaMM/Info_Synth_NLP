# Description: Este script se encarga de conectarse con el front y el back para realizar la lectura de los QRs y la generación de preguntas de trivia.
#! Status: In Progress

from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlConnector import *
import hashlib
from LlamaAPIResumen import resumen_Llama

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["*"] para permitir todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Pydantic model para las peticiones del QR
class QRRequest(BaseModel): # Pydantic model para los QR
    qr_data: str # Datos del QR
    id_visitante: int  # ID del visitante a partir de las cookies

class Visitante(BaseModel): # Pydantic model para los visitantes
    nombre: str
    edad: int

# Ruta para registrar un visitante
@app.post("/registrar_visitante") #* Funciona correctamente
async def registrar_visitante(visitante: Visitante):
    # Crea un usuario temporal en la base de datos
    crear_usuario_temporal(visitante.nombre, visitante.edad)

    # Retorna el id del usuario temporal para guardar en las cookies
    id_visitante = obtener_id_visitante(visitante.nombre, visitante.edad)
    
    # Verifica si se obtuvo un id y retorna el JSON
    if id_visitante:
        return {"id_visitante": id_visitante}
    else:
        raise HTTPException(status_code=500, detail="Error al crear visitante")

# Ruta que recibe el QR
@app.post("/scan_qr")  #* Funciona correctamente
async def scan_qr(qr_request: QRRequest):
    qr_data = qr_request.qr_data
    id_visitante = qr_request.id_visitante
    
    # Desencriptar el QR y obtener el id_objeto
    id_objeto = obtener_id_objeto(qr_data)
    if id_objeto is None:
        raise HTTPException(status_code=400, detail="Error al desencriptar el hash.")
    
    # Obtener el resumen usando id_objeto e id_visitante
    resumen = resumen_Llama(id_objeto, id_visitante)
    
    return {"resumen": resumen}


#! Revisa el flujo de aplicacion terminal si tienes dudas

#! Endpoint para enviar finalizar el recorrido

# Para correr el servidor de FastAPI: uvicorn main:app --reload