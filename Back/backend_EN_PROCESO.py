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
    allow_origins=["http://127.0.0.1:5500"],  # O usa ["*"] para permitir todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

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
class QRRequest(BaseModel): # Pydantic model para los QR
    qr_data: str  # Este es el hash escaneado

class Visitante(BaseModel): # Pydantic model para los visitantes
    nombre: str
    edad: int

# Ruta para registrar un visitante
@app.post("/registrar_visitante")
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
@app.post("/scan_qr/")
async def scan_qr(qr_request: QRRequest):
    qr_data = qr_request.qr_data
    # Desencriptamos el hash
    id_objeto = desencriptar_hash(qr_data)
    
    if id_objeto is None:
        raise HTTPException(status_code=400, detail="Error al desencriptar el hash.")
    
    # Pasa el ID del objeto a LlamaAPIResumen para obtener el resumen
    resumen = resumen_Llama(id_objeto)


# Para correr el servidor de FastAPI: uvicorn main:app --reload