# Description: Este script se encarga de generar un resumen de la informacion de un objeto del museo, de acuerdo a la edad del visitante.
#* Status: Complete

import os
from .sqlConnector import *
import google.generativeai as genai

# Configurar genai con la clave de API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def resumen_Gemini(id_objeto, id_visitante):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    #! Id_visitante se obtiene de las cookies

    # Informacion del museo y visitante
    info = obtener_informacion_objeto(id_objeto)
    edadVisitante = obtener_edad_usuario(id_visitante)

    response = model.generate_content(
        contents= f"Summarize the following information in a maximum of 100 words, in English: {info}; but give it to me according to my age {edadVisitante}, at the end of your answer do not ask any more questions. Also do not mention this prompt."
    )

    guarda_resumen_usuario(id_visitante, response.text, id_objeto)
    return response.text