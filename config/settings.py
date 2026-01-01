"""
Configuration centralisée.
"""

APP_CONFIG = {
    "title": "Job Hunter CRM",
    "icon": "🎯",
    "layout": "wide",
    "version": "2.0.0",
}

COLORS = {
    "primary": "#6366F1",
    "secondary": "#8B5CF6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "dark": "#1F2937",
    "light": "#F9FAFB",
    "muted": "#6B7280",
}

STATUS_CONFIG = {
    "À Analyser": {
        "color": "#F59E0B",
        "icon": "🔍",
        "order": 1,
    },
    "Générer LM": {
        "color": "#8B5CF6",
        "icon": "✍️",
        "order": 2,
    },
    "Prêt": {
        "color": "#3B82F6",
        "icon": "📤",
        "order": 3,
    },
    "Postulé": {
        "color": "#10B981",
        "icon": "✅",
        "order": 4,
    },
    "Refus": {
        "color": "#EF4444",
        "icon": "❌",
        "order": 5,
    },
}

# Mapping des colonnes Airtable
COLUMNS = {
    "poste": "Poste",
    "entreprise": "Entreprise",
    "location": "Location",
    "url": "URL Offre",
    "description": "Description",
    "date_candidature": "Date de Candidature",
    "date_scraping": "Date Scraping",  # ✅ Nouvelle colonne
    "cover_letter": "Cover letter",
    "score": "Score Match",
    "statut": "Statut",
    "a_analyser": "À Analyser",
    "est_postule": "Est Postulé",
    "contact": "Contact",
    "relance": "Relance",
    "job_board": "Job board",
    "contact_mail": "contact mail",
}

PIPELINE_ORDER = ["À Analyser", "Générer LM", "Prêt", "Postulé", "Refus"]

SCORE_THRESHOLDS = {
    "high": 8,
    "medium": 5,
}

DEFAULT_STATUS = "À Analyser"