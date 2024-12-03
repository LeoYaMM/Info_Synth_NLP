# Description: Este script se encarga de conectarse con el front y el back para realizar la lectura de los QRs y la generación de preguntas de trivia.
#! Status: In Progress
from fastapi.staticfiles import StaticFiles
from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlConnector import *
from GeminiAPIResumen import resumen_Gemini
from GeminiAPITrivia import *
import json
import logging

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["*"] para permitir todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Esta linea hace la configuracion para que lea los archivos HTML del front
# app.mount("/Front", StaticFiles(directory="Front", html=True), name="Front")

# # aqui se define la ruta principal para que mande al index
# @app.get("/")
# async def read_index():
#     return RedirectResponse(url="../Front/indexG.html")

# Pydantic model para las peticiones del QR
class QRRequest(BaseModel): # Pydantic model para los QR
    qr_data: str # Datos del QR
    id_visitante: int  # ID del visitante a partir de las cookies

class Visitante(BaseModel): # Pydantic model para los visitantes
    nombre: str
    edad: int

# Modelo para recibir la solicitud
class TriviaRequest(BaseModel):
    id_visitante: int
    noResumen: int

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
    resumen = resumen_Gemini(id_objeto, id_visitante)
    
    return {"resumen": resumen}

# Ruta para la trivia
# @app.post("/trivia")  
# async def trivia(request: TriviaRequest):
#     print("entrando al back jej")
#     scanCount = request.noResumen
    
#     info = obtener_resumenes_visitantes(request.id_visitante)
#     edadVisitante = obtener_edad_usuario(request.id_visitante)

#     pregunta = pregunta_trivia_Gemini(info[scanCount], edadVisitante, request.id_visitante)
#     logging.info(pregunta)
#     return pregunta

@app.post("/trivia")
async def trivia(request: TriviaRequest):
    print("entrando al back jej")
    scanCount = request.noResumen
    info = obtener_resumenes_visitantes(request.id_visitante)
    edadVisitante = obtener_edad_usuario(request.id_visitante)
    
    # Procesar las preguntas antes de hacer el return
    preguntas = []
    for i in range(scanCount):
        pregunta = pregunta_trivia_Gemini(info[i], edadVisitante, request.id_visitante)
        preguntas.append(pregunta)
    
    # Devolver todas las preguntas procesadas
    return {"preguntas": preguntas}



#TODO: Para correr el servidor de FastAPI: uvicorn Backend:app --reload