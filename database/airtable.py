"""
Module de connexion et CRUD Airtable.
=====================================
Gère toutes les interactions avec la base Airtable.
"""

import streamlit as st
import pandas as pd
from pyairtable import Api

from config.settings import COLUMNS


@st.cache_resource
def get_airtable_connection():
    """
    Établit la connexion à Airtable via les secrets Streamlit.
    
    Returns:
        Table: Instance de la table Airtable
        
    Raises:
        SystemExit: Si la configuration est manquante
    """
    try:
        API_KEY = st.secrets["airtable"]["api_key"]
        BASE_ID = st.secrets["airtable"]["base_id"]
        TABLE_NAME = st.secrets["airtable"]["table_name"]
        api = Api(API_KEY)
        return api.table(BASE_ID, TABLE_NAME)
    except (FileNotFoundError, KeyError):
        st.error("⚠️ Configuration Airtable manquante!")
        st.code('''# .streamlit/secrets.toml
[airtable]
api_key = "pat..."
base_id = "app..."
table_name = "Jobs"''', language="toml")
        st.stop()


@st.cache_data(ttl=60)
def load_jobs_data(_table) -> pd.DataFrame:
    """
    Charge toutes les données depuis Airtable.
    
    Le underscore devant _table évite le hashing par Streamlit
    (les objets pyairtable ne sont pas hashables).
    
    Args:
        _table: Instance de la table Airtable
        
    Returns:
        pd.DataFrame: DataFrame avec toutes les offres d'emploi
    """
    records = _table.all()
    
    if not records:
        return pd.DataFrame()
    
    # Extraction des données
    data = [{"id": r["id"], **r["fields"]} for r in records]
    df = pd.DataFrame(data)
    
    # Valeurs par défaut pour colonnes manquantes
    defaults = {
        COLUMNS["statut"]: "A analyser",
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
        COLUMNS["est_postule"]: 0,
    }
    
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
    
    # Conversion score en numérique
    df[COLUMNS["score"]] = pd.to_numeric(df[COLUMNS["score"]], errors='coerce').fillna(0)
    
    return df


def update_job(table, record_id: str, updates: dict) -> None:
    """
    Met à jour un enregistrement Airtable.
    
    Args:
        table: Instance de la table Airtable
        record_id: ID de l'enregistrement
        updates: Dictionnaire {colonne: nouvelle_valeur}
    """
    table.update(record_id, updates)
    st.cache_data.clear()


def delete_job(table, record_id: str) -> None:
    """
    Supprime un enregistrement Airtable.
    
    Args:
        table: Instance de la table Airtable
        record_id: ID de l'enregistrement à supprimer
    """
    table.delete(record_id)
    st.cache_data.clear()