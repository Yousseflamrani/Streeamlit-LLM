import streamlit as st

st.set_page_config(page_title="Deep Chat", page_icon="💬")
st.title("💬 Mon Deep Learning Chat")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Zone d'entrée
if prompt := st.chat_input("Écris ton message ici ..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

 # Générer une réponse simulée
    response = f"🤖 Réponse de GPR : '{prompt[::-1]}'"  # Réponse inversée pour l'exemple
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)