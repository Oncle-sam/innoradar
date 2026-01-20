import streamlit as st

def render_innovation_card(db, logo_text, status, name, verified, location, description, impact_key, impact_value):
    """Affiche une carte d'innovation 'À la une' avec redirection fonctionnelle."""
    verified_badge = " <span style='color:#4B79FF;'>✔</span>" if verified else ""
    status_class = "badge-new" if status == "Nouveauté" else "badge-purple"
    
    # Rendu Visuel HTML
    st.markdown(f"""
    <div class="innovation-card">
        <div class="card-header-flex">
            <div class="card-logo-placeholder-small" style="background:#252941; width:50px; height:50px; display:flex; align-items:center; justify-content:center; border-radius:8px;">{logo_text}</div>
            <div class="card-info-col" style="margin-left:15px;">
                <div class="badges-row"><span class="badge-dark {status_class}">{status}</span></div>
                <div class="card-title-small" style="margin:0; font-size:16px; font-weight:700;">{name}{verified_badge}</div>
                <div class="card-meta-small" style="margin:0; color:#a0a2b3; font-size:12px;">📍 {location}</div>
            </div>
        </div>
        <p style="font-size:13px; margin: 15px 0; color:#e0e0e0; height:60px; overflow:hidden;">{description}</p>
        <div style="background:#0b0e17; padding:8px; border-radius:8px; margin-bottom:10px;">
            <div style="font-size:10px; color:#a0a2b3; text-transform:uppercase;">Impact Clé</div>
            <div style="font-weight:700; color:#4ade80; font-size:14px;">{impact_key}: {impact_value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bouton Streamlit pour redirection (Le lien avec le CSV)
    if st.button(f"Plus d'informations sur {name}", key=f"home_btn_{name}", use_container_width=True):
        # On cherche la ligne correspondante dans le CSV
        sol_data = db.df[db.df['Dénomination actuelle'] == name]
        if not sol_data.empty:
            st.session_state.selected_solution = sol_data.iloc[0]
            st.session_state.page = 'details'
            st.rerun()
        else:
            st.error(f"Erreur : '{name}' est introuvable dans le fichier CSV.")

def render_home(db):
    # --- BLOC 1 : WIZARD ---
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>📡 Lancer le radar</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a0a2b3; font-weight: 400; margin-top: 10px;'>Trouvez la solution réellement adaptée à votre besoin.</h3>", unsafe_allow_html=True)
    st.markdown("---")

    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1

    col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])
    
    with col_main:
        if st.session_state.wizard_step == 1:
            st.subheader("1. Votre profil")
            st.write("Sélectionnez le profil correspondant le mieux à votre organisation.")
            profils = [
                "Club professionnel", "Club amateur / Association", "Ligue / Comité", 
                "Fédération", "Organisateur événement / compétition", "Sponsor / Mécène", 
                "Média", "Ayant Droit", "Fournisseur biens / services", "Entreprise", 
                "Fan / Supporter", "Sportif amateur", "Staff technique", "Sportif professionnel"
            ]
            choix = st.multiselect("Profil(s) :", profils, key="home_profil_select")
            if st.button("Suivant ➝", key="home_next_1", type="primary", use_container_width=True):
                if choix:
                    st.session_state.user_profile = choix
                    st.session_state.wizard_step = 2
                    st.rerun()
                else:
                    st.warning("Veuillez sélectionner au moins un profil.")

        elif st.session_state.wizard_step == 2:
            st.subheader("2. Votre besoin")
            st.write("Décrivez votre besoin, vos freins opérationnels ou défis actuels.")
            user_need = st.text_area("Besoin :", height=150, key="home_need_input", placeholder="Ex: Améliorer l'engagement des fans...")
            c1, c2 = st.columns([1, 2])
            if c1.button("← Retour", key="home_back_2", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
            if c2.button("Suivant ➝", key="home_next_2", type="primary", use_container_width=True):
                if user_need.strip():
                    st.session_state.user_need = user_need
                    st.session_state.wizard_step = 3
                    st.rerun()

        elif st.session_state.wizard_step == 3:
            st.subheader("3. Votre objectif")
            st.write("Définissez vos objectifs et résultats attendus.")
            user_goal = st.text_area("Objectif :", height=100, key="home_goal_input", placeholder="Ex: Augmenter les revenus de billetterie de 10%...")
            c1, c2 = st.columns([1, 2])
            if c1.button("← Retour", key="home_back_3", use_container_width=True):
                st.session_state.wizard_step = 2
                st.rerun()
            if c2.button("Lancer le radar 🚀", key="home_launch", type="primary", use_container_width=True):
                st.session_state.user_goal = user_goal
                st.session_state.current_query = f"{st.session_state.user_need} {user_goal}"
                st.session_state.page = 'results'
                st.rerun()

    # --- BLOC 2 : INFOS CLÉS ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='text-align: center; color: #a0a2b3;'>
            <p><strong>{len(db.df) if db.df is not None else '900+'}</strong> solutions indexées • Propulsé par l'IA d'InnoRadar</p>
        </div>
    """, unsafe_allow_html=True)

    # --- BLOC 3 : INNOVATIONS À LA UNE ---
    st.markdown("<br><br><h2 style='text-align:center;'>Les innovations à la une</h2>", unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        render_innovation_card(db, "AR", "Sponsorisé", "Arioneo", True, "France", "Suivi de performance équine.", "Précision", "+99%")
    with i2:
        render_innovation_card(db, "VC", "Nouveauté", "VOGO", True, "Montpellier", "Live video pour staffs techniques.", "Gain de temps", "Instantané")
    with i3:
        render_innovation_card(db, "SK", "Sponsorisé", "SkillCorner", False, "Paris", "Tracking automatisé via flux TV.", "Couverture", "+60 compétitions")

    # --- BLOC 4 : ÉCOSYSTÈME ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg, #1a1d2e 0%, #0b0e17 100%); padding:40px; border-radius:20px; text-align:center; border:1px solid #2a2e45;">
        <h2 style="margin:0;">Libérez la Puissance d'InnoRadar</h2>
        <p style="color:#a0a2b3;">Rejoignez l'écosystème leader de la sport tech pour accéder aux fonctionnalités exclusives.</p>
        <div style="display:flex; justify-content:center; gap:30px; margin:25px 0;">
            <div style="font-size:14px;"><span style="color:#7F56D9;">◈</span> Assistant Projet IA</div>
            <div style="font-size:14px;"><span style="color:#7F56D9;">◈</span> Filtres Pro Avancés</div>
            <div style="font-size:14px;"><span style="color:#7F56D9;">◈</span> Sauvegarder & Comparer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Se Connecter", key="home_login_cta", use_container_width=True):
        st.toast("Module de connexion à venir")

    # --- FOOTER ---
    st.markdown("<br><br><hr style='border-color:#1f233a;'>", unsafe_allow_html=True)
    f_col1, f_col2 = st.columns([1, 1])
    with f_col1:
        st.markdown("⚡ **InnoRadar**")
    with f_col2:
        st.markdown("""
            <div style="text-align:right; font-size:12px; color:#555;">
                Mentions Légales | Confidentialité & RGPD
            </div>
        """, unsafe_allow_html=True)
