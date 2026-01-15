import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

class InnoMatcher:
    def __init__(self, db_manager):
        self.db = db_manager

    def generate_recommendation(self, user_need, context_step):
        """
        Analyse le besoin et compare avec la base de données.
        """
        # On extrait les 10 solutions les plus proches (version simplifiée pour le test)
        # Idéalement, on utiliserait un filtrage sémantique ici
        subset = self.db.df.head(10) 
        
        solutions_text = ""
        for i, row in subset.iterrows():
            solutions_text += f"- ID {i}: {row['Dénomination actuelle']} ({row['Résumé']})\n"

        prompt = f"""
        Tu es l'expert IA d'InnoRadar, plateforme de matchmaking Sport Tech.
        
        BESOIN DE L'UTILISATEUR :
        "{user_need}"
        
        CONTEXTE : {context_step}
        
        SOLUTIONS DISPONIBLES :
        {solutions_text}
        
        MISSION :
        Sélectionne les 3 solutions les plus pertinentes. 
        Pour chaque solution, donne :
        1. Le nom de la solution.
        2. Un score de match (0-100%).
        3. Un "Reasoning" (raisonnement) expliquant pourquoi elle répond précisément au besoin.
        
        Réponds au format JSON.
        """

        response = model.generate_content(prompt)
        return response.text