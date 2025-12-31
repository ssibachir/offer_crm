"""
Configuration centralisée de l'application.
============================================
Contient toutes les constantes et mappings utilisés dans l'app.
"""

# Application metadata
APP_CONFIG = {
    "title": "Job Hunter CRM",
    "icon": "🎯",
    "layout": "wide",
    "version": "2.0.0",
}

# Palette de couleurs SaaS moderne
COLORS = {
    "primary": "#6366F1",      # Indigo
    "secondary": "#8B5CF6",    # Purple
    "success": "#10B981",      # Emerald
    "warning": "#F59E0B",      # Amber
    "danger": "#EF4444",       # Red
    "info": "#3B82F6",         # Blue
    "dark": "#1F2937",         # Gray 800
    "light": "#F9FAFB",        # Gray 50
    "muted": "#6B7280",        # Gray 500
}

# Configuration des statuts avec couleurs et icônes
STATUS_CONFIG = {
    "À Analyser": {
        "color": "#F59E0B",
        "icon": "🔍",
        "order": 1,
        "description": "Nouveau job à examiner"
    },
    "Générer LM": {
        "color": "#8B5CF6",
        "icon": "✍️",
        "order": 2,
        "description": "Lettre de motivation à créer"
    },
    "Pret": {
        "color": "#3B82F6",
        "icon": "📤",
        "order": 3,
        "description": "Prêt à être envoyé"
    },
    "Postulé": {
        "color": "#10B981",
        "icon": "✅",
        "order": 4,
        "description": "Candidature envoyée"
    },
    "Refus": {
        "color": "#EF4444",
        "icon": "❌",
        "order": 5,
        "description": "Candidature refusée"
    },
}

# Mapping des colonnes Airtable vers noms internes
COLUMNS = {
    "poste": "Poste",
    "entreprise": "Entreprise",
    "location": "Location",
    "url": "URL Offre",
    "description": "Description",
    "date_candidature": "Date de Candidature",
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

# Ordre des statuts pour le pipeline Kanban
PIPELINE_ORDER = ["À Analyser", "Générer LM", "Prêt", "Postulé", "Refus"]

# Seuils de score
SCORE_THRESHOLDS = {
    "high": 8,
    "medium": 5,
}