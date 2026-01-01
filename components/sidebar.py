"""
Sidebar Dark Theme Moderne.
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, APP_CONFIG


def render_sidebar(df: pd.DataFrame) -> None:
    """Sidebar dark theme avec navigation et stats."""
    
    with st.sidebar:
        # Logo & Brand
        st.markdown(f"""
            <div style="text-align: center; padding: 1.5rem 0 2rem 0;">
                <div style="
                    width: 50px; 
                    height: 50px; 
                    background: linear-gradient(135deg, #a78bfa, #818cf8);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 1rem auto;
                    font-size: 1.5rem;
                ">🎯</div>
                <h1 style="color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 0;">
                    Job Hunter
                </h1>
                <p style="color: #64748b; font-size: 0.7rem; margin-top: 0.25rem; letter-spacing: 1px;">
                    PERSONAL CRM v{APP_CONFIG["version"]}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        current = st.session_state.get('current_page', 'dashboard')
        
        if st.button(
            "📊  Dashboard",
            use_container_width=True,
            type="primary" if current == 'dashboard' else "secondary"
        ):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        to_analyze = len(df[df[COLUMNS["statut"]] == "À Analyser"]) if not df.empty else 0
        inbox_label = f"📥  Inbox  •  {to_analyze}" if to_analyze > 0 else "📥  Inbox"
        
        if st.button(
            inbox_label,
            use_container_width=True,
            type="primary" if current == 'inbox' else "secondary"
        ):
            st.session_state.current_page = "inbox"
            st.rerun()
        
        if st.button(
            "🎯  Pipeline",
            use_container_width=True,
            type="primary" if current == 'pipeline' else "secondary"
        ):
            st.session_state.current_page = "pipeline"
            st.rerun()
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Quick Stats
        st.markdown("""
            <p style='color: #64748b; font-size: 0.65rem; font-weight: 600; 
                      letter-spacing: 1px; margin-bottom: 0.75rem;'>
                QUICK STATS
            </p>
        """, unsafe_allow_html=True)
        
        if not df.empty:
            total = len(df)
            high_score = len(df[df[COLUMNS["score"]] >= 8])
            applied = len(df[df[COLUMNS["statut"]] == "Postulé"])
            
            # Stats
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: #94a3b8; font-size: 0.8rem;">Total Jobs</span>
                        <span style="color: #f8fafc; font-size: 1.1rem; font-weight: 700;">{total}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: #94a3b8; font-size: 0.8rem;">Score \geq 8</span>
                        <span style="color: #4ade80; font-size: 1.1rem; font-weight: 700;">{high_score}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress = applied / total if total > 0 else 0
            st.markdown(f"""
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span style="color: #94a3b8; font-size: 0.8rem;">Progression</span>
                        <span style="color: #f8fafc; font-size: 0.8rem; font-weight: 600;">{applied}/{total}</span>
                    </div>
                    <div class="progress-container-dark">
                        <div class="progress-fill-dark" style="width: {progress * 100}%; background: linear-gradient(90deg, #a78bfa, #818cf8);"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style="position: fixed; bottom: 1rem; left: 0; right: 0; text-align: center; width: inherit;">
                <p style="color: #475569; font-size: 0.7rem;">
                    Made with ❤️ & Streamlit
                </p>
            </div>
        """, unsafe_allow_html=True)