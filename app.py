"""
Job Hunter CRM - Personal Job Application Tracker
==================================================
Point d'entrée principal de l'application.

Usage:
    streamlit run app.py
"""

import streamlit as st

from config.settings import APP_CONFIG
from config.styles import inject_custom_css
from database.airtable import get_airtable_connection, load_jobs_data
from components.sidebar import render_sidebar
from pages.dashboard import render_dashboard
from pages.inbox import render_inbox
from pages.job_details import render_job_details
from pages.pipeline import render_pipeline


def init_session_state() -> None:
    """Initialise les variables de session Streamlit."""
    defaults = {
        'current_page': 'dashboard',
        'selected_job_id': None,
        'confirm_delete': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    """
    Fonction principale - Orchestration de l'application.
    
    Workflow:
    1. Configuration de la page
    2. Injection du CSS
    3. Initialisation session state
    4. Connexion Airtable
    5. Chargement des données
    6. Routing vers la page appropriée
    """
    # Page config
    st.set_page_config(
        page_title=APP_CONFIG["title"],
        page_icon=APP_CONFIG["icon"],
        layout=APP_CONFIG["layout"],
        initial_sidebar_state="expanded"
    )
    
    # CSS injection
    inject_custom_css()
    
    # Session state
    init_session_state()
    
    # Database connection
    table = get_airtable_connection()
    
    # Load data
    with st.spinner('📊 Chargement des données...'):
        df = load_jobs_data(table)
    
    # Handle empty data
    if df.empty:
        st.warning("⚠️ Aucune donnée trouvée dans Airtable.")
        st.info("Vérifiez votre configuration dans `.streamlit/secrets.toml`")
        return
    
    # Render sidebar & get current page
    render_sidebar(df)
    
    # Page routing
    current_page = st.session_state.current_page
    
    match current_page:
        case 'dashboard':
            render_dashboard(df)
        case 'inbox':
            render_inbox(df, table)
        case 'details':
            if st.session_state.selected_job_id:
                render_job_details(df, table, st.session_state.selected_job_id)
            else:
                st.session_state.current_page = 'inbox'
                st.rerun()
        case 'pipeline':
            render_pipeline(df, table)
        case _:
            render_dashboard(df)


if __name__ == "__main__":
    main()