import streamlit as st
import json

def render_complex_card_html(data, is_ai_factory=False):
    """Génère le HTML d'une carte. Retourne une seule chaîne propre."""
    
    if is_ai_factory:
        title = "InnoRadar AI Factory"
        badges = '<span class="badge-dark badge-purple">À LA UNE</span>'
        location = "Paris, France"
        slogan = "Créez votre propre Agent IA autonome."
        overview = "Architecture IA, Intégrations API & Sécurité sur-mesure."
        trust_score = 100
        logo_bg = "linear-gradient(135deg, #4B79FF, #7F56D9)"
        cta_text = "Demander une Analyse"
        logo_in = "IN"
    else:
        title = data.get("name", "Solution")
        badges = f'<span class="badge-dark">{data.get("category", "Innovation")}</span>'
        location = data.get("location", "Global")
        slogan = data.get("summary", "")[:60] + "..."
        overview = data.get("summary", "")
        trust_score = data.get("match_score", 85)
        logo_bg = "#252941"
        cta_text = "Détails"
        logo_in = title[:2].upper()

    # On construit la carte dans une div unique
    return f"""
    <div class="dark-result-card-vertical">
        <div class="card-logo-placeholder-small" style="background: {logo_bg};">
            {logo_in}
        </div>
        <div class="badges-row" style="justify-content:center; margin-bottom:10px;">{badges}</div>
        <h3 class="card-title-small" style="text-align:center;">{title}</h3>
        <p class="card-meta-small" style="text-align:center;">📍 {location}</p>
        <hr style="border-color: #2a2e45; margin: 15px 0;">
        <p class="slogan-small" style="text-align:center;">"{slogan}"</p>
        
        <div class="trust-section-small" style="margin-top:auto;">
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;">
                <span style="color:#a0a2b3;">MATCH SCORE</span>
                <span style="color:#4ade80; font-weight:bold;">{trust_score}%</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{trust_score}%; background:#4ade80;"></div>
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <button class="cta-btn-purple-small">{cta_text}</button>
        </div>
    </div>
    """

def render_results(matcher):
    # En-tête avec bouton retour
    col_nav, col_empty = st.columns([1, 4])
    with col_nav:
        if st.button("← Retour", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<h2 style='text-align:center;'>Résultats du Radar</h2>", unsafe_allow_html=True)
    
    user_need = st.session_state.get("user_need", "")
    selected_cat = st.session_state.get("selected_cat", "Toutes")

    with st.spinner("L'IA affine la sélection..."):
        # 1. Appel au moteur IA (qui doit renvoyer du JSON)
        raw_response = matcher.generate_recommendation(user_need, selected_cat)
        
        try:
            # On nettoie et parse le JSON
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
            solutions_market = json.loads(clean_json)
        except:
            # Fallback si l'IA ne répond pas en JSON valide
            solutions_market = [
                {"name": "Solution 1", "category": "Analyse", "match_score": 90, "summary": "Analyse en cours..."},
                {"name": "Solution 2", "category": "Data", "match_score": 85, "summary": "Chargement des données..."}
            ]

    # --- AFFICHAGE CÔTE À CÔTE (3 Colonnes) ---
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        if len(solutions_market) > 0:
            st.markdown(render_complex_card_html(solutions_market[0]), unsafe_allow_html=True)
    
    with col2:
        if len(solutions_market) > 1:
            st.markdown(render_complex_card_html(solutions_market[1]), unsafe_allow_html=True)
        
    with col3:
        # Toujours l'AI Factory en 3ème position
        st.markdown(render_complex_card_html(None, is_ai_factory=True), unsafe_allow_html=True)
