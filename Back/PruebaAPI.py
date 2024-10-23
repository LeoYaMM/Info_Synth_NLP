import os
from groq import Groq
from langchain_groq import ChatGroq

api = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api)

# Informacion del museo
info = """Máscara funeraria de Pakal el Grande

Ubicada en la Sala Maya, esta máscara funeraria fue utilizada para cubrir el rostro del gobernante maya K'inich Janaab' Pakal al momento de su entierro, hacia el año 683 d.C. La pieza está hecha de mosaico de jade, uno de los materiales más valorados por los mayas, quienes consideraban que simbolizaba la inmortalidad y la conexión con el mundo espiritual. Los ojos están formados por conchas y obsidiana, destacando la habilidad de los artesanos mayas para trabajar con precisión y belleza estos materiales.

La máscara fue hallada en la Tumba del Templo de las Inscripciones en Palenque, Chiapas, dentro del sarcófago de Pakal, y representa no solo su estatus como rey, sino su transición al mundo de los muertos, donde continuaría su reinado como divinidad. Hoy, esta pieza es uno de los objetos más importantes del patrimonio arqueológico de México, testimonio de la sofisticación y creencias funerarias de la civilización maya."""

# # Parametros
# llm_text = ChatGroq(
#     model="llama3-8b-8192",
#     temperature = 0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]

# ai_msg = llm_text.invoke(messages)
# ai_msg

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Resume la sigueinte informacion: {info}",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)