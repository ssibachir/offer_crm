"""
Page Pipeline - Vue Kanban.
===========================
4 colonnes : À Analyser, Générer LM, Prêt, Postulé
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG
from database.airtable import update_job

# 4 colonnes seulement (sans Refus)
KANBAN_COLUMNS = ["À Analyser", "Générer LM", "Prêt", "Postulé"]


def get_score_style(score: float) -> tuple[str, str]:
    """Retourne (background, color) pour le score."""
    if score >= 8:
        return "rgba(74, 222, 128, 0.15)", "#4ade80"
    elif score >= 5:
        return "rgba(251, 146, 60, 0.15)", "#fb923c"
    return "rgba(248, 113, 113, 0.15)", "#f87171"


def render_pipeline(df: pd.DataFrame, table) -> None:
    """Page Pipeline principale."""
    
    # Header
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.25rem;">
                🎯 Pipeline
            </h1>
            <p style="color: #64748b; font-size: 0.9rem;">
                Suivez la progression de vos candidatures
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats (4 colonnes alignées avec kanban)
    total = len(df)
    in_progress = len(df[~df[COLUMNS["statut"]].isin(["Postulé", "Refus"])])
    applied = len(df[df[COLUMNS["statut"]] == "Postulé"])
    conversion = (applied / total * 100) if total > 0 else 0
    
    stat_cols = st.columns(4)
    stats = [
        ("📊", total, "Total", "#a78bfa"),
        ("⏳", in_progress, "En cours", "#60a5fa"),
        ("✅", applied, "Postulés", "#4ade80"),
        ("📈", f"{conversion:.0f}%", "Conversion", "#f472b6"),
    ]
    
    for col, (icon, value, label, color) in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
                <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;text-align:center;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                    <div style="font-size:0.75rem;color:#64748b;">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    # Kanban (4 colonnes)
    kanban_cols = st.columns(4)
    
    for col_idx, status in enumerate(KANBAN_COLUMNS):
        cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
        status_jobs = df[df[COLUMNS["statut"]] == status].sort_values(COLUMNS["score"], ascending=False)
        count = len(status_jobs)
        
        with kanban_cols[col_idx]:
            # Header
            st.markdown(f"""
                <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:0.75rem;margin-bottom:0.75rem;display:flex;align-items:center;justify-content:space-between;">
                    <div style="display:flex;align-items:center;gap:0.5rem;">
                        <span style="color:{cfg['color']};font-size:1.1rem;">{cfg['icon']}</span>
                        <span style="color:#f8fafc;font-weight:600;font-size:0.9rem;">{status}</span>
                    </div>
                    <span style="background:{cfg['color']}20;color:{cfg['color']};padding:0.2rem 0.6rem;border-radius:8px;font-size:0.75rem;font-weight:600;">{count}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Cards
            if status_jobs.empty:
                st.markdown("""
                    <div style="background:rgba(30,41,59,0.4);border:1px dashed #334155;border-radius:8px;padding:2rem 0.75rem;text-align:center;color:#64748b;font-size:0.85rem;">Aucun job</div>
                """, unsafe_allow_html=True)
            else:
                for _, job in status_jobs.iterrows():
                    render_job_card(job, col_idx, table)


def render_job_card(job: pd.Series, col_idx: int, table):
    """Carte job."""
    job_id = job['id']
    score = float(job[COLUMNS["score"]])
    entreprise = str(job[COLUMNS["entreprise"]])[:22]
    poste = str(job[COLUMNS["poste"]])
    location = str(job[COLUMNS["location"]]) if pd.notna(job[COLUMNS["location"]]) else ""
    
    score_bg, score_color = get_score_style(score)
    poste_short = poste[:35] + "..." if len(poste) > 35 else poste
    loc_short = location[:28] + "..." if len(location) > 28 else location
    
    with st.container(border=True):
        # Entreprise + Score
        st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                <span style="font-size:0.75rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.3px;">{entreprise}</span>
                <span style="background:{score_bg};color:{score_color};padding:0.25rem 0.5rem;border-radius:6px;font-size:0.8rem;font-weight:700;">{score:.0f}/10</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Titre
        st.markdown(f"""
            <div style="font-size:0.9rem;font-weight:500;color:#f8fafc;line-height:1.35;margin-bottom:0.4rem;">{poste_short}</div>
        """, unsafe_allow_html=True)
        
        # Location
        if loc_short:
            st.caption(f"📍 {loc_short}")
        
        # Boutons
        b1, b2, b3 = st.columns(3)
        
        with b1:
            if col_idx > 0:
                if st.button("←", key=f"p_{job_id}", use_container_width=True):
                    update_job(table, job_id, {COLUMNS["statut"]: KANBAN_COLUMNS[col_idx - 1]})
                    st.rerun()
        
        with b2:
            if st.button("👁", key=f"v_{job_id}", use_container_width=True):
                st.session_state.selected_job_id = job_id
                st.session_state.current_page = "details"
                st.rerun()
        
        with b3:
            if col_idx < len(KANBAN_COLUMNS) - 1:
                if st.button("→", key=f"n_{job_id}", use_container_width=True):
                    update_job(table, job_id, {COLUMNS["statut"]: KANBAN_COLUMNS[col_idx + 1]})
                    st.rerun()