import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration de Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None




class InnoMatcher:
    def __init__(self, db_manager):
        self.db = db_manager

    def generate_recommendation(self, user_need, category_filter=None):
        if not model:
            return "Erreur : Clé API manquante."

        df_filtered = self.db.df
        if category_filter and category_filter not in ["Toutes", "Cadrage initial"]:
            if 'Catégorisation' in df_filtered.columns:
                df_filtered = df_filtered[df_filtered['Catégorisation'] == category_filter]
        
        subset = df_filtered.head(20)
        
        solutions_text = ""
        for i, row in subset.iterrows():
            # Utilisation de doubles guillemets pour éviter le bug sur "Cas d'usage"
            nom = row.get('Dénomination actuelle', 'Solution')
            usage = row.get("Cas d'usage", 'N/A') 
            solutions_text += f"- ID {i}: {nom} (Usage: {usage})\n"

        prompt = f"""
        Sélectionne EXACTEMENT les 2 meilleures solutions pour ce besoin : {user_need}.
        Réponds UNIQUEMENT en JSON :
        [
          {{"name": "Nom", "summary": "Explication", "match_score": 95, "location": "Pays", "verified": true}},
          {{"name": "Nom", "summary": "Explication", "match_score": 85, "location": "Pays", "verified": false}}
        ]
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        # Nettoyage pour garantir un JSON valide
        return response.text.replace("```json", "").replace("```", "").strip()




    def ask_chatbot(self, question):
        if not model: return "IA non configurée."
        prompt = f"Tu es l'assistant InnoRadar. Réponds brièvement à : {question}"
        response = model.generate_content(prompt)
        return response.text

    
