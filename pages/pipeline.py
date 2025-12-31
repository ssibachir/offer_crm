"""
Page Pipeline - Vue Kanban (corrigée).
=====================================
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG, PIPELINE_ORDER
from components.cards import get_score_bg, get_score_color
from database.airtable import update_job


def render_pipeline(df: pd.DataFrame, table) -> None:
    """Affiche le pipeline Kanban."""
    
    st.markdown("## 🎯 Pipeline - Vue Kanban")
    st.markdown("---")
    
    cols = st.columns(len(PIPELINE_ORDER))
    
    for idx, status in enumerate(PIPELINE_ORDER):
        cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
        jobs_in_status = df[df[COLUMNS["statut"]] == status].sort_values(
            COLUMNS["score"], ascending=False
        )
        count = len(jobs_in_status)
        
        with cols[idx]:
            # Header
            st.markdown(
                f"### {cfg['icon']} {status}",
            )
            st.caption(f"{count} job(s)")
            
            st.markdown("---")
            
            # Cards
            for _, job in jobs_in_status.iterrows():
                score = float(job[COLUMNS["score"]])
                entreprise = str(job[COLUMNS["entreprise"]])
                poste = str(job[COLUMNS["poste"]])[:28]
                
                bg = get_score_bg(score)
                score_color = get_score_color(score)
                
                with st.container(border=True):
                    st.markdown(f"**{entreprise}**")
                    st.caption(poste)
                    
                    # Score
                    st.markdown(
                        f'<span style="background: {bg}; color: {score_color}; '
                        f'padding: 0.2rem 0.5rem; border-radius: 10px; '
                        f'font-size: 0.75rem; font-weight: 600;">'
                        f'⭐ {score:.0f}/10</span>',
                        unsafe_allow_html=True
                    )
                    
                    # Buttons
                    b1, b2 = st.columns(2)
                    
                    with b1:
                        if st.button("👁", key=f"k_view_{job['id']}", use_container_width=True):
                            st.session_state.selected_job_id = job['id']
                            st.session_state.current_page = "details"
                            st.rerun()
                    
                    with b2:
                        current_idx = PIPELINE_ORDER.index(status)
                        if current_idx < len(PIPELINE_ORDER) - 2:
                            next_status = PIPELINE_ORDER[current_idx + 1]
                            if st.button("→", key=f"k_next_{job['id']}", use_container_width=True):
                                update_job(table, job['id'], {COLUMNS["statut"]: next_status})
                                st.rerun()