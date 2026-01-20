import streamlit as st
import os
import sys

# Ajout du chemin pour importer backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database_manager import DatabaseManager
from backend.ai_engine import InnoMatcher
from pages_ui.home import render_home

# Configuration de la page
st.set_page_config(page_title="InnoRadar", page_icon="⚡", layout="wide")

# Chargement du CSS (Nouveau Design)
css_file = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialisation
@st.cache_resource
def get_core():
    db = DatabaseManager("data/solutions.csv") # Chemin ajusté selon votre Dockerfile
    # Si le chargement échoue, créer un DB manager vide pour ne pas crasher
    if db.df is None:
        st.error("Erreur de chargement de la base de données.")
    matcher = InnoMatcher(db)
    return db, matcher

db, matcher = get_core()

# Gestion de la navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HEADER CUSTOM ---
st.markdown("""
<div class="custom-header">
    <div style="display:flex; align-items:center; gap:10px;">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">InnoRadar</span>
    </div>
    <button class="auth-btn-header">SE CONNECTER</button>
</div>
""", unsafe_allow_html=True)

# --- ROUTAGE ---
# On importe les pages dynamiquement pour éviter les dépendances circulaires
if st.session_state.page == 'home':
    # Note: Assurez-vous d'avoir créé le fichier frontend/pages_ui/home.py
    from pages_ui.home import render_home
    render_home(db)

elif st.session_state.page == 'results':
    # Note: Assurez-vous d'avoir créé le fichier frontend/pages_ui/results.py
    from pages_ui.results import render_results
    render_results(matcher)

# --- CHATBOT & CONTACT (Global) ---
with st.sidebar:
    # Code du chatbot ici (ou popover flottant)
    pass 

# Sticky Contact Button
st.markdown("""
    <div style="position:fixed; bottom:20px; right:20px; z-index:9999;">
        <a href="mailto:samy@aklam.fr" class="cta-btn-purple" style="text-decoration:none;">
            💬 Parler à un expert
        </a>
    </div>
""", unsafe_allow_html=True)
