# 🚀 Streamlit-LLM

## 📋 Table des matières
- [Pré-requis](#pré-requis)
- [Installation](#installation)
- [Démarrage du projet](#démarrage-du-projet)
- [Tests et comparaison](#tests-et-comparaison)

## ✅ Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.11.0** (version recommandée)
- Un compte sur [https://console.groq.com](https://console.groq.com) pour obtenir une clé API GROQ

---

## 🛠️ Installation

### 1. Créer l'environnement virtuel Python
```bash
cd streamlit_chat_gpr
python -m venv venv
```

### 2. Activer l'environnement virtuel
```bash
# Sur macOS/Linux
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
pip install streamlit openai python-dotenv sentence-transformers
```

### 4. Configuration de l'API GORQ

Pour interagir avec les modèles d'OpenAI, vous devez configurer une clé API :

4.1. Obtenir une clé API
Rendez-vous sur https://console.groq.com/keys pour créer une clé si vous n’en avez pas.

4.2. Dans le répertoire streamlit_chat_gpr, éditez le fichier .env et remplacez la valeur de l'ancienne clé par la votre :
```python
GROQ_API_KEY= "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"
GROQ_API_URL="https://api.groq.com/openai/v1"
```

4.3. Vérifier que le fichier .env est bien chargé
Assurez-vous que le code charge la clé via python-dotenv comme ceci (dans app.py ou autre) :
```python
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
from db import init_db, save_message_to_db, load_conversation, list_conversations, delete_conversation_from_db


load_dotenv()
init_db()

client = OpenAI (
    api_key = os.getenv("GROQ_API_KEY"),
    base_url= os.getenv("GROQ_API_URL")
)
```

## 🚀 Démarrage du projet
```bash
streamlit run app.py
```

## 🧪 Tests et comparaison
Pour tester et comparer les modèles :
```bash
python comparaison_models.py
```

---
*Projet développé avec Streamlit et OpenAI*

---

##  collaborateurs

### ALAOUI EL MRANI YOUSSEF
### Jong Hoa CHONG
### Tom BRUAIRE
### Maylis GAILLARD
### Enolha DAIJARDIN
