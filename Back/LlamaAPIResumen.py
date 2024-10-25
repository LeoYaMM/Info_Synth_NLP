# Description: Este script se encarga de generar un resumen de la informacion de un objeto del museo, de acuerdo a la edad del visitante.

import os
from sqlConnector import *
from groq import Groq
from langchain_groq import ChatGroq


api = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api)

#! Id_visitante se obtiene de las cookies

# Informacion del museo y visitante
info = obtener_informacion_objeto(1)
edadVisitante = obtener_edad_usuario(1)

# Parametros
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Resume y complementa la sigueinte informacion de maximo 100 palabras: {info}; pero damela acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más preguntas :)",
        }
    ],
    model="llama3-8b-8192",
    temperature= 0.3,
)

print(chat_completion.choices[0].message.content)

# Guarda la respuesta generada por el modelo en la tabla resumen
guarda_resumen_usuario(2, chat_completion.choices[0].message.content)