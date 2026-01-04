"""
Page Dashboard - Dark Theme Moderne.
====================================
Utilise Date Scraping pour les graphiques, scores affichés en /10.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from config.settings import COLUMNS, STATUS_CONFIG, SCORE_THRESHOLDS, PIPELINE_ORDER


def get_weekly_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les données par semaine en utilisant la colonne Date Scraping.
    
    Returns:
        DataFrame avec colonnes: week_label, count, avg_score, applied_count
    """
    # Convertir Date Scraping en datetime
    df_dated = df.copy()
    
    if COLUMNS["date_scraping"] in df_dated.columns:
        df_dated['_date'] = pd.to_datetime(df_dated[COLUMNS["date_scraping"]], errors='coerce')
    else:
        # Fallback si pas de colonne
        df_dated['_date'] = pd.NaT
    
    # Créer la structure des 8 dernières semaines
    today = datetime.now()
    weeks_data = []
    
    for i in range(7, -1, -1):
        week_start = today - timedelta(weeks=i)
        week_start = week_start - timedelta(days=week_start.weekday())  # Lundi
        week_end = week_start + timedelta(days=6)  # Dimanche
        
        # Format: "23 Déc"
        month_names = {
            'Jan': 'Jan', 'Feb': 'Fév', 'Mar': 'Mar', 'Apr': 'Avr',
            'May': 'Mai', 'Jun': 'Juin', 'Jul': 'Juil', 'Aug': 'Août',
            'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Déc'
        }
        raw_label = week_start.strftime("%d %b")
        day = raw_label.split()[0].lstrip("0")
        month = month_names.get(raw_label.split()[1], raw_label.split()[1])
        week_label = f"{day} {month}"
        
        # Filtrer les jobs de cette semaine
        mask = (df_dated['_date'] >= week_start) & (df_dated['_date'] <= week_end)
        week_jobs = df_dated[mask]
        
        weeks_data.append({
            'week_label': week_label,
            'count': len(week_jobs),
            'avg_score': week_jobs[COLUMNS["score"]].mean() if len(week_jobs) > 0 else 0,
            'applied_count': len(week_jobs[week_jobs[COLUMNS["statut"]] == "Postulé"]) if len(week_jobs) > 0 else 0
        })
    
    return pd.DataFrame(weeks_data)


def create_donut_chart(df: pd.DataFrame) -> go.Figure:
    """Donut chart pour la distribution des statuts."""
    status_counts = []
    status_labels = []
    colors = []
    
    for status in PIPELINE_ORDER:
        count = len(df[df[COLUMNS["statut"]] == status])
        if count > 0:
            status_counts.append(count)
            status_labels.append(status)
            colors.append(STATUS_CONFIG.get(status, {}).get("color", "#6B7280"))
    
    fig = go.Figure(data=[go.Pie(
        labels=status_labels,
        values=status_counts,
        hole=0.65,
        marker=dict(colors=colors),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value} jobs (%{percent})<extra></extra>'
    )])
    
    total = len(df)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='#94a3b8', size=10)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=40, l=10, r=10),
        height=220,
        annotations=[dict(
            text=f'<b>{total}</b><br><span style="font-size:11px">Total</span>',
            x=0.5, y=0.5,
            font=dict(size=24, color='#f8fafc'),
            showarrow=False,
        )]
    )
    
    return fig


def create_weekly_score_chart(df: pd.DataFrame) -> go.Figure:
    """Évolution du score moyen par semaine."""
    weekly = get_weekly_data(df)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly['week_label'],
        y=weekly['avg_score'],
        mode='lines+markers',
        line=dict(color='#a78bfa', width=3),
        marker=dict(size=8, color='#a78bfa'),
        fill='tozeroy',
        fillcolor='rgba(167, 139, 250, 0.15)',
        hovertemplate='<b>Semaine du %{x}</b><br>Score moyen: %{y:.1f}/10<extra></extra>'
    ))
    
    fig.add_hline(
        y=8, 
        line_dash="dash", 
        line_color="#4ade80",
        annotation_text="HP",
        annotation_position="right",
        annotation_font_color="#4ade80",
        annotation_font_size=10
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=30, l=35, r=10),
        height=180,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=9, color='#94a3b8'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#334155',
            tickfont=dict(size=10, color='#94a3b8'),
            range=[0, 10]
        ),
        hovermode='x unified',
        showlegend=False
    )
    
    return fig


def create_weekly_jobs_chart(df: pd.DataFrame) -> go.Figure:
    """Nombre de jobs scrappés par semaine."""
    weekly = get_weekly_data(df)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekly['week_label'],
        y=weekly['count'],
        marker=dict(color='#60a5fa', cornerradius=4),
        hovertemplate='<b>Semaine du %{x}</b><br>%{y} jobs<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=30, l=35, r=10),
        height=160,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=9, color='#94a3b8'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#334155',
            tickfont=dict(size=10, color='#94a3b8'),
        ),
        bargap=0.4,
        showlegend=False
    )
    
    return fig


def create_weekly_applications_chart(df: pd.DataFrame) -> go.Figure:
    """Nombre de candidatures envoyées par semaine."""
    weekly = get_weekly_data(df)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekly['week_label'],
        y=weekly['applied_count'],
        marker=dict(color='#4ade80', cornerradius=4),
        hovertemplate='<b>Semaine du %{x}</b><br>%{y} candidature(s)<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=30, l=35, r=10),
        height=160,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=9, color='#94a3b8'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#334155',
            tickfont=dict(size=10, color='#94a3b8'),
        ),
        bargap=0.4,
        showlegend=False
    )
    
    return fig


def render_kpi_card(icon: str, value, label: str, color: str):
    """Carte KPI dark theme."""
    st.markdown(f"""
        <div style="
            background: #1e293b;
            border-radius: 12px;
            padding: 1.25rem;
            border: 1px solid #334155;
            text-align: center;
        ">
            <div style="
                width: 42px;
                height: 42px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
                margin: 0 auto 0.75rem auto;
                background: {color}20;
            ">{icon}</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f8fafc;">{value}</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def get_score_badge_html(score: float) -> str:
    """Retourne le HTML du badge score en format /10."""
    if score >= 8:
        bg = "rgba(74, 222, 128, 0.15)"
        color = "#4ade80"
    elif score >= 5:
        bg = "rgba(251, 146, 60, 0.15)"
        color = "#fb923c"
    else:
        bg = "rgba(248, 113, 113, 0.15)"
        color = "#f87171"
    
    return f"""
        <div style="
            background: {bg};
            color: {color};
            padding: 0.4rem 0.6rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            text-align: center;
        ">{score:.0f}/10</div>
    """


def render_dashboard(df: pd.DataFrame) -> None:
    """Dashboard principal dark theme."""
    
    # === HEADER ===
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.25rem;">
                📊 Dashboard
            </h1>
            <p style="color: #64748b; font-size: 0.9rem;">
                Vue d'ensemble de vos candidatures
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # === KPIs ===
    total = len(df)
    to_analyze = len(df[df[COLUMNS["statut"]] == "À Analyser"])
    to_generate = len(df[df[COLUMNS["statut"]] == "Générer LM"])
    ready = len(df[df[COLUMNS["statut"]] == "Prêt"])
    applied = len(df[df[COLUMNS["statut"]] == "Postulé"])
    avg_score = df[COLUMNS["score"]].mean() if not df.empty else 0
    
    kpi_cols = st.columns(5)
    kpis = [
        ("📁", total, "Total Scrappés", "#a78bfa"),
        ("🔍", to_analyze, "À Analyser", "#fb923c"),
        ("✍️", to_generate, "LM à Générer", "#f472b6"),
        ("📤", ready, "Prêts", "#60a5fa"),
        ("✅", applied, "Postulés", "#4ade80"),
    ]
    
    for col, (icon, value, label, color) in zip(kpi_cols, kpis):
        with col:
            render_kpi_card(icon, value, label, color)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # === MAIN LAYOUT ===
    col_left, col_right = st.columns([1, 1.3])
    
    # --- LEFT: High Priority Jobs ---
    with col_left:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <span style="font-size: 1.1rem; font-weight: 600; color: #f8fafc;">🔥 High Priority</span>
                <span style="
                    background: linear-gradient(135deg, #a78bfa, #818cf8);
                    color: white;
                    padding: 0.25rem 0.6rem;
                    border-radius: 6px;
                    font-size: 0.65rem;
                    font-weight: 600;
                    text-transform: uppercase;
                ">Score \geq 8</span>
            </div>
        """, unsafe_allow_html=True)
        
        high_priority = df[
    (df[COLUMNS["score"]] >= SCORE_THRESHOLDS["high"]) & 
    (df[COLUMNS["statut"]] == "À Analyser")
].sort_values(COLUMNS["score"], ascending=False).head(5)
        
        if high_priority.empty:
            st.markdown("""
                <div style="
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    text-align: center; 
                    padding: 3rem 1rem;
                ">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📭</div>
                    <div style="color: #94a3b8; font-size: 0.95rem;">Aucun job haute priorité</div>
                    <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.35rem;">
                        Les jobs avec score \geq 8 apparaîtront ici
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for _, job in high_priority.iterrows():
                score = float(job[COLUMNS["score"]])
                poste = str(job[COLUMNS["poste"]])
                entreprise = str(job[COLUMNS["entreprise"]])
                location = str(job[COLUMNS["location"]]) if pd.notna(job[COLUMNS["location"]]) else ""
                status = str(job[COLUMNS["statut"]])
                job_id = job['id']
                
                status_cfg = STATUS_CONFIG.get(status, {"icon": "📋", "color": "#a78bfa"})
                
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{poste[:50]}{'...' if len(poste) > 50 else ''}**")
                        st.caption(f"🏢 {entreprise}")
                        if location:
                            st.caption(f"📍 {location}")
                    with c2:
                        st.markdown(get_score_badge_html(score), unsafe_allow_html=True)
                    
                    f1, f2 = st.columns([2, 1])
                    with f1:
                        st.markdown(f"""
                            <span style="
                                background: {status_cfg['color']}20;
                                color: {status_cfg['color']};
                                padding: 0.2rem 0.5rem;
                                border-radius: 5px;
                                font-size: 0.7rem;
                                font-weight: 600;
                            ">{status_cfg['icon']} {status}</span>
                        """, unsafe_allow_html=True)
                    with f2:
                        if st.button("Ouvrir →", key=f"open_{job_id}", use_container_width=True):
                            st.session_state.selected_job_id = job_id
                            st.session_state.current_page = "details"
                            st.rerun()
    
    # --- RIGHT: Charts ---
    with col_right:
        # Chart 1: Score moyen
        st.markdown("""
            <div style="margin-bottom: 0.35rem;">
                <span style="font-size: 0.95rem; font-weight: 600; color: #f8fafc;">📈 Évolution du Score Moyen</span>
                <span style="font-size: 0.75rem; color: #64748b; margin-left: 0.5rem;">Par semaine</span>
            </div>
        """, unsafe_allow_html=True)
        
        fig_score = create_weekly_score_chart(df)
        st.plotly_chart(fig_score, use_container_width=True, config={'displayModeBar': False})
        
        # Chart 2: Donut
        st.markdown("""
            <div style="margin-top: 0.75rem; margin-bottom: 0.35rem;">
                <span style="font-size: 0.95rem; font-weight: 600; color: #f8fafc;">🎯 Répartition des Statuts</span>
            </div>
        """, unsafe_allow_html=True)
        
        fig_donut = create_donut_chart(df)
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        
        # Two small charts
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">📥 Jobs Scrappés</span>
                </div>
            """, unsafe_allow_html=True)
            fig_jobs = create_weekly_jobs_chart(df)
            st.plotly_chart(fig_jobs, use_container_width=True, config={'displayModeBar': False})
        
        with chart_col2:
            st.markdown("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">✅ Candidatures</span>
                </div>
            """, unsafe_allow_html=True)
            fig_applied = create_weekly_applications_chart(df)
            st.plotly_chart(fig_applied, use_container_width=True, config={'displayModeBar': False})
        
        # Stats row
        stat_cols = st.columns(3)
        
        with stat_cols[0]:
            st.markdown(f"""
                <div style="
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    text-align: center; 
                    padding: 0.65rem;
                ">
                    <div style="color: #64748b; font-size: 0.65rem;">Score Moyen</div>
                    <div style="color: #a78bfa; font-size: 1.1rem; font-weight: 700;">{avg_score:.1f}/10</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stat_cols[1]:
            conversion = (applied / total * 100) if total > 0 else 0
            st.markdown(f"""
                <div style="
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    text-align: center; 
                    padding: 0.65rem;
                ">
                    <div style="color: #64748b; font-size: 0.65rem;">Conversion</div>
                    <div style="color: #4ade80; font-size: 1.1rem; font-weight: 700;">{conversion:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stat_cols[2]:
            hp_count = len(df[df[COLUMNS["score"]] >= 8])
            st.markdown(f"""
                <div style="
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    text-align: center; 
                    padding: 0.65rem;
                ">
                    <div style="color: #64748b; font-size: 0.65rem;">High Priority</div>
                    <div style="color: #f472b6; font-size: 1.1rem; font-weight: 700;">{hp_count}</div>
                </div>
            """, unsafe_allow_html=True)