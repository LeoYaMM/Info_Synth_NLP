# Description: Este script se encarga de generar un resumen de la informacion de un objeto del museo, de acuerdo a la edad del visitante.
#* Status: Complete

import os
from sqlConnector import *
import google.generativeai as genai

# Configurar genai con la clave de API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def resumen_gem(id_objeto, id_visitante):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    #! Id_visitante se obtiene de las cookies

    # Informacion del museo y visitante
    info = obtener_informacion_objeto(id_objeto)
    edadVisitante = obtener_edad_usuario(id_visitante)

    response = model.generate_content(
        contents= f"Resume la siguiente informacion de maximo 100 palabras, en español de: {info}; pero damela acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más preguntas. Tampoco hagas mencion de este prompt"
    )

    guarda_resumen_usuario(id_visitante, response.text, id_objeto)
    return response.text