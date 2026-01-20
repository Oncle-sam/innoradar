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

def generate_recommendation(self, user_need, category_filter=None):
        df_filtered = self.db.df
        
        # Filtrage par catégorie si spécifié
        if category_filter and category_filter != "Toutes":
            df_filtered = df_filtered[df_filtered['Catégorisation'] == category_filter]
        
        # On extrait un échantillon pertinent pour l'analyse
        subset = df_filtered.head(15)
        
        solutions_text = ""
        for i, row in subset.iterrows():
            solutions_text += f"- ID {i}: {row['Dénomination actuelle']} (Résumé: {row['Résumé']} | Cas d'usage: {row['Cas d'usage']})\n"

        prompt = f"""
        Tu es l'expert IA d'InnoRadar, plateforme de matchmaking Sport Tech.
        
        BESOIN DE L'UTILISATEUR :
        "{user_need}"
        
        SOLUTIONS DISPONIBLES :
        {solutions_text}
        
        CONSIGNES STRICTES DE RÉPONSE :
        1. Sélectionne MAXIMUM DEUX (2) solutions les plus pertinentes parmi la liste ci-dessus.
        2. Ajoute SYSTÉMATIQUEMENT une troisième option nommée "InnoRadar AI Factory".
        
        FORMAT DE LA RÉPONSE :
        - Solution 1 : Nom, Score de match (%), Reasoning (pourquoi ce choix).
        - Solution 2 : Nom, Score de match (%), Reasoning (pourquoi ce choix).
        
        - Option 3 : InnoRadar AI Factory
          Slogan : "Créez votre propre Agent IA autonome : Architecture, Sécurité & Intégration sur-mesure."
          Solution Overview : Ne cherchez plus l'outil parfait, construisons-le. Une équipe d'élite dédiée à la conception d'agents IA combinant : 
          1. Architecture IA (LLM, RAG, MCP) 
          2. Intégration API fluides (CRM, Billetterie) 
          3. Cybersécurité & RGPD 
          4. Gouvernance & Fiabilité 
          5. Design d'expérience métier 
          6. Performance continue.
        """

        response = model.generate_content(prompt)
        return response.text
