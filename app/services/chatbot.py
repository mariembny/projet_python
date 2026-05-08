import os
from google import genai
from google.genai import types
from app.models.book import get_library_context

# Lire la clé API depuis variable d'environnement
# fallback si non définie
os.environ.setdefault("GEMINI_API_KEY", "AIzaSyB8nPOIwDikQBQQjjJpOkBe9z-Fcew79s4")

SYSTEM_PROMPT = """
Tu es un assistant intelligent de bibliothèque nommé "BiblioBot".
Tu aides les utilisateurs à trouver des informations sur les livres dans la bibliothèque.

Règles importantes :
1. Réponds TOUJOURS en français.
2. Utilise UNIQUEMENT les données du catalogue fourni pour répondre aux questions sur les livres.
3. Si un livre n'est pas dans le catalogue, dis-le clairement.
4. Sois chaleureux, professionnel et précis.
5. Pour les recommandations, base-toi sur les catégories, auteurs et disponibilités réels.
6. Formate tes réponses de façon claire avec des emojis appropriés.
7. Pour les livres empruntés, mentionne la date de retour si disponible.
"""


def get_chatbot_response(user_message: str, history: list = None) -> str:
    """
    Génère réponse chatbot Gemini avec historique conversation.

    history format:
    [
        {"role": "user", "parts": ["bonjour"]},
        {"role": "model", "parts": ["salut"]}
    ]
    """

    api_key = os.environ.get("GEMINI_API_KEY", "")

    if not api_key:
        return "❌ Clé API Gemini manquante."

    if history is None:
        history = []

    try:
        client = genai.Client(api_key=api_key)

        # Charger contexte bibliothèque depuis BD
        library_context = get_library_context()

        # Construire contexte dynamique
        context_prefix = f"""
Le catalogue actuel de la bibliothèque :

{library_context}

Question de l'utilisateur :
"""

        # Convertir historique au format Gemini SDK
        chat_history = []

        for entry in history:
            role = entry["role"]
            text = entry["parts"][0] if entry["parts"] else ""

            chat_history.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=text)]
                )
            )

        # Créer chat session
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
            history=chat_history
        )

        # Envoyer message
        response = chat.send_message(
            context_prefix + user_message
        )

        return response.text

    except Exception as e:
        error_str = str(e)

        if "API_KEY_INVALID" in error_str or "API key" in error_str:
            return "❌ Clé API invalide. Vérifiez GEMINI_API_KEY."

        if "quota" in error_str.lower() or "429" in error_str:
            return "❌ Quota API dépassé ou indisponible dans votre région."

        if "404" in error_str or "not found" in error_str.lower():
            return "❌ Modèle Gemini introuvable."

        return f"❌ Erreur chatbot : {error_str}"