import requests
import time
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import numpy as np

load_dotenv()

# Clé Api et Url
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("GROQ_API_URL")

# Modèles à comparer
MODELS = {
    "llama3" : "llama3-70b-8192",
    "gemma2" : "gemma2-9b-it"
}

# Questions d'évaluation
QUESTIONS = [
    "Peux-tu expliquer simplement le théorème de Pythagore ?",
    "Quelle est la différence entre ADN et ARN ?",
    "Comment résoudre une équation du second degré ?",
    "Qu'est-ce que la photosynthèse ?",
    "Explique-moi la seconde guerre mondiale ?"
]

REFERENCES = [
    "Le théorème de Pythagore affirme que dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.",
    "L'ADN est le support de l'information génétique dans les cellules, tandis que l'ARN sert principalement à transmettre cette information et à aider à la synthèse des protéines.",
    "Pour résoudre une équation du second degré, on utilise la formule quadratique : x = (-b ± √(b² - 4ac)) / (2a), où a, b et c sont les coefficients de l'équation.",
    "La photosynthèse est un processus par lequel les plantes utilisent la lumière du soleil pour convertir le dioxyde de carbone et l'eau en glucose et oxygène.",
    "La Seconde Guerre mondiale est un conflit mondial qui a eu lieu de 1939 à 1945, impliquant la majorité des nations du monde, opposant les Alliés aux puissances de l'Axe."
]

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Modèle d"'embeddings pour mesurer la similarité sémantique 
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def ask_model(model_id, question):
    """Interroge l'API Groq avec la question et modèle donné."""
    payload = {
        "models": model_id,
        "messages": [
            {"role": "system", "content": "Tu es assistant pédagogique clair et synthétique."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }
    start = time.time()
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    elapsed = time.time() - start
    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip(), elapsed
    else:
        return f"Erreur {response.status_code}", elapsed

def evaluate_similarity(reference, response):
    """Calcule la simularité cosine entre référence et réponse."""
    ref_emb = embed_model.encode(reference, convert_to_tensor=True)
    resp_emb = embed_model.encode(response, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(ref_emb, resp_emb).item()
    return similarity

def length_score(length, ideal=150, tolerance=50):
    """ Score simple pour la longueur : max 1 à 'ideal', 
        baisse linéaire en dehors de [ideal - tol, ideal + tol].
    """
    if length < ideal - tolerance:
        return max(0, length / (ideal - tolerance))
    elif length > ideal + tolerance:
        return max(0, 1 - (length - (ideal + tolerance)) / tolerance)
    else:
        return 1

def main():
    results = []

    print("Lancement des tests sur les modèles...\n")
    for i, question in enumerate(QUESTIONS):
        reference = REFERENCES[i]
        for model_name, model_id in MODELS.items():
            answer, duration = ask_model(model_id, question)
            word_count = len(answer.split())
            similarity = evaluate_similarity(reference, answer)
            l_score = length_score(word_count)
            results.append({
                "Question": question,
                "Modèle": model_name,
                "Durée (s)": duration,
                "Longueur (mots)": word_count,
                "Score longueur": l_score,
                "Similarité": similarity,
                "Réponse": answer.replace('\n', '')
            })
            print(f"[{model_name}] Question : '{question[:30]}...' -> Similarité: {similarity:.3f}, Durée: {duration:.2f}s, Longueur: {word_count}")
    
    # Analyse globale par modèle
    summary = {}
    for model_name in MODELS.keys():
        filered = [r for r in results if r["Modèle"] == model_name]
        avg_sim = np.mean([r["Similarité"] for r in filered])
        avg_dur = np.mean([r["Durée (s)"] for r in filered])
        avg_len = np.mean([r["Score longueur"] for r in filered])

        # Pondération personnalisée - modifie ici si besoin 
        score_global = avg_sim * 0.6 - avg_dur * 0.3 + avg_len * 0.1
        summary[model_name] = {
            "Similarité moyenne": avg_sim,
            "Durée moyenne (s)": avg_dur,
            "Score longueur moyen": avg_len,
            "Score global": score_global
    }

    print("\n=== Résumé final ===")
    for model, metrics in summary.items():
        print(f"\nModèle: {model}")
        for k, v in metrics.items():
            print(f" {k}: {v:.3f}")

    meilleur = max(summary.items(), key=lambda x: x[1]["Score global"])
    print(f"\n Meilleur modèle selon score global: {meilleur[0]} avec un score de {meilleur[1]['Score global']:.3f}")

if __name__ == "__main__":
    main()