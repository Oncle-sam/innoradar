import streamlit as st

def render_home(db):
    # --- CSS spécifique pour centrer le titre du Wizard ---
    st.markdown("""
        <style>
        .wizard-container { max-width: 700px; margin: 0 auto; }
        .step-indicator { color: #4B79FF; font-weight: 700; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; margin-bottom: 5px; }
        </style>
    """, unsafe_allow_html=True)

    # --- Header de la page ---
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>📡 Lancer le radar</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a0a2b3; font-weight: 400; margin-top: 10px; font-size: 18px;'>Trouvez la solution réellement adaptée à votre besoin.</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Initialisation de l'étape du wizard
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1

    # Container central pour le formulaire
    col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])
    
    with col_main:
        # --- ÉTAPE 1 : VOTRE PROFIL ---
        if st.session_state.wizard_step == 1:
            st.markdown('<div class="step-indicator">Étape 1/3</div>', unsafe_allow_html=True)
            st.subheader("Votre profil")
            st.info("Sélectionnez le profil correspondant le mieux à votre organisation.")
            
            profils = [
                "Club professionnel", "Club amateur / Association", "Ligue / Comité", 
                "Fédération", "Organisateur événement / compétition", "Sponsor / Mécène", 
                "Média", "Ayant Droit", "Fournisseur biens / services", 
                "Entreprise", "Fan / Supporter", "Sportif amateur", 
                "Staff technique", "Sportif professionnel"
            ]
            
            # On vérifie si une sélection existe déjà
            current_index = 0
            if 'user_profile' in st.session_state and st.session_state.user_profile in profils:
                current_index = profils.index(st.session_state.user_profile)

            choix_profil = st.selectbox("Je représente :", profils, index=current_index, label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Suivant ➝", type="primary", use_container_width=True):
                st.session_state.user_profile = choix_profil
                st.session_state.wizard_step = 2
                st.rerun()

        # --- ÉTAPE 2 : VOTRE BESOIN ---
        elif st.session_state.wizard_step == 2:
            st.markdown('<div class="step-indicator">Étape 2/3</div>', unsafe_allow_html=True)
            st.subheader("Votre besoin")
            st.info("Décrivez votre besoin, vos freins opérationnels ou défis actuels.")
            
            default_need = st.session_state.get('user_need', '')
            user_need = st.text_area("Besoin :", value=default_need, height=150, placeholder="Ex: Je cherche à digitaliser la billetterie pour améliorer l'expérience fan et collecter plus de data...", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_back, col_next = st.columns([1, 2])
            with col_back:
                if st.button("← Retour", use_container_width=True):
                    st.session_state.wizard_step = 1
                    st.rerun()
            with col_next:
                if st.button("Suivant ➝", type="primary", use_container_width=True):
                    if user_need.strip():
                        st.session_state.user_need = user_need
                        st.session_state.wizard_step = 3
                        st.rerun()
                    else:
                        st.error("Veuillez décrire votre besoin pour continuer.")

        # --- ÉTAPE 3 : VOTRE OBJECTIF ---
        elif st.session_state.wizard_step == 3:
            st.markdown('<div class="step-indicator">Étape 3/3</div>', unsafe_allow_html=True)
            st.subheader("Votre objectif")
            st.info("Définissez vos objectifs et résultats attendus.")
            
            default_goal = st.session_state.get('user_goal', '')
            user_goal = st.text_area("Objectif :", value=default_goal, height=100, placeholder="Ex: Augmenter de 15% les revenus 'jour de match'...", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_back, col_launch = st.columns([1, 2])
            with col_back:
                if st.button("← Retour", use_container_width=True):
                    st.session_state.wizard_step = 2
                    st.rerun()
            with col_launch:
                if st.button("Lancer le radar 🚀", type="primary", use_container_width=True):
                    st.session_state.user_goal = user_goal
                    # Construction de la requête complète pour l'IA
                    full_query = f"Profil: {st.session_state.user_profile}. Besoin: {st.session_state.user_need}. Objectif: {user_goal}"
                    st.session_state.current_query = full_query
                    
                    # Transition vers la page de résultats
                    st.session_state.page = 'results'
                    st.rerun()

    # --- Footer Bloc : Crédibilité ---
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #555; font-size: 14px;'>
            <p>🔒 Vos données sont sécurisées • Analyse propulsée par Gemini Pro</p>
        </div>
    """, unsafe_allow_html=True)
