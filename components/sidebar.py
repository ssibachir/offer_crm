"""
Sidebar de navigation.
======================
Menu principal et statistiques rapides.
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, APP_CONFIG


def render_sidebar(df: pd.DataFrame) -> None:
    """
    Affiche la sidebar avec navigation et stats.
    
    Args:
        df: DataFrame pour calculer les métriques
    """
    with st.sidebar:
        # Header
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="color: white; font-size: 1.5rem; margin: 0;">
                    {APP_CONFIG["icon"]} Job Hunter
                </h1>
                <p style="color: #9CA3AF; font-size: 0.75rem; margin-top: 0.5rem;">
                    Personal CRM v{APP_CONFIG["version"]}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown(
            "<p style='color: #9CA3AF; font-size: 0.75rem;'>NAVIGATION</p>",
            unsafe_allow_html=True
        )
        
        current = st.session_state.get('current_page', 'dashboard')
        
        # Dashboard button
        if st.button(
            "📊 Dashboard",
            use_container_width=True,
            type="primary" if current == 'dashboard' else "secondary"
        ):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        # Inbox button with badge
        to_analyze = len(df[df[COLUMNS["statut"]] == "À Analyser"]) if not df.empty else 0
        inbox_label = f"📥 Inbox ({to_analyze})" if to_analyze > 0 else "📥 Inbox"
        
        if st.button(
            inbox_label,
            use_container_width=True,
            type="primary" if current == 'inbox' else "secondary"
        ):
            st.session_state.current_page = "inbox"
            st.rerun()
        
        # Pipeline button
        if st.button(
            "🎯 Pipeline",
            use_container_width=True,
            type="primary" if current == 'pipeline' else "secondary"
        ):
            st.session_state.current_page = "pipeline"
            st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown(
            "<p style='color: #9CA3AF; font-size: 0.75rem;'>QUICK STATS</p>",
            unsafe_allow_html=True
        )
        
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", len(df))
            with col2:
                high_score = len(df[df[COLUMNS["score"]] >= 8])
                st.metric("Score \geq8", high_score)
            
            # Progress bar
            applied = len(df[df[COLUMNS["statut"]] == "Postulé"])
            total = len(df)
            progress = applied / total if total > 0 else 0
            st.progress(progress, text=f"{applied}/{total} postulés")
        
        st.markdown("---")
        st.caption("Made with ❤️ & Streamlit")