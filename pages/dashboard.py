"""
Page Dashboard - Vue d'ensemble (corrigée).
===========================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config.settings import COLUMNS, COLORS, STATUS_CONFIG, SCORE_THRESHOLDS
from components.cards import render_kpi_card, get_score_bg, get_score_color


def render_high_priority_card(job: pd.Series) -> None:
    """Render une carte high priority avec Streamlit natif."""
    score = float(job[COLUMNS["score"]])
    poste = str(job[COLUMNS["poste"]])
    entreprise = str(job[COLUMNS["entreprise"]])
    location = str(job[COLUMNS["location"]]) if job[COLUMNS["location"]] else ""
    status = str(job[COLUMNS["statut"]])
    
    cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#6B7280"})
    bg = get_score_bg(score)
    score_color = get_score_color(score)
    
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{poste}**")
            st.caption(f"🏢 {entreprise}")
            if location:
                st.caption(f"📍 {location}")
            st.markdown(
                f'<span style="color: {cfg["color"]}; font-size: 0.8rem;">'
                f'{cfg["icon"]} {status}</span>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f'<div style="background: {bg}; color: {score_color}; '
                f'padding: 0.5rem 0.75rem; border-radius: 20px; '
                f'font-weight: 700; font-size: 1rem; text-align: center; '
                f'margin-top: 0.5rem;">'
                f'{score:.0f}/10</div>',
                unsafe_allow_html=True
            )


def render_dashboard(df: pd.DataFrame) -> None:
    """Affiche le dashboard principal."""
    
    st.markdown("## 📊 Dashboard")
    st.markdown("---")
    
    # === KPIs ===
    total = len(df)
    to_analyze = len(df[df[COLUMNS["statut"]] == "À Analyser"])
    to_generate = len(df[df[COLUMNS["statut"]] == "Générer LM"])
    ready = len(df[df[COLUMNS["statut"]] == "Pret"])
    applied = len(df[df[COLUMNS["statut"]] == "Postulé"])
    
    cols = st.columns(5)
    kpis = [
        ("📁", total, "Total Scrappés", COLORS["primary"]),
        ("🔍", to_analyze, "À Analyser", COLORS["warning"]),
        ("✍️", to_generate, "LM à Générer", COLORS["secondary"]),
        ("📤", ready, "Prêts", COLORS["info"]),
        ("✅", applied, "Postulés", COLORS["success"]),
    ]
    
    for col, (icon, value, label, color) in zip(cols, kpis):
        with col:
            render_kpi_card(icon, value, label, color)
    
    st.markdown("")
    st.markdown("")
    
    # === Two columns ===
    col_left, col_right = st.columns([1, 1])
    
    # --- Left: High Priority ---
    with col_left:
        st.markdown("### 🔥 High Priority")
        st.caption(f"Score \geq {SCORE_THRESHOLDS['high']}")
        
        high_priority = df[
            df[COLUMNS["score"]] >= SCORE_THRESHOLDS["high"]
        ].sort_values(COLUMNS["score"], ascending=False).head(5)
        
        if high_priority.empty:
            st.info("Aucun job haute priorité (score \geq 8)")
        else:
            for _, job in high_priority.iterrows():
                render_high_priority_card(job)
                if st.button(
                    "📄 Voir détails",
                    key=f"hp_{job['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_job_id = job['id']
                    st.session_state.current_page = "details"
                    st.rerun()
    
    # --- Right: Chart + Stats ---
    with col_right:
        st.markdown("### 📈 Distribution des Statuts")
        
        if not df.empty:
            status_counts = df[COLUMNS["statut"]].value_counts().reset_index()
            status_counts.columns = ['Statut', 'Count']
            
            colors = [
                STATUS_CONFIG.get(s, {}).get("color", "#6B7280")
                for s in status_counts['Statut']
            ]
            
            fig = go.Figure(data=[go.Pie(
                labels=status_counts['Statut'],
                values=status_counts['Count'],
                hole=0.6,
                marker_colors=colors,
                textinfo='label+value',
                textposition='outside',
                textfont_size=11,
            )])
            
            fig.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                height=260,
                annotations=[dict(
                    text=f'<b>{total}</b><br>Total',
                    x=0.5, y=0.5,
                    font_size=16,
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Stats
        st.markdown("#### 📊 Statistiques")
        avg_score = df[COLUMNS["score"]].mean() if not df.empty else 0
        refused = len(df[df[COLUMNS["statut"]] == "Refus"])
        conversion = (applied / total * 100) if total > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Score moyen", f"{avg_score:.1f}/10")
        c2.metric("Conversion", f"{conversion:.0f}%")
        c3.metric("Refusés", refused)