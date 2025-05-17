# Streeamlit-LLM
#créer environnement virtuel python pour le projet
cd streamlit_chat_gpr
python -m venv venv
source venv/bin/activate # Pour mac # ou venv\Scripts\activate sur Windows

#Installer les packages nécessaire au projet
pip install -r requirements.txt

#Démarer le projet
streamlit run app.py 

#Installer le model 
pip install streamlit openai

#Installer le package pour les variables d'environnement
pip install python-dotenv
