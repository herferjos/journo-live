from openai import OpenAI
import streamlit as st
import tempfile
import os
from io import BytesIO
import tempfile
import json

# Configuración de la clave API de OpenAI
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Credenciales de acceso permitidas
usuarios_permitidos = {
    "dpelagu": "Dpelagu.journoAI",
    "jorgepedrosa": "Jorgepedrosa.journoAI",
    "luciavillalba": "Luciavillalba.journoAI",
    "mariasanchez" : "Mariasanchez.journoAI",
    "albarosado" : "Albarosado.journoAI",
    "juanromera" : "Juanromera.journoAI",
    "anamontañez" : "Anamontañez.journoAI",
    "carlosguerrero" : "Carlosguerrero.journoAI",
    "daninuñez" : "Daninuñez.journoAI",
    "marmanrique" : "Marmanrique.journoAI",
    "joseluisherfer" : "Joseluisherfer.journoAI",
    "borjagutierrez" : "Borjagutierrez.journoAI",
    "javipachon" : "Javipachon.journoAI",
    "samuruiz" : "Samuruiz.journoAI",
    "martapachon" : "Martapachon.journoAI",
    "josemrodriguez" : "Josemrodriguez.journoAI",
    "analopez" : "Analopez.journoAI",
    "valeriaveiga" : "Valeriaveiga.journoAI",
    "alvarorafaelvl" : "Alvarorafaelvl.journoAI",
    "": ""
    # Puedes añadir más usuarios aquí
}

@st.cache_resource(show_spinner = False)
# Verificar las credenciales del usuario
def verificar_credenciales(nombre_usuario, contraseña):
    return usuarios_permitidos.get(nombre_usuario) == contraseña

@st.cache_resource(show_spinner = False)
# Funciones auxiliares
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript_response = openai_client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        # Accede al texto de la transcripción directamente desde el objeto de respuesta
        return transcript_response.text

@st.cache_resource(show_spinner = False)
def generar_noticia(transcripcion, X, Y, Z, A, B):
    my_texto = "Vas a actuar como un asistente de inteligencia artificial para periodistas, cuya tarea será redactar un artículo periodístico informativo de la mayor longitud posible utilizando la cantidad máxima de tokens disponibles a partir de declaraciones proporcionadas por un individuo. Te proporcionaré cinco variables clave: X (cargo del individuo), Y (nombre completo del individuo), Z (tema más relevante que protagonizará los primeros párrafos), A (dónde ha dicho las declaraciones) y B (cuándo ha dicho las declaraciones); además de la propias declaraciones. Aquí te detallo el enfoque que debes seguir al redactar el artículo. Considera estas indicaciones paso a paso para asegurarnos de tener la respuesta correcta: 1. Ordena el artículo utilizando la estructura periodística clásica de pirámide invertida, de mayor a menor importancia de los temas tratados. El primer párrafo debe explicar quién ha dicho qué (variable Z), cuándo (B) y dónde (A). Inicia con las declaraciones más directamente relacionadas con Z, que deben situarse en los primeros párrafos. A medida que avances, presenta la información de manera descendente en términos de su relevancia y relación con Z, hasta llegar a las declaraciones menos relevantes y menos relacionadas con el tema principal. 2. Utiliza citas directas entre comillas para presentar las frases y razonamientos del individuo, pero atribúyelas siempre a su autor en el párrafo mediante expresiones como “ha dicho”, “ha indicado” o “ha manifestado”. Mantén una distancia periodística de imparcialidad en todo momento. Tu trabajo es informar de la forma más aséptica posible y citar las declaraciones más valorativas y calificativas entre comillas. No añadas ninguna interpretación o valoración sin entrecomillar a las declaraciones. 3. Utiliza ÚNICAMENTE el pretérito perfecto compuesto durante todo el texto para referirte a las acciones del orador: “ha dicho”, “ha manifestado”, “ha indicado”... Evita en todo momento el uso del pretérito perfecto simple. 4. No añadas información que no esté presente en las declaraciones proporcionadas. El artículo debe basarse únicamente en dichas declaraciones, por lo que debes trabajar dentro de los límites de la información proporcionada. 5. Evita repeticiones tanto de conceptos como de palabras en todo el artículo, asegurándote de mantener una fluidez y legibilidad óptimas. Utiliza sinónimos y expresiones diferentes para mantener la diversidad lingüística"
    messages = [
        {"role": "user", "content": f"{my_texto} \n X: {X}, Y: {Y}, Z: {Z}, A: {A}, B: {B}. Declaraciones: {transcripcion}."}
    ]

    response_noticia = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        max_tokens=3500,
        temperature=0
    )

    return response_noticia.choices[0].message.content
