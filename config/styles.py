"""
Styles CSS - Dark Theme Moderne.
================================
Inspiré de UX Stdio avec glassmorphism et accents colorés.
"""

import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #1e293b;
        --bg-card-hover: #334155;
        --border-color: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-purple: #a78bfa;
        --accent-blue: #60a5fa;
        --accent-pink: #f472b6;
        --accent-green: #4ade80;
        --accent-orange: #fb923c;
        --accent-red: #f87171;
        --gradient-purple: linear-gradient(135deg, #a78bfa, #818cf8);
        --gradient-blue: linear-gradient(135deg, #60a5fa, #38bdf8);
        --gradient-pink: linear-gradient(135deg, #f472b6, #e879f9);
    }
    
    /* ===== HIDE STREAMLIT DEFAULT NAVIGATION ===== */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"] * {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* ===== FORCE SIDEBAR ALWAYS VISIBLE ===== */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        position: relative !important;
        transform: translateX(0) !important;
        min-width: 280px !important;
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    /* ===== HIDE ONLY SIDEBAR COLLAPSE BUTTON ===== */
    button[data-testid="baseButton-header"],
    button[data-testid="collapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* ===== GLOBAL ===== */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    #MainMenu, footer, header {
        visibility: hidden;
        display: none;
    }
    
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1600px;
        background: var(--bg-primary);
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    
    /* ===== SIDEBAR DARK ===== */
    section[data-testid="stSidebar"] > div {
        background: var(--bg-secondary);
        padding-top: 1rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-color);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        text-align: left;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: var(--bg-card-hover);
        color: var(--text-primary);
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: var(--gradient-purple);
        color: white;
    }
    
    /* ===== KPI CARDS DARK ===== */
    .kpi-card-dark {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .kpi-card-dark:hover {
        border-color: var(--accent-purple);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(167, 139, 250, 0.15);
    }
    
    .kpi-icon-dark {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .kpi-value-dark {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .kpi-label-dark {
        font-size: 0.8rem;
        color: var(--text-muted);
        font-weight: 500;
    }
    
    /* ===== GLASSMORPHISM CARD ===== */
    .glass-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .chart-subtitle {
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    /* ===== JOB CARD DARK ===== */
    .job-card-dark {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 1px solid var(--border-color);
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .job-card-dark:hover {
        background: var(--bg-card-hover);
        border-color: var(--accent-purple);
    }
    
    .job-title-dark {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.35rem;
    }
    
    .job-company-dark {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 0.25rem;
    }
    
    .job-location-dark {
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    /* ===== SCORE BADGES DARK ===== */
    .score-badge-dark {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    
    .score-high-dark {
        background: rgba(74, 222, 128, 0.15);
        color: var(--accent-green);
    }
    
    .score-medium-dark {
        background: rgba(251, 146, 60, 0.15);
        color: var(--accent-orange);
    }
    
    .score-low-dark {
        background: rgba(248, 113, 113, 0.15);
        color: var(--accent-red);
    }
    
    /* ===== STATUS BADGE DARK ===== */
    .status-badge-dark {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        background: rgba(167, 139, 250, 0.15);
        color: var(--accent-purple);
    }
    
    /* ===== SECTION HEADER DARK ===== */
    .section-header-dark {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-badge {
        background: var(--gradient-purple);
        color: white;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== STAT ROW DARK ===== */
    .stat-row-dark {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .stat-row-dark:last-child {
        border-bottom: none;
    }
    
    .stat-label-dark {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .stat-value-dark {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* ===== PROGRESS BAR DARK ===== */
    .progress-container-dark {
        background: var(--bg-primary);
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .progress-fill-dark {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* ===== BUTTONS DARK - LARGER ===== */
    .stButton > button {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background: var(--bg-card-hover);
        border-color: var(--accent-purple);
    }
    
    .stButton > button[kind="primary"] {
        background: var(--gradient-purple);
        border: none;
        color: white;
    }
    
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    
    /* ===== INPUTS DARK ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-purple);
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
    }
    
    /* ===== SLIDER DARK ===== */
    .stSlider > div > div > div > div {
        background: var(--accent-purple);
    }
    
    .stSlider > div > div > div > div > div {
        background: var(--accent-purple);
    }
    
    /* ===== METRICS DARK ===== */
    div[data-testid="stMetric"] {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }
    
    div[data-testid="stMetric"] label {
        color: var(--text-muted);
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--text-primary);
    }
    
    /* ===== CONTAINERS DARK - LARGER CARDS ===== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #475569 !important;
    }
    
    /* ===== SUCCESS/INFO/WARNING ===== */
    .stAlert {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
    }
    
    /* ===== EXPANDER DARK ===== */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    /* ===== CAPTIONS - LARGER ===== */
    .stCaption {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
    }
    
    /* ===== MARKDOWN ===== */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    /* ===== TABLE DARK ===== */
    .table-dark {
        width: 100%;
        border-collapse: collapse;
    }
    
    .table-dark th {
        text-align: left;
        padding: 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        border-bottom: 1px solid var(--border-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .table-dark td {
        padding: 0.75rem;
        font-size: 0.85rem;
        color: var(--text-primary);
        border-bottom: 1px solid var(--border-color);
    }
    
    .table-dark tr:hover td {
        background: var(--bg-card-hover);
    }
    
    /* ===== PIPELINE / KANBAN STYLES ===== */
    .pipeline-column {
        background: var(--bg-primary);
        border-radius: 12px;
        padding: 0.5rem;
        min-height: 500px;
    }
    
    .kanban-column-header {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .kanban-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 0.85rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .kanban-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--accent-purple);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.15);
    }
    
    .kanban-card-bordered {
        border-left: 3px solid;
    }
    
    .kanban-card-company {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.35rem;
    }
    
    .kanban-card-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.3;
    }
    
    .kanban-card-location {
        font-size: 0.7rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }
    
    .column-empty {
        background: rgba(30, 41, 59, 0.4);
        border: 1px dashed var(--border-color);
        border-radius: 8px;
        padding: 2rem 1rem;
        text-align: center;
        color: var(--text-muted);
    }
    
    /* ===== INBOX STYLES ===== */
    .inbox-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .inbox-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--accent-purple);
    }
    
    /* ===== JOB DETAILS STYLES ===== */
    .detail-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    }
    
    .detail-section-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .detail-info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .detail-info-item {
        background: var(--bg-primary);
        padding: 0.75rem;
        border-radius: 8px;
    }
    
    .detail-info-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }
    
    .detail-info-value {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .description-box {
        background: var(--bg-primary);
        border-radius: 8px;
        padding: 1rem;
        max-height: 300px;
        overflow-y: auto;
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
    }
</style>
"""


def inject_custom_css() -> None:
    """Injecte le CSS dark theme moderne."""
    st.markdown(CSS, unsafe_allow_html=True)