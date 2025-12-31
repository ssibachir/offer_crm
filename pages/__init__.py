"""Pages package."""
from pages.dashboard import render_dashboard
from pages.inbox import render_inbox
from pages.job_details import render_job_details
from pages.pipeline import render_pipeline

__all__ = ['render_dashboard', 'render_inbox', 'render_job_details', 'render_pipeline']