import streamlit as st
import os
import sys

# Import des modules backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database_manager import DatabaseManager
from backend.ai_engine import InnoMatcher

# Configuration
st.set_page_config(page_title="InnoRadar", page_icon="⚡", layout="wide")

# Initialisation DB et IA (en cache pour la performance)
@st.cache_resource
def init_core():
    db = DatabaseManager("data/solutions.csv")
    matcher = InnoMatcher(db)
    return db, matcher

db, matcher = init_core()

# Chargement du CSS
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HEADER (Commun) ---
col_logo, col_auth = st.columns([1, 1])
with col_logo:
    st.markdown("### ⚡ Innoradar")
with col_auth:
    if st.button("Se connecter", key="auth_btn"):
        st.session_state.authenticated = True

# --- ROUTAGE DES PAGES ---
if st.session_state.page == 'home':
    # Import local pour éviter les imports circulaires
    from pages_ui.home import render_home
    render_home(db)
elif st.session_state.page == 'results':
    from pages_ui.results import render_results
    render_results(matcher)

# --- CHATBOT FLOTTANT (Bas Gauche) ---
with st.popover("🤖"):
    st.markdown("### Assistant InnoRadar")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Une question sur la Sport Tech ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = matcher.ask_chatbot(prompt) # Nouvelle méthode dans InnoMatcher
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- BOUTON CONTACT (Bas Droite) ---
st.markdown(f"""
    <div class="sticky-contact">
        <a href="mailto:samy@aklam.fr?subject=Contact InnoRadar" style="text-decoration:none;">
            <button style="background:#1a1a1a; color:white; border-radius:50px; padding:12px 24px; border:none; cursor:pointer;">
                🤝 Contacter un expert
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
