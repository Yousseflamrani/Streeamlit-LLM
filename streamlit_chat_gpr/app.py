import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

client = OpenAI (
    api_key = os.getenv("GROQ_API_KEY"),
    base_url= os.getenv("GROQ_API_URL")
)

st.set_page_config(page_title="Artificiel Education", page_icon="💬")
st.title("💬 Artificiel Education")
st.markdown("Pose une question sur un sujet scolaire et reçois une explication claire !")

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

#--- Fonctions ---
def create_new_conversation():
    conv_id = str(uuid.uuid4())
    st.session_state.conversations[conv_id] = [
        {"role": "system", "content": "Tu es un assistant pédagogique, clair et simple."}
    ]
    st.session_state.current_conv_id = conv_id


def delete_conversation():
    current_id = st.session_state.current_conv_id
    if current_id:
        st.session_state.conversations.pop(current_id, None)
        st.session_state.current_conv_id = None
        st.rerun()

def get_label(messages):
    if len(messages) > 1:
        return messages[1]["content"][:30] + "..."
    return "Nouvelle conversation"


# --- Sidebar : gestion des conversations ---
st.sidebar.title("📚 Conversations")

for conv_id in list(st.session_state.conversations):
    messages = st.session_state.conversations[conv_id]
    label = get_label(messages)
    if st.sidebar.button(label, key=f"select_{conv_id}"):
        st.session_state.current_conv_id = conv_id


st.sidebar.markdown("---")
if st.sidebar.button("➕ Nouvelle conversation"):
    create_new_conversation()
    st.rerun()

if st.session_state.current_conv_id and st.sidebar.button("🗑️ Supprimer cette conversation"):
    delete_conversation()

conv_id = st.session_state.current_conv_id

prompt = st.chat_input("Écris ton message ici ...")

# Affichage et gestion de la conversation sélectionnée 
if prompt and not conv_id:
    create_new_conversation()
    conv_id = st.session_state.current_conv_id

if conv_id:
    messages = st.session_state.conversations[conv_id]

    # Affichage des messages
    for msg in messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Zone d'entrée
    if prompt:
        # Afficher le message utilisateur
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

 # Générer une réponse simulée
    # response = f"🤖 Réponse de GPR : '{prompt[::-1]}'"  # Réponse inversée pour l'exemple
    # st.session_state.messages.append({"role": "assistant", "content": response})
    # with st.chat_message("assistant"):
    #     st.markdown(response)
        with st.chat_message("assistant"):
            with st.spinner("🤖 Réflexion ..."):
                try: 
                    response = client.chat.completions.create(
                        # model méta
                        model = "llama3-70b-8192",
                        # model google
                        # model= "gemma2-9b-it",
                        messages = messages,
                        temperature = 0.6,
                        max_tokens = 800
                    )
                    reply = response.choices[0].message.content
                except Exception as e :
                    reply = f"❌ Erreur : {e}"
            
            st.markdown(reply)
            messages.append({"role": "assistant", "content": reply})