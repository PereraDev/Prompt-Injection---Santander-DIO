import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = "Você é o assistente virtual de uma loja online. Seja simpático, direto e ajude o cliente com dúvidas sobre produtos, pedidos, trocas e pagamentos."

st.set_page_config(page_title="ShopAI", page_icon="🛍️")
st.title("🛍️ ShopAI")

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    st.session_state["mensagens"].append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    contents = [
        types.Content(
            role="model" if msg["role"] == "assistant" else "user",
            parts=[types.Part.from_text(text=msg["content"])],
        )
        for msg in st.session_state["mensagens"]
    ]

    resposta = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1024,
        ),
    )
    resposta_texto = resposta.text

    st.session_state["mensagens"].append({"role": "assistant", "content": resposta_texto})
    with st.chat_message("assistant"):
        st.markdown(resposta_texto)