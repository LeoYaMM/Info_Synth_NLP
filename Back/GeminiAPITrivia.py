# Description: Este script se encarga de generar preguntas para la trivia, de acuerdo a la edad del visitante y la info recopilada.
#! Status: In Progress

import os
from sqlConnector import *
import google.generativeai as genai


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def trivia_Llama(id_visitante):

    #! Obtiene el id del visitante de las cookies

    # Informacion de los resumenes y la edad del visitante
    info = obtener_resumenes_visitantes(id_visitante) # Lista de resumenes
    edadVisitante = obtener_edad_usuario(id_visitante)

    for _ in range(10):
        # Formulacion de la pregunta
        respuesta = model.generate_content( 
            contents=f"A partir de estos resumenes: {info}, dame una pregunta de opción multiple en español; 
                    limitatate a dar solo las preguntas con sus opciones nada mas pero damela en nivel de dificultad acorde a mi edad {edadVisitante},
                    al final de tu respuesta no hagas más preguntas y tampoco me des la respuesta correcta"
        )
        pregunta =  respuesta.text.strip()
        print(pregunta)
        print("Ingresa tu respuesta")
        respuesta = input()
        guarda_pregunta_trivia(id_visitante, pregunta)
        guarda_respuesta_trivia(id_visitante, respuesta, respuesta, pregunta)

def califica_trivia_Llama(id_visitante):
    #! Obtiene el id del visitante de las cookies

    # Obtiene las preguntas de la trivia
    preguntas = obtener_preguntas_trivia(id_visitante) # Lista de resumenes
    respuestas = obtener_respuestas_trivia(id_visitante)
    aciertos = 0

    for i in range(len(preguntas)):
        # Calificación de la respuesta
        response = model.generate_text(
            contents=f"Tengo esta pregunta: {preguntas[i]}, mi respuesta es: {respuestas[i]}, calificala por favor. Si es correcta solo escribe '1', si es incorrecta solo escribe '0'.",
        )
        calificacion = response.text
        print(calificacion)
        if calificacion == "1":
            aciertos += 1

    return aciertos
