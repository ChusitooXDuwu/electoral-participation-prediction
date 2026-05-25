"""Estilos globales reutilizados por todas las páginas."""

import streamlit as st

PRIMARY = "#0f172a"      # near-black navy
ACCENT = "#1d4ed8"       # right
ACCENT_ALT = "#b91c1c"   # left
MUTED = "#475569"
BORDER = "#e2e8f0"
SUBTLE_BG = "#f8fafc"


CSS = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"]  {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  }}

  /* Heading weight & tracking */
  h1, h2, h3, h4 {{
    letter-spacing: -0.015em;
    color: {PRIMARY};
  }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
    background: {SUBTLE_BG};
    border-right: 1px solid {BORDER};
  }}
  section[data-testid="stSidebar"] .stRadio label,
  section[data-testid="stSidebar"] a {{
    font-size: 0.92rem;
  }}

  /* Compact metric cards */
  div[data-testid="stMetric"] {{
    background: white;
    border: 1px solid {BORDER};
    padding: 0.9rem 1rem;
    border-radius: 10px;
  }}
  div[data-testid="stMetricLabel"] {{
    color: {MUTED};
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  div[data-testid="stMetricValue"] {{
    font-size: 1.6rem;
    font-weight: 600;
  }}

  /* Buttons */
  .stButton > button, .stDownloadButton > button {{
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid {BORDER};
  }}
  .stButton > button[kind="primary"] {{
    background: {PRIMARY};
    color: white;
    border-color: {PRIMARY};
  }}
  .stButton > button[kind="primary"]:hover {{
    background: #1e293b;
    border-color: #1e293b;
  }}

  /* Expander */
  details summary {{
    font-weight: 600 !important;
  }}

  /* Caption tweak */
  .small-caption {{
    color: {MUTED};
    font-size: 0.85rem;
  }}

  /* Generic card */
  .card {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
    background: white;
    height: 100%;
  }}
  .card-title {{
    font-weight: 600;
    color: {PRIMARY};
    margin-bottom: 0.25rem;
  }}
  .card-body {{
    color: {MUTED};
    font-size: 0.9rem;
  }}

  /* Section eyebrow */
  .eyebrow {{
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
  }}

  /* Result banner */
  .result-banner {{
    border: 1px solid {BORDER};
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    background: white;
  }}

  /* Streamlit default footer hide */
  footer {{ visibility: hidden; }}
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
