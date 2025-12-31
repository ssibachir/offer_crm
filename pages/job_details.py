"""
Page Job Details - Vue détaillée.
=================================
Description, cover letter éditable et actions.
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG
from components.cards import get_score_class
from database.airtable import update_job, delete_job


def render_job_details(df: pd.DataFrame, table, job_id: str) -> None:
    """
    Affiche la page détaillée d'un job.
    
    Layout:
    - Gauche: Infos entreprise + description (read-only)
    - Droite: Cover letter (éditable) + statut + actions
    """
    job = df[df['id'] == job_id]
    
    if job.empty:
        st.error("❌ Job introuvable")
        if st.button("← Retour à l'Inbox"):
            st.session_state.current_page = "inbox"
            st.rerun()
        return
    
    job = job.iloc[0]
    
    # === Header ===
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Retour", use_container_width=True):
            st.session_state.current_page = "inbox"
            st.rerun()
    with col_title:
        st.markdown(f"## {job[COLUMNS['poste']]}")
    
    st.markdown("---")
    
    # === Two Column Layout ===
    col_left, col_right = st.columns([1, 1])
    
    # --- LEFT: Read-only Info ---
    with col_left:
        st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
        
        st.markdown(f"### 🏢 {job[COLUMNS['entreprise']]}")
        
        # Score & Status badges
        score = job[COLUMNS["score"]]
        score_class = get_score_class(score)
        status = job[COLUMNS["statut"]]
        status_cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
        
        st.markdown(f"""
            <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                <span class="score-badge {score_class}" style="font-size: 1rem; padding: 0.5rem 1rem;">
                    ⭐ Score: {score}/10
                </span>
                <span class="status-pill" style="background: {status_cfg['color']}20; color: {status_cfg['color']};">
                    {status_cfg['icon']} {status}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Info Grid
        st.markdown(f"""
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">📍 Localisation</div>
                    <div class="info-value">{job[COLUMNS['location']] or 'Non spécifiée'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🌐 Job Board</div>
                    <div class="info-value">{job[COLUMNS['job_board']] or 'Non spécifié'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">👤 Contact</div>
                    <div class="info-value">{job[COLUMNS['contact']] or 'Non spécifié'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📧 Email</div>
                    <div class="info-value">{job[COLUMNS['contact_mail']] or 'Non spécifié'}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Description
        st.markdown("#### 📄 Description du poste")
        description = job[COLUMNS['description']] or "Aucune description."
        st.markdown(f"""
            <div style="background: #F9FAFB; padding: 1rem; border-radius: 8px; 
                        max-height: 280px; overflow-y: auto; color: #374151;">
                {description}
            </div>
        """, unsafe_allow_html=True)
        
        # URL
        if job[COLUMNS['url']]:
            st.markdown(f"[🔗 Voir l'offre originale]({job[COLUMNS['url']]})")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- RIGHT: Editable Content ---
    with col_right:
        st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
        
        st.markdown("#### ✍️ Cover Letter")
        st.caption("Éditez la lettre avant envoi")
        
        new_letter = st.text_area(
            "Cover letter",
            value=job[COLUMNS['cover_letter']] or "",
            height=280,
            label_visibility="collapsed",
            placeholder="Votre lettre de motivation..."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Status dropdown
        st.markdown("#### 🔄 Statut")
        status_options = list(STATUS_CONFIG.keys())
        current_idx = status_options.index(status) if status in status_options else 0
        
        new_status = st.selectbox(
            "Statut",
            options=status_options,
            index=current_idx,
            format_func=lambda x: f"{STATUS_CONFIG[x]['icon']} {x}",
            label_visibility="collapsed"
        )
        
        # Contact fields
        st.markdown("#### 📞 Suivi")
        c1, c2 = st.columns(2)
        with c1:
            new_contact = st.text_input("Contact", value=job[COLUMNS['contact']] or "")
        with c2:
            new_relance = st.text_input("Relance", value=job[COLUMNS['relance']] or "")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action buttons
        btn1, btn2, btn3 = st.columns(3)
        
        with btn1:
            if st.button("💾 Sauvegarder", type="primary", use_container_width=True):
                updates = {
                    COLUMNS["cover_letter"]: new_letter,
                    COLUMNS["statut"]: new_status,
                    COLUMNS["contact"]: new_contact,
                    COLUMNS["relance"]: new_relance,
                }
                update_job(table, job['id'], updates)
                st.success("✅ Sauvegardé!")
                st.rerun()
        
        with btn2:
            if st.button("📤 Marquer Prêt", use_container_width=True):
                update_job(table, job['id'], {
                    COLUMNS["cover_letter"]: new_letter,
                    COLUMNS["statut"]: "Pret"
                })
                st.success("✅ Prêt!")
                st.rerun()
        
        with btn3:
            if st.button("🗑 Supprimer", use_container_width=True):
                if st.session_state.get('confirm_delete') == job['id']:
                    delete_job(table, job['id'])
                    st.session_state.current_page = "inbox"
                    st.session_state.confirm_delete = None
                    st.rerun()
                else:
                    st.session_state.confirm_delete = job['id']
                    st.warning("Cliquez encore pour confirmer")
        
        st.markdown('</div>', unsafe_allow_html=True)