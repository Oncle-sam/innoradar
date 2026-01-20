# frontend/app.py
import streamlit as st
import os
from pages_ui import home, results, details


def load_css():
    css_file = os.path.join("frontend", "styles.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback si le fichier est ailleurs
        st.warning("Fichier CSS introuvable.")

# Appliquer le CSS
load_css()


# Config de base
st.set_page_config(page_title="InnoRadar", layout="wide", page_icon="⚡")

# Injection du CSS (Pour le Header custom et le Sticky Button)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("frontend/styles.css")

# Gestion de la navigation (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False # Mettre à True pour tester la version connectée

# Header Custom (Apparaît sur toutes les pages)
st.markdown("""
<div class="custom-header">
    <div class="logo-container">
        <span class="logo-icon">⚡</span> <span class="logo-text">Innoradar</span>
    </div>
    <div class="auth-button">
        <a href="#" target="_self">Se connecter</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Routeur de pages
if st.session_state.page == 'home':
    home.render_page()
elif st.session_state.page == 'results':
    results.render_page()
elif st.session_state.page == 'details':
    details.render_page()

# Sticky Button (Partout)
st.markdown("""
<a href="#" class="sticky-button">Contacter un expert</a>
""", unsafe_allow_html=True)
