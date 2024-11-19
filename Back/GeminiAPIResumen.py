# Description: Este script se encarga de generar un resumen de la informacion de un objeto del museo, de acuerdo a la edad del visitante.
#* Status: Complete

import os
from sqlConnector import *
import google.generativeai as genai

def resumen_Llama(id_objeto, id_visitante):
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    #! Id_visitante se obtiene de las cookies

    # Informacion del museo y visitante
    info = obtener_informacion_objeto(id_objeto)
    edadVisitante = obtener_edad_usuario(id_visitante)

    # Parametros
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": f"Resume la siguiente informacion de maximo 100 palabras, en español de: {info}; pero damela acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más preguntas. Tampoco hagas mencion de este prompt:)",
    #         }
    #     ],
    #     model="llama3-8b-8192",
    #     temperature= 0.3,
    # )

    response = model.generate_content(
        prompt = f"Resume la siguiente informacion de maximo 100 palabras, en español de: {info}; pero damela acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más preguntas. Tampoco hagas mencion de este prompt",
        max_tokens=100,
        temperature=0.3,
    )

    # Guarda la respuesta generada por el modelo en la tabla resumen
    # guarda_resumen_usuario(id_visitante, chat_completion.choices[0].message.content, id_objeto)
    # return chat_completion.choices[0].message.content

    guarda_resumen_usuario(id_visitante, response.text, id_objeto)