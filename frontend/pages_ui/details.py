import streamlit as st



def render_report_popup():
    st.write("Sélectionnez les éléments à inclure :")
    st.checkbox("Structure de Prix")
    st.checkbox("Comparatif Concurrents")
    st.checkbox("Roadmap Déploiement")
    if st.button("Envoyer la demande"):
        st.success("Votre demande a été transmise à l'expert !")


def render_details(sol):
    if sol is None:
        st.session_state.page = 'home'
        st.rerun()

    # --- BLOC 1 : RETOUR (ID Unique ajouté) ---
    if st.button("← Retour", key="details_back_home"):
        st.session_state.page = 'home'
        st.rerun()

    # --- BLOC 2 : ESSENTIELS ---
    col_logo, col_info, col_actions = st.columns([1, 3, 2])
    
    with col_logo:
        st.markdown(f'<div class="card-logo-placeholder" style="width:120px; height:120px; font-size:40px; background:#252941; display:flex; align-items:center; justify-content:center; border-radius:12px;">{sol["Dénomination actuelle"][:2]}</div>', unsafe_allow_html=True)
    
    with col_info:
        st.markdown(f"""
            <span class="badge-dark badge-purple">À LA UNE</span>
            <h1 style="margin:10px 0;">{sol['Dénomination actuelle']} <span style="color:#4B79FF;">✔</span></h1>
            <p style="color:#a0a2b3;">📍 {sol.get('Siège social', 'N/A')} | 👥 {sol.get('Nombre de salariés', 'N/A')}</p>
        """, unsafe_allow_html=True)

    with col_actions:
        # Ajout de clés uniques pour les boutons d'action
        if st.button("❤️ Favoris", key=f"fav_{sol['Dénomination actuelle']}", use_container_width=True):
            st.toast("Ajouté aux favoris !")
        if st.button("📄 Rapport détaillé", key=f"report_{sol['Dénomination actuelle']}", use_container_width=True, type="primary"):
            st.toast("Demande envoyée !")

    # --- BLOC 3 : HEADLINE & DESCRIPTION ---
    st.markdown("---")
    st.markdown(f"### *\"{sol.get('Résumé', '')[:150]}...\"*")
    st.write(sol.get('Résumé', 'Description complète non disponible.'))
    
    # --- BLOC 4 : BUSINESS & POSITIONNEMENT ---
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Informations Business")
        st.markdown(f"**Modèle Économique :** {sol.get('Modèle économique', 'SaaS / Licence')}")
        st.markdown(f"**Appartenance :** {sol.get('Groupe / Indépendant', 'Indépendant')}")
    with c2:
        st.subheader("🎯 Positionnement")
        st.markdown(f"**Sports cibles :** {sol.get('Sport ciblé', 'Tous sports')}")
        st.markdown(f"**Clients cibles :** {sol.get('Cibles / Utilisateurs finaux', 'B2B / Clubs')}")

    # --- BLOC 5 : CONFIANCE (TRUST SCORE) ---
    st.markdown("---")
    st.subheader("🛡️ Confiance")
    ts_col1, ts_col2 = st.columns([1, 2])
    with ts_col1:
        st.markdown(f'<h2 style="color:#4ade80;">95/100</h2>', unsafe_allow_html=True)
    with ts_col2:
        st.markdown("""
            - **Années d'activité :** Présence établie
            - **Marché Français :** Récence et réputation validées
            - **Certifications :** Reconnu SportTech France
        """)

    # --- BLOC 6 : PARTENAIRES & AWARDS ---
    st.markdown("---")
    st.subheader("🏆 Références")
    st.write(f"**Partenaires :** {sol.get('Clients / Partenaires publics', 'Non renseigné')}")
    st.write(f"**Awards :** {sol.get('Récompenses / Accélérations', 'N/A')}")
