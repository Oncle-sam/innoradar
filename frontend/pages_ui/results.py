import streamlit as st

def render_card(solution, match_score, is_ai_factory=False):
    # CSS pour faire une belle carte
    border_color = "#ff4b4b" if is_ai_factory else "#ddd"
    
    st.markdown(f"""
    <div style="border: 1px solid {border_color}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between;">
            <h4>{solution['name']}</h4>
            <span style="color: green; font-weight: bold;">{match_score}% Match</span>
        </div>
        <p style="font-size: 12px; color: grey;">{solution['location']}</p>
        <p>{solution['summary']}</p>
        <hr>
        <div style="text-align: right;">
            <button>Plus d'informations</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Note : Le bouton HTML ci-dessus est visuel, en Streamlit on utilisera st.button avec une clé unique

def render_page():
    st.title("Résultats du Radar")
    
    # --- LOGIQUE FILTRES ---
    if not st.session_state.authenticated:
        st.info("🔒 Mode Freemium : Les filtres avancés sont verrouillés.")
        if st.button("Débloquer les filtres"):
            # Rediriger vers login
            pass
    else:
        st.sidebar.header("Filtres Pro Avancés")
        st.sidebar.multiselect("Catégories", ["Athletes & perf", "Ticketing", "Fan Exp"])
        # ... autres filtres

    # --- LISTING DES SOLUTIONS ---
    # Récupération des résultats IA (Code fictif pour l'exemple)
    results = get_ai_results() # Renvoie une liste de dictionnaires
    
    # On itère sur les résultats
    for index, solution in enumerate(results):
        
        # INJECTION FORCEE DE L'AI FACTORY EN POSITION 4 (Index 3)
        if index == 3:
            ai_factory_data = {
                "name": "InnoRadar AI Factory",
                "summary": "Créez votre propre Agent IA autonome. Architecture sur-mesure.",
                "location": "Paris, France (Remote)",
            }
            render_card(ai_factory_data, 100, is_ai_factory=True)
        
        # Affichage normal
        render_card(solution, solution['score'])
        
        # En Freemium, on bloque la pagination
        if not st.session_state.authenticated and index >= 5:
            st.warning("🔒 Connectez-vous pour voir les 900+ autres solutions.")
            break
