import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3

# Set your OpenAI API key
openai.api_key = "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"

# Configuración de la página
st.set_page_config(page_title="Pharmacist Bot", page_icon="💊")

# Estilos globales: navy, blanco y fuente moderna
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #001F3F; /* Azul Navy */
        color: white;
    }

    .stApp {
        background-color: #001F3F;
        color: white;
    }

    h1, h2, h3, h4 {
        color: white;
    }

    .stButton > button {
        background-color: #0074D9;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
    }

    .stButton > button:hover {
        background-color: #005fa3;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado con dos columnas para las imágenes
col1, col2 = st.columns([1, 1])
with col1:
    st.image("PharmaEdu.png", width=130)
with col2:
    st.image("pharma_bot_character.png", width=130)

# Título
st.markdown("<h1 style='text-align:center;'>PharmaEdu AI Assistant</h1>", unsafe_allow_html=True)

st.write("🎙️ Click the button below to ask your question about your medications:")

# Botón para entrada por voz
if st.button("🎤 Ask by Voice"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening to your question...")
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio, language="en-US")
        st.success(f"🗣️ You asked: {question}")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content

        # Caja de respuesta con fondo blanco y letra oscura
        st.markdown(f"""
            <div style='background-color: white; color: #001F3F; padding: 15px;
                        border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        margin-top: 20px;'>
                <strong>🤖 Bot's Answer:</strong><br>{answer}
            </div>
        """, unsafe_allow_html=True)

        # Reproducir respuesta
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(answer)
        engine.runAndWait()

    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand what you said.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
