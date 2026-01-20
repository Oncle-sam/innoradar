import streamlit as st
import os
import sys

# Ajout du chemin pour importer backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database_manager import DatabaseManager
from backend.ai_engine import InnoMatcher

# Configuration de la page
st.set_page_config(page_title="InnoRadar", page_icon="⚡", layout="wide")

# Chargement du CSS
css_file = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialisation du moteur et de la session
@st.cache_resource
def get_core():
    db = DatabaseManager("data/solutions.csv")
    matcher = InnoMatcher(db)
    return db, matcher

db, matcher = get_core()

# Initialisation des variables de navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_solution' not in st.session_state:
    st.session_state.selected_solution = None

# --- HEADER CUSTOM ---
st.markdown(f"""
<div class="custom-header">
    <div style="display:flex; align-items:center; gap:10px;">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">InnoRadar</span>
    </div>
    <button class="auth-btn-header">SE CONNECTER</button>
</div>
""", unsafe_allow_html=True)

# --- ROUTAGE DES PAGES ---
if st.session_state.page == 'home':
    from pages_ui.home import render_home
    render_home(db)

elif st.session_state.page == 'results':
    from pages_ui.results import render_results
    render_results(matcher)

elif st.session_state.page == 'details':
    from pages_ui.details import render_details
    render_details(st.session_state.selected_solution)

# --- CHATBOT FLOTTANT (Bas Gauche) ---
with st.popover("💬"):
    st.markdown("### 🤖 Assistant InnoRadar")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Une question ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = matcher.ask_chatbot(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- CONTACT EXPERT (Bas Droite) ---
st.markdown("""
    <div style="position:fixed; bottom:20px; right:20px; z-index:9999;">
        <a href="mailto:samy@aklam.fr" class="cta-btn-purple" style="text-decoration:none;">
            🤝 Parler à un expert
        </a>
    </div>
""", unsafe_allow_html=True)
