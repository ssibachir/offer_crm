"""
Composants UI réutilisables - Version corrigée.
===============================================
Cards, badges et éléments visuels avec rendu fiable.
"""

import streamlit as st
import pandas as pd

from config.settings import COLUMNS, STATUS_CONFIG, SCORE_THRESHOLDS


def get_score_class(score: float) -> str:
    """Retourne la classe CSS selon le score."""
    if score >= SCORE_THRESHOLDS["high"]:
        return "score-high"
    elif score >= SCORE_THRESHOLDS["medium"]:
        return "score-medium"
    return "score-low"


def get_score_color(score: float) -> str:
    """Retourne la couleur selon le score."""
    if score >= SCORE_THRESHOLDS["high"]:
        return "#166534"  # Green
    elif score >= SCORE_THRESHOLDS["medium"]:
        return "#92400E"  # Amber
    return "#991B1B"  # Red


def get_score_bg(score: float) -> str:
    """Retourne le background selon le score."""
    if score >= SCORE_THRESHOLDS["high"]:
        return "#DCFCE7"
    elif score >= SCORE_THRESHOLDS["medium"]:
        return "#FEF3C7"
    return "#FEE2E2"


def render_kpi_card(icon: str, value, label: str, color: str = None) -> None:
    """Affiche une carte KPI stylisée."""
    color_style = f"color: {color};" if color else ""
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value" style="{color_style}">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_job_card(job: pd.Series, show_status: bool = False) -> str:
    """
    Affiche une carte job avec Streamlit natif.
    
    Utilise st.container() et colonnes pour un rendu fiable.
    """
    score = float(job[COLUMNS["score"]])
    poste = str(job[COLUMNS["poste"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    location = str(job[COLUMNS["location"]]) if job[COLUMNS["location"]] else ""
    status = str(job[COLUMNS["statut"]])
    
    # Container avec styling
    with st.container():
        # Card wrapper
        st.markdown("""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 1rem 1.25rem;
                margin-bottom: 0.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border: 1px solid #E5E7EB;
            ">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            # Titre du poste
            st.markdown(f"**{poste}**")
            # Entreprise
            st.caption(f"🏢 {entreprise}")
            # Location
            if location:
                st.caption(f"📍 {location}")
            # Status badge
            if show_status:
                cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
                st.markdown(
                    f'<span style="color: {cfg["color"]}; font-size: 0.8rem;">'
                    f'{cfg["icon"]} {status}</span>',
                    unsafe_allow_html=True
                )
        
        with col2:
            # Score badge
            bg = get_score_bg(score)
            color = get_score_color(score)
            st.markdown(
                f'<div style="background: {bg}; color: {color}; '
                f'padding: 0.4rem 0.8rem; border-radius: 20px; '
                f'font-weight: 600; font-size: 0.85rem; text-align: center;">'
                f'{score:.0f}/10</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_job_card_v2(job: pd.Series, show_status: bool = False) -> None:
    """
    Version alternative 100% Streamlit natif.
    Plus fiable pour le rendu.
    """
    score = float(job[COLUMNS["score"]])
    poste = str(job[COLUMNS["poste"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    location = str(job[COLUMNS["location"]]) if job[COLUMNS["location"]] else ""
    status = str(job[COLUMNS["statut"]])
    
    # Emoji selon le score
    if score >= 8:
        score_emoji = "🟢"
    elif score >= 5:
        score_emoji = "🟡"
    else:
        score_emoji = "🔴"
    
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.markdown(f"**{poste}**")
            
            info_parts = [f"🏢 {entreprise}"]
            if location:
                info_parts.append(f"📍 {location}")
            st.caption(" • ".join(info_parts))
            
            if show_status:
                cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
                st.caption(f"{cfg['icon']} {status}")
        
        with col2:
            st.metric(
                label="Score",
                value=f"{score:.0f}",
                delta=None,
                label_visibility="collapsed"
            )
            st.caption(f"{score_emoji} /10")


def render_kanban_card(job: pd.Series, status: str) -> None:
    """Affiche une carte Kanban compacte."""
    color = STATUS_CONFIG.get(status, {}).get("color", "#6B7280")
    score = float(job[COLUMNS["score"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    poste = str(job[COLUMNS["poste"]])
    
    # Truncate
    poste_short = poste[:30] + "..." if len(poste) > 30 else poste
    
    # Score styling
    bg = get_score_bg(score)
    score_color = get_score_color(score)
    
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border-left: 3px solid {color};
        ">
            <div style="font-weight: 600; color: #1F2937; font-size: 0.85rem; margin-bottom: 0.25rem;">
                {entreprise}
            </div>
            <div style="color: #6B7280; font-size: 0.75rem; margin-bottom: 0.5rem;">
                {poste_short}
            </div>
            <span style="
                background: {bg}; 
                color: {score_color}; 
                padding: 0.2rem 0.5rem; 
                border-radius: 10px; 
                font-size: 0.7rem; 
                font-weight: 600;
            ">⭐ {score:.0f}/10</span>
        </div>
    """, unsafe_allow_html=True)