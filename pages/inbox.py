"""
Page Inbox - Jobs à Analyser.
=============================
Interface originale avec compteur dynamique et suppression.
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG
from database.airtable import update_job, delete_job


def render_inbox(df: pd.DataFrame, table) -> None:
    """Page Inbox."""
    
    # Header
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            <span style="font-size: 1.5rem;">📧</span>
            <h1 style="font-size: 1.5rem; font-weight: 700; color: #f8fafc; margin: 0;">
                Inbox - Jobs à Analyser
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    total = len(df[df[COLUMNS["statut"]] == "À Analyser"])
    high_score = len(df[(df[COLUMNS["statut"]] == "À Analyser") & (df[COLUMNS["score"]] >= 8)])
    avg_score = df[df[COLUMNS["statut"]] == "À Analyser"][COLUMNS["score"]].mean() if total > 0 else 0
    
    stat_cols = st.columns(3)
    
    with stat_cols[0]:
        st.markdown(f"""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;text-align:center;">
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.25rem;">À traiter</div>
                <div style="font-size:1.75rem;font-weight:700;color:#f8fafc;">{total}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[1]:
        st.markdown(f"""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;text-align:center;">
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.25rem;">Score \geq 8</div>
                <div style="font-size:1.75rem;font-weight:700;color:#4ade80;">{high_score}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[2]:
        st.markdown(f"""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;text-align:center;">
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.25rem;">Score moyen</div>
                <div style="font-size:1.75rem;font-weight:700;color:#a78bfa;">{avg_score:.1f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    # Filtre par score
    min_score = st.slider(
        "Filtrer par score minimum",
        min_value=0,
        max_value=10,
        value=0,
        step=1,
        key="score_filter"
    )
    
    # Filtrer les jobs : À Analyser + score >= min_score
    filtered_df = df[
        (df[COLUMNS["statut"]] == "À Analyser") & 
        (df[COLUMNS["score"]] >= min_score)
    ].sort_values(COLUMNS["score"], ascending=False)
    
    filtered_count = len(filtered_df)
    
    # Compteur dynamique
    st.markdown(f"""
        <div style="color:#64748b;font-size:0.85rem;margin:0.75rem 0 1rem 0;">
            <strong style="color:#f8fafc;">{filtered_count}</strong> job(s) affiché(s)
            {f'<span style="color:#a78bfa;margin-left:0.5rem;">(score \geq {min_score})</span>' if min_score > 0 else ''}
        </div>
    """, unsafe_allow_html=True)
    
    # Liste des jobs
    if filtered_df.empty:
        st.info("Aucun job ne correspond aux filtres")
    else:
        for _, job in filtered_df.iterrows():
            render_job_card(job, table)


def render_job_card(job: pd.Series, table) -> None:
    """Carte job style original."""
    
    job_id = job['id']
    score = float(job[COLUMNS["score"]])
    poste = str(job[COLUMNS["poste"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    location = str(job[COLUMNS["location"]]) if pd.notna(job[COLUMNS["location"]]) else ""
    source = str(job.get(COLUMNS.get("source", "source"), "")) if "source" in COLUMNS else ""
    
    # Style du score
    if score >= 8:
        score_bg, score_color = "rgba(74,222,128,0.15)", "#4ade80"
    elif score >= 5:
        score_bg, score_color = "rgba(251,146,60,0.15)", "#fb923c"
    else:
        score_bg, score_color = "rgba(248,113,113,0.15)", "#f87171"
    
    with st.container(border=True):
        # Layout principal
        col_content, col_actions = st.columns([5, 1])
        
        with col_content:
            # Titre du poste
            st.markdown(f"""
                <div style="font-size:0.95rem;font-weight:600;color:#f8fafc;margin-bottom:0.4rem;">
                    {poste[:70]}{'...' if len(poste) > 70 else ''}
                </div>
            """, unsafe_allow_html=True)
            
            # Source
            if source:
                st.markdown(f"""
                    <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.25rem;">
                        {source}
                    </div>
                """, unsafe_allow_html=True)
            
            # Location
            if location:
                st.markdown(f"""
                    <div style="font-size:0.8rem;color:#64748b;">
                        📍 {location}
                    </div>
                """, unsafe_allow_html=True)
        
        with col_actions:
            # Score badge
            st.markdown(f"""
                <div style="background:{score_bg};color:{score_color};padding:0.35rem 0.6rem;border-radius:8px;font-size:0.85rem;font-weight:700;text-align:center;margin-bottom:0.5rem;">
                    {score:.0f}/10
                </div>
            """, unsafe_allow_html=True)
            
            # Boutons d'action
            btn_cols = st.columns(3)
            
            with btn_cols[0]:
                if st.button("👁", key=f"view_{job_id}", help="Voir"):
                    st.session_state.selected_job_id = job_id
                    st.session_state.current_page = "details"
                    st.rerun()
            
            with btn_cols[1]:
                if st.button("✏️", key=f"edit_{job_id}", help="Éditer statut"):
                    st.session_state[f"edit_{job_id}"] = True
                    st.rerun()
            
            with btn_cols[2]:
                if st.button("❌", key=f"del_{job_id}", help="Supprimer"):
                    st.session_state[f"confirm_del_{job_id}"] = True
                    st.rerun()
        
        # Modal édition statut
        if st.session_state.get(f"edit_{job_id}", False):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                new_status = st.selectbox(
                    "Nouveau statut",
                    options=["À Analyser", "Générer LM", "Prêt", "Postulé"],
                    key=f"status_{job_id}",
                    label_visibility="collapsed"
                )
            
            with col2:
                if st.button("✅ Valider", key=f"save_{job_id}"):
                    update_job(table, job_id, {COLUMNS["statut"]: new_status})
                    del st.session_state[f"edit_{job_id}"]
                    st.rerun()
            
            with col3:
                if st.button("↩️ Annuler", key=f"cancel_{job_id}"):
                    del st.session_state[f"edit_{job_id}"]
                    st.rerun()
        
        # Modal confirmation suppression
        if st.session_state.get(f"confirm_del_{job_id}", False):
            st.markdown("---")
            st.error("⚠️ **Supprimer définitivement cette offre ?**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Oui, supprimer", key=f"yes_{job_id}", type="primary"):
                    try:
                        delete_job(table, job_id)
                        del st.session_state[f"confirm_del_{job_id}"]
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
            
            with col2:
                if st.button("↩️ Annuler", key=f"no_{job_id}"):
                    del st.session_state[f"confirm_del_{job_id}"]
                    st.rerun()