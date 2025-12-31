"""
Styles CSS personnalisés pour l'application.
============================================
Design moderne style SaaS dashboard.
"""

import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #F9FAFB;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #E5E7EB;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1F2937;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 0.875rem;
        color: #6B7280;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Job Cards */
    .job-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #E5E7EB;
        transition: all 0.2s ease;
    }
    
    .job-card:hover {
        border-color: #6366F1;
        box-shadow: 0 4px 12px rgba(99,102,241,0.15);
    }
    
    .job-card-title {
        font-weight: 600;
        color: #1F2937;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    .job-card-company {
        color: #6B7280;
        font-size: 0.875rem;
    }
    
    .job-card-location {
        color: #9CA3AF;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }
    
    /* Score Badges */
    .score-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .score-high { background: #DCFCE7; color: #166534; }
    .score-medium { background: #FEF3C7; color: #92400E; }
    .score-low { background: #FEE2E2; color: #991B1B; }
    
    /* Kanban */
    .kanban-column {
        background: #F3F4F6;
        border-radius: 12px;
        padding: 1rem;
        min-height: 400px;
    }
    
    .kanban-header {
        font-weight: 600;
        color: #374151;
        padding: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .kanban-count {
        background: #E5E7EB;
        color: #6B7280;
        padding: 0.125rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
    }
    
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 0.875rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid;
    }
    
    /* Misc */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .priority-badge {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .detail-panel {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #E5E7EB;
        height: 100%;
    }
    
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .info-item {
        background: #F9FAFB;
        padding: 0.75rem;
        border-radius: 8px;
    }
    
    .info-label {
        font-size: 0.75rem;
        color: #6B7280;
        margin-bottom: 0.25rem;
    }
    
    .info-value {
        font-weight: 500;
        color: #1F2937;
    }
</style>
"""


def inject_custom_css() -> None:
    """Injecte le CSS personnalisé dans l'application."""
    st.markdown(CSS, unsafe_allow_html=True)