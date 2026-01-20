import streamlit as st

def render_page():
    # Gestion des étapes du formulaire
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1

    st.markdown("<h1 style='text-align: center;'>Lancer le radar</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Trouvez la solution réellement adaptée à votre besoin.</h3>", unsafe_allow_html=True)

    # --- ÉTAPE 1 : PROFIL ---
    if st.session_state.wizard_step == 1:
        st.subheader("1. Votre profil")
        st.info("Sélectionnez le profil correspondant le mieux à votre organisation.")
        profils = ["Club professionnel", "Club amateur", "Fédération", "Entreprise", "Média"] # Liste complète à mettre
        
        # On utilise des colonnes pour faire des "Tuiles" ou une simple multiselect
        choix = st.selectbox("Je suis :", profils)
        
        if st.button("Suivant"):
            st.session_state.user_profile = choix
            st.session_state.wizard_step = 2
            st.rerun()

    # --- ÉTAPE 2 : BESOIN ---
    elif st.session_state.wizard_step == 2:
        st.subheader("2. Votre besoin")
        st.info("Décrivez votre besoin, vos freins opérationnels ou défis actuels.")
        user_need = st.text_area("Ex: Je veux améliorer la fan experience...", height=150)
        
        col1, col2 = st.columns([1, 1])
        if col1.button("Retour"):
            st.session_state.wizard_step = 1
            st.rerun()
        if col2.button("Suivant"):
            if user_need:
                st.session_state.user_need = user_need
                st.session_state.wizard_step = 3
                st.rerun()
            else:
                st.error("Veuillez décrire votre besoin.")

    # --- ÉTAPE 3 : OBJECTIF ---
    elif st.session_state.wizard_step == 3:
        st.subheader("3. Votre objectif")
        st.info("Définissez vos objectifs et résultats attendus.")
        user_goal = st.text_area("Ex: Augmenter mes revenus de billetterie de 10%", height=100)
        
        col1, col2 = st.columns([1, 1])
        if col1.button("Retour"):
            st.session_state.wizard_step = 2
            st.rerun()
        if col2.button("Lancer le Radar 🚀", type="primary"):
            st.session_state.user_goal = user_goal
            st.session_state.page = 'results' # On change de page !
            st.rerun()

    # --- BLOC "INNOVATIONS À LA UNE" ---
    st.markdown("---")
    st.subheader("Les innovations à la une")
    # Ici, code pour afficher les 3 cartes statiques
