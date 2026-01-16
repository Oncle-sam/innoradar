import streamlit as st
import sys
import os

# Ajout du chemin pour importer nos modules backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database_manager import DatabaseManager
from backend.ai_engine import InnoMatcher

st.set_page_config(page_title="InnoRadar - Sport Tech Matchmaker", page_icon="📡")

st.title("📡 InnoRadar")
st.subheader("Le radar d'innovation du sport")

# Initialisation des composants
db = DatabaseManager("data/solutions.csv")
matcher = InnoMatcher(db)

# Formulaire de besoin
with st.form("match_form"):
    user_input = st.text_area("Quel est votre besoin métier ? (ex: Améliorer l'expérience spectateur)")
    submitted = st.form_submit_button("Lancer le Radar")

if submitted and user_input:
    with st.spinner("L'IA analyse 900+ solutions..."):
        recommendations = matcher.generate_recommendation(user_input, "Cadrage initial")
        st.write("### Recommandations de l'IA")
        st.write(recommendations)