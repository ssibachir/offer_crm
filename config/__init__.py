"""Configuration package."""
from config.settings import APP_CONFIG, COLORS, STATUS_CONFIG, COLUMNS
from config.styles import inject_custom_css

__all__ = ['APP_CONFIG', 'COLORS', 'STATUS_CONFIG', 'COLUMNS', 'inject_custom_css']