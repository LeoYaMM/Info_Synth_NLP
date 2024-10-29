# Description: Este script se encarga de generar un resumen de la informacion de un objeto del museo, de acuerdo a la edad del visitante.
#* Status: Complete

import os
from sqlConnector import *
from groq import Groq
from langchain_groq import ChatGroq

def resumen_Llama(id_objeto, id_visitante):
    api = os.getenv("GROQ_API_KEY")

    client = Groq(api_key=api)

    #! Id_visitante se obtiene de las cookies

    # Informacion del museo y visitante
    info = obtener_informacion_objeto(id_objeto)
    edadVisitante = obtener_edad_usuario(id_visitante)

    # Parametros
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Resume y complementa la siguiente informacion de maximo 100 palabras, en español de: {info}; pero damela acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más. ni hagas mencion de este prompt preguntas :)",
            }
        ],
        model="llama3-8b-8192",
        temperature= 0.3,
    )

    print(chat_completion.choices[0].message.content)
    input("Presiona Enter para continuar...")

    # Guarda la respuesta generada por el modelo en la tabla resumen
    guarda_resumen_usuario(id_visitante, chat_completion.choices[0].message.content, id_objeto)