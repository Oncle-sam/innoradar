import streamlit as st
import json
import re

# --- MOTEUR DE RENDU HTML (Design Image 0) ---
def render_complex_card_html(data, is_ai_factory=False):
    """
    Génère le HTML d'une carte résultat avec le design Dark Mode avancé.
    """
    
    # 1. Configuration des données (AI Factory vs Solution Standard)
    if is_ai_factory:
        # Données statiques pour l'AI Factory (Conforme à votre demande)
        badges_html = """
            <span class="badge-dark badge-purple">À LA UNE</span>
            <span class="badge-dark badge-outline">CUSTOM DEVELOPMENT</span>
        """
        title = "InnoRadar AI Factory"
        verified = True
        location = "Paris, France"
        employees = "51-100 employés"
        # Le slogan en italique
        slogan = "Créez votre propre Agent IA autonome : Architecture, Sécurité & Intégration sur-mesure."
        # Le texte principal
        overview = """
        Ne cherchez plus l'outil parfait, construisons-le. Une équipe d'élite dédiée à la conception d'agents IA combinant : 
        <ul style="margin-top:5px; padding-left:20px; color:#a0a2b3;">
            <li>Architecture IA (LLM, RAG, MCP)</li>
            <li>Intégration API fluides (CRM, Billetterie)</li>
            <li>Cybersécurité & RGPD</li>
            <li>Design d'expérience métier</li>
        </ul>
        """
        trust_score = 100
        active_since = "2023"
        presence_level = "High"
        presence_color = "#4ade80" # Vert
        cta_text = "Demander une Analyse"
        cta_icon = "🟣"
        logo_initials = "IN"
        logo_bg = "linear-gradient(135deg, #4B79FF, #7F56D9)"
    
    else:
        # Données dynamiques venant du CSV/IA
        cat = data.get("category", "Innovation")
        badges_html = f'<span class="badge-dark">{cat}</span>'
        title = data.get("name", "Solution sans nom")
        verified = data.get("verified", False)
        location = data.get("location", "Non renseigné")
        employees = data.get("employees", "N/A")
        
        raw_summary = data.get("summary", "Pas de description disponible.")
        # On coupe le slogan pour l'affichage
        slogan = raw_summary[:80] + "..." if len(raw_summary) > 80 else raw_summary
        overview = raw_summary
        
        trust_score = data.get("match_score", 80)
        active_since = data.get("creation_year", "N/A")
        presence_level = "Medium"
        presence_color = "#Facc15" # Jaune
        cta_text = "Voir la fiche"
        cta_icon = "👁️"
        # Initiales pour le logo placeholder
        logo_initials = title[:2].upper() if title else "??"
        logo_bg = "#252941" # Gris bleuté par défaut

    # Icône de vérification
    verified_html = '<span class="verified-icon" title="Vérifié par InnoRadar">✔</span>' if verified else ''
    
    # --- CONSTRUCTION DU HTML ---
    html = f"""
    <div class="dark-result-card">
        <div class="card-header-flex">
            <div class="card-logo-placeholder" style="background: {logo_bg};">
                {logo_initials}
            </div>
            
            <div class="card-info-col">
                <div class="badges-row">{badges_html}</div>
                
                <div class="card-title-row">
                    <h2>{title} {verified_html}</h2>
                </div>
                
                <div class="card-meta-row">
                    <span class="meta-item"><span style="opacity:0.7">📍</span> {location}</span>
                    <span class="meta-item"><span style="opacity:0.7">👥</span> {employees}</span>
                </div>
                
                <div class="card-links-row">
                    <span>🇬🇧 🇫🇷</span> <a href="#" class="visit-link">VISITER LE SITE ↗</a>
                </div>
            </div>
            
            <div class="card-actions-col">
                <button class="fav-btn">♡</button>
                <button class="cta-btn-purple">{cta_text}</button>
            </div>
        </div>

        <div style="border-left: 3px solid #7F56D9; padding-left: 15px; margin-bottom: 25px;">
            <p style="font-size: 18px; font-style: italic; color: #e0e0e0; margin: 0;">
                "{slogan}"
            </p>
        </div>

        <div class="content-layout-grid">
            
            <div class="main-text-col">
                <div class="section-title"><span class="purple-dot"></span> Solution Overview</div>
                <div class="overview-text">{overview}</div>
            </div>
            
            <div class="trust-sidebar-box">
                <div class="trust-header">
                    <span class="trust-title">TRUST & VIABILITY</span>
                    <span class="trust-score-big" style="color:{presence_color}">{trust_score}/100</span>
                </div>
                
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {trust_score}%; background-color: {presence_color};"></div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <div style="background:#252941; padding: 8px; border-radius: 6px; flex:1; text-align:center;">
                        <div style="font-size:10px; color:#a0a2b3; text-transform:uppercase;">Active Since</div>
                        <div style="font-weight:600; font-size:14px;">{active_since}</div>
                    </div>
                    <div style="background:#252941; padding: 8px; border-radius: 6px; flex:1; text-align:center;">
                         <div style="font-size:10px; color:#a0a2b3; text-transform:uppercase;">Presence</div>
                        <div style="font-weight:600; font-size:14px; color:{presence_color};">{presence_level}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html


# --- PAGE RENDERER ---
def render_results(matcher):
    # Bouton de retour
    if st.button("← Retour à la recherche", key="back_btn"):
        st.session_state.page = 'home'
        st.rerun()

    st.title("Résultats du Radar")
    
    # Récupération de la requête
    query = st.session_state.get("current_query", "")
    user_need = st.session_state.get("user_need", "")
    
    if not query:
        st.warning("Aucune donnée de recherche. Veuillez repasser par l'accueil.")
        return

    # --- MATCHMAKING (Simulation intelligente ou Appel API) ---
    # Pour l'instant, on utilise des données simulées pour garantir le rendu visuel
    # Dans la version finale, on parsera le JSON renvoyé par matcher.generate_recommendation(user_need, "Toutes")
    
    # 1. On affiche la requête analysée
    st.info(f"🔍 Analyse pour : {user_need[:100]}...")

    # 2. Données Mockées (En attendant que l'IA soit parfaitement calibrée en JSON)
    # Ceci garantit que vous voyez le design immédiatement
    solutions_market = [
        {
            "name": "FanEngage Pro",
            "category": "Fan Experience",
            "location": "Londres, UK",
            "employees": "11-50 employés",
            "verified": True,
            "match_score": 92,
            "summary": "Plateforme SaaS leader pour la gamification des fans en jour de match. Augmentez l'engagement via des quiz live et des récompenses blockchain.",
            "creation_year": "2019"
        },
        {
            "name": "Stadium Analytics",
            "category": "Data & Performance",
            "location": "Berlin, Allemagne",
            "employees": "51-200 employés",
            "verified": False,
            "match_score": 85,
            "summary": "Solution IoT pour tracker les flux de spectateurs en temps réel et optimiser les revenus des buvettes.",
            "creation_year": "2021"
        }
    ]

    # --- RENDU DES CARTES ---
    
    # 1. Les Solutions du Marché (Top 2)
    st.markdown("### 📡 Top 2 Solutions du Marché")
    for sol in solutions_market:
        st.markdown(render_complex_card_html(sol, is_ai_factory=False), unsafe_allow_html=True)

    # 2. L'Injection InnoRadar AI Factory (Toujours en dernier)
    st.markdown("### 🚀 Solution Recommandée sur-mesure")
    st.markdown(render_complex_card_html(None, is_ai_factory=True), unsafe_allow_html=True)
