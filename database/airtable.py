"""
Module Airtable avec Date Scraping.
"""

import streamlit as st
import pandas as pd
from pyairtable import Api

from config.settings import COLUMNS


@st.cache_resource
def get_airtable_connection():
    """Connexion à Airtable."""
    try:
        API_KEY = st.secrets["airtable"]["api_key"]
        BASE_ID = st.secrets["airtable"]["base_id"]
        TABLE_NAME = st.secrets["airtable"]["table_name"]
        api = Api(API_KEY)
        return api.table(BASE_ID, TABLE_NAME)
    except (FileNotFoundError, KeyError):
        st.error("⚠️ Configuration Airtable manquante!")
        st.code('''[airtable]
api_key = "pat..."
base_id = "app..."
table_name = "Jobs"''', language="toml")
        st.stop()


@st.cache_data(ttl=60)
def load_jobs_data(_table) -> pd.DataFrame:
    """Charge les données depuis Airtable."""
    records = _table.all()
    
    if not records:
        return pd.DataFrame()
    
    data = [{"id": r["id"], **r["fields"]} for r in records]
    df = pd.DataFrame(data)
    
    # Valeurs par défaut
    defaults = {
        COLUMNS["statut"]: "À Analyser",
        COLUMNS["score"]: 0,
        COLUMNS["poste"]: "Non spécifié",
        COLUMNS["entreprise"]: "Non spécifiée",
        COLUMNS["description"]: "",
        COLUMNS["cover_letter"]: "",
        COLUMNS["url"]: "",
        COLUMNS["location"]: "",
        COLUMNS["contact"]: "",
        COLUMNS["contact_mail"]: "",
        COLUMNS["job_board"]: "",
        COLUMNS["relance"]: "",
        COLUMNS["date_candidature"]: None,
        COLUMNS["date_scraping"]: None,  # ✅ Ajouté
    }
    
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
    
    # Score en numérique
    df[COLUMNS["score"]] = pd.to_numeric(df[COLUMNS["score"]], errors='coerce').fillna(0)
    
    return df


def update_job(table, record_id: str, updates: dict) -> None:
    """Met à jour un job."""
    table.update(record_id, updates)
    st.cache_data.clear()


def delete_job(table, record_id: str) -> None:
    """Supprime un job."""
    table.delete(record_id)
    st.cache_data.clear()