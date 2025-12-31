"""
Page Inbox - File de validation (corrigée).
==========================================
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG
from components.cards import get_score_bg, get_score_color
from database.airtable import update_job


def render_inbox_card(job: pd.Series) -> dict:
    """
    Render une carte inbox et retourne les actions.
    Utilise 100% Streamlit natif pour éviter les bugs HTML.
    """
    score = float(job[COLUMNS["score"]])
    poste = str(job[COLUMNS["poste"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    location = str(job[COLUMNS["location"]]) if job[COLUMNS["location"]] else ""
    
    bg = get_score_bg(score)
    score_color = get_score_color(score)
    
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{poste}**")
            info = f"🏢 {entreprise}"
            if location:
                info += f" • 📍 {location}"
            st.caption(info)
        
        with col2:
            st.markdown(
                f'<div style="background: {bg}; color: {score_color}; '
                f'padding: 0.4rem 0.6rem; border-radius: 15px; '
                f'font-weight: 600; font-size: 0.9rem; text-align: center;">'
                f'{score:.0f}/10</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            view = st.button("👁", key=f"view_{job['id']}", help="Voir détails")
        
        with col4:
            generate = st.button("✍️", key=f"gen_{job['id']}", help="Générer LM")
        
        with col5:
            reject = st.button("❌", key=f"reject_{job['id']}", help="Refuser")
    
    return {"view": view, "generate": generate, "reject": reject}


def render_inbox(df: pd.DataFrame, table) -> None:
    """Affiche la file d'attente des jobs à analyser."""
    
    st.markdown("## 📥 Inbox - Jobs à Analyser")
    st.markdown("---")
    
    to_review = df[df[COLUMNS["statut"]] == "À Analyser"].sort_values(
        COLUMNS["score"], ascending=False
    )
    
    # === Metrics ===
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        st.metric("À traiter", len(to_review))
    with col2:
        high = len(to_review[to_review[COLUMNS["score"]] >= 8])
        st.metric("Score \geq 8", high)
    with col3:
        avg = to_review[COLUMNS["score"]].mean() if len(to_review) > 0 else 0
        st.metric("Score moyen", f"{avg:.1f}")
    with col4:
        score_filter = st.slider(
            "Filtrer par score minimum",
            min_value=0,
            max_value=10,
            value=0,
            key="inbox_filter"
        )
    
    st.markdown("")
    
    # === Filtered List ===
    filtered = to_review[to_review[COLUMNS["score"]] >= score_filter]
    
    if filtered.empty:
        st.success("🎉 Inbox vide ! Tous les jobs ont été traités.")
        return
    
    st.caption(f"{len(filtered)} job(s) affiché(s)")
    
    # Job list
    for _, job in filtered.iterrows():
        actions = render_inbox_card(job)
        
        if actions["view"]:
            st.session_state.selected_job_id = job['id']
            st.session_state.current_page = "details"
            st.rerun()
        
        if actions["generate"]:
            update_job(table, job['id'], {COLUMNS["statut"]: "Générer LM"})
            st.rerun()
        
        if actions["reject"]:
            update_job(table, job['id'], {COLUMNS["statut"]: "Refus"})
            st.rerun()