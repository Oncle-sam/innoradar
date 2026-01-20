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

st.sidebar.header("Configuration du Radar")

# On récupère les catégories dynamiquement depuis le CSV
categories = ["Toutes"] + db.get_unique_categories()
selected_cat = st.sidebar.selectbox("Catégorie de produit/service", categories)

with st.form("match_form"):
    user_input = st.text_area("Quel est votre besoin métier ?")
    submitted = st.form_submit_button("Lancer le Radar")

if submitted and user_input:
    with st.spinner(f"Analyse de la catégorie {selected_cat}..."):
        # On passe la catégorie sélectionnée à l'IA
        recommendations = matcher.generate_recommendation(user_input, selected_cat)
        st.write(recommendations)
# Styles personnalisés pour le bouton et l'encadré AI Factory
st.markdown("""
    <style>
    .ai-factory-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ... après l'appel à matcher.generate_recommendation ...

if submitted and user_input:
    with st.spinner("Analyse du marché et conception de votre solution..."):
        recommendations = matcher.generate_recommendation(user_input, selected_cat)
        
        # Affichage des solutions du marché (simplifié ici pour l'exemple)
        st.markdown("### 📡 Top 2 Solutions du Marché")
        st.write(recommendations) # Ici, on pourrait parser le JSON pour un meilleur affichage

        # Mise en avant de l'AI Factory
        st.markdown('<div class="ai-factory-box">', unsafe_allow_html=True)
        st.subheader("🚀 Option 3 : InnoRadar AI Factory")
        st.info("**Slogan :** Créez votre propre Agent IA autonome : Architecture, Sécurité & Intégration sur-mesure.")
        
        st.markdown("""
        **Solution Overview :** Ne cherchez plus l'outil parfait, construisons-le. Une équipe d'élite dédiée à la conception d'agents IA combinant :
        1. Architecture IA (LLM, RAG, MCP)
        2. Intégration API fluides (CRM, Billetterie)
        3. Cybersécurité & RGPD
        4. Design d'expérience métier
        """)
        
        # Bouton de contact (peut être un lien mailto: ou un formulaire)
        contact_url = "mailto:samy@aklam.fr?subject=Demande InnoRadar AI Factory"
        st.link_button("🤝 Contacter l'équipe AI Factory", contact_url, type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
