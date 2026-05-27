"""
Página de inicio.

Ejecutar localmente:
    streamlit run app/streamlit_app.py
"""

import subprocess
from datetime import datetime
from pathlib import Path

import streamlit as st

from theme import inject, PRIMARY, MUTED
from utils import BASE_DIR, load_model, load_processed_data


@st.cache_data(show_spinner=False)
def _build_info() -> dict:
    """Return the short SHA and date of the current commit, if available."""
    try:
        sha = subprocess.check_output(
            ["git", "-C", str(BASE_DIR), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
        date = subprocess.check_output(
            ["git", "-C", str(BASE_DIR), "log", "-1", "--format=%cs", "HEAD"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
        return {"sha": sha, "date": date}
    except Exception:
        return {"sha": "unknown", "date": datetime.utcnow().strftime("%Y-%m-%d")}

st.set_page_config(
    page_title="Orientación Política · ECP 2023",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject()


def _hero():
    st.markdown(
        f"""
        <div style="margin-top: 0.5rem;">
            <div class="eyebrow">Encuesta de Cultura Política 2023 · DANE</div>
            <h1 style="margin: 0.1rem 0 0.4rem; font-weight: 600; font-size: 2.1rem;">
                Predicción de orientación política
            </h1>
            <p style="color:{MUTED}; max-width: 720px; font-size: 1rem; line-height: 1.55;">
                Modelo de clasificación binaria que estima la inclinación
                ideológica (izquierda o derecha) de una persona a partir de sus
                respuestas en la ECP 2023.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _kpi_cards(model, data):
    n_rows = len(data)
    n_features = model.n_features_in_
    left_pct = (data["political_orientation"] == 0).mean() * 100
    right_pct = (data["political_orientation"] == 1).mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algoritmo", type(model).__name__)
    c2.metric("Variables", f"{n_features}")
    c3.metric("Observaciones", f"{n_rows:,}")
    c4.metric("Izq / Der", f"{left_pct:.0f}% / {right_pct:.0f}%")


def _section_cards():
    st.markdown("<div class='eyebrow' style='margin-top:1.2rem'>Secciones</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    items = [
        ("01", "Predicción individual",
         "Formulario guiado para estimar la orientación política de una persona."),
        ("02", "Predicción por lotes",
         "Carga un CSV con las 73 variables y descarga el archivo con predicciones."),
        ("03", "Desempeño del modelo",
         "Métricas, matriz de confusión y curva ROC sobre el conjunto de prueba."),
        ("04", "Datos y exploración",
         "Distribución de la variable objetivo y explorador por variable."),
    ]
    for col, (num, title, body) in zip(cols, items):
        col.markdown(
            f"""
            <div class="card">
                <div style="color:{MUTED}; font-size:0.78rem; letter-spacing:0.08em;">{num}</div>
                <div class="card-title" style="margin-top:0.3rem">{title}</div>
                <div class="card-body" style="margin-top:0.3rem">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _about():
    st.markdown("<div class='eyebrow' style='margin-top:1.6rem'>Metodología</div>", unsafe_allow_html=True)
    st.markdown(
        """
La variable objetivo `political_orientation` se deriva de la pregunta P5328
(autoubicación ideológica en escala 1–10) siguiendo la convención del
Barómetro de las Américas (LAPOP):

- Izquierda (0): P5328 ∈ {1, 2, 3, 4}
- Derecha (1): P5328 ∈ {7, 8, 9, 10}
- Se excluyen los valores centrales (5, 6) y las no-respuestas (98, 99).

El modelo utiliza 73 variables sobre demografía, confianza institucional,
participación electoral y cívica, valores sociales y consumo de información política.
        """
    )
    st.info(
        "Las predicciones son probabilísticas. Úselas como referencia agregada, "
        "no como diagnóstico individual.",
        icon=None,
    )


def main():
    _hero()
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    model = load_model()
    data = load_processed_data()

    _kpi_cards(model, data)
    _section_cards()
    _about()

    st.divider()
    info = _build_info()
    st.markdown(
        f"<div class='small-caption'>Fuente: DANE — Encuesta de Cultura Política 2023. "
        f"Modelo: <code>app/best_model.pkl</code>. "
        f"Build <code>{info['sha']}</code> · {info['date']}.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
