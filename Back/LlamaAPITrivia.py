# Description: Este script se encarga de generar preguntas para la trivia, de acuerdo a la edad del visitante y la info recopilada.
#! Status: In Progress

import os
from sqlConnector import *
from groq import Groq
from langchain_groq import ChatGroq


api = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api)

#! Obtiene el id del visitante de las cookies

# Informacion de los resumenes y la edad del visitante
info = obtener_resumenes_visitantes(1) # Lista de resumenes
edadVisitante = obtener_edad_usuario(1)

#! Falta iterar los resumenes para obtener una pregunta
print(info)

for i in range(10):
    # Formulacion de la pregunta
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"A partir de estos resumenes: {info}, dame una pregunta de opción multiple en español; limitatate a dar solo las preguntas con sus opciones nada mas pero damela en nivel de dificultad acorde a mi edad {edadVisitante}, al final de tu respuesta no hagas más preguntas)",
            }
        ],
        model="llama3-8b-8192",
        temperature=1,
    )
    print(chat_completion.choices[0].message.content)

'''#! Falta iterar para generar las opciones multiple

# Formulacion de la respuesta correcta
chat_completion2 = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Las respuestas correctas son: {info}",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)

#! Falta iterar para escoger la respuesta correcta de la lista de opcion multiple

#! Falta guardar las preguntas y respuestas en la tabla Trivia'''