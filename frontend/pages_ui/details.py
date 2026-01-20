import streamlit as st

def render_page():
    if st.button("← Retour aux résultats"):
        st.session_state.page = 'results'
        st.rerun()

    # Layout en colonnes pour le Header de la fiche
    col_img, col_info = st.columns([1, 3])
    
    with col_info:
        st.title("Nom de la Solution")
        st.markdown("📍 France | 👥 10-50 employés")
        
        # Bouton Rapport Détaillé
        if st.button("📄 Demander un rapport détaillé"):
            if not st.session_state.authenticated:
                st.error("🔒 Cette fonctionnalité est réservée aux membres connectés.")
            else:
                render_report_popup()

@st.dialog("Configurer votre rapport")
def render_report_popup():
    st.write("Sélectionnez les éléments à inclure :")
    st.checkbox("Structure de Prix")
    st.checkbox("Comparatif Concurrents")
    st.checkbox("Roadmap Déploiement")
    if st.button("Envoyer la demande"):
        st.success("Votre demande a été transmise à l'expert !")
