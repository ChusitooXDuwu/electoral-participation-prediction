"""Predicción por lotes (CSV)."""

import io
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from theme import ACCENT, MUTED, inject
from utils import BASE_DIR, LABEL_MAP, get_feature_order, load_model, predict_with_proba

st.set_page_config(page_title="Predicción por lotes", layout="wide")
inject()

st.markdown("<div class='eyebrow'>02 — Predicción</div>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top:0.1rem'>Predicción por lotes</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p style='color:{MUTED}; max-width: 720px;'>Sube un archivo CSV con las 73 variables de la "
    "ECP 2023 y descarga el resultado con la clase y probabilidad predicha.</p>",
    unsafe_allow_html=True,
)

model = load_model()
feature_order = get_feature_order(model)

with st.expander("Formato esperado y archivo de muestra", expanded=False):
    st.markdown(
        f"""
- El archivo debe contener las **{len(feature_order)} columnas** con los códigos originales de la ECP.
- Pueden venir en cualquier orden y pueden incluir columnas adicionales (serán ignoradas).
- Los valores deben ser numéricos según el cuestionario (1, 2, 99, etc.).
        """
    )

    sample_path = BASE_DIR / "data" / "sample_batch.csv"
    plantilla = pd.DataFrame([{c: 1 for c in feature_order}])

    col1, col2 = st.columns(2)
    if sample_path.exists():
        col1.download_button(
            "Descargar archivo de muestra (20 filas reales)",
            data=sample_path.read_bytes(),
            file_name="sample_batch.csv",
            mime="text/csv",
        )
    col2.download_button(
        "Descargar plantilla vacía",
        data=plantilla.to_csv(index=False).encode("utf-8"),
        file_name="plantilla_ecp.csv",
        mime="text/csv",
    )

uploaded = st.file_uploader("Archivo CSV", type=["csv"])

if uploaded is None:
    st.caption("Esperando archivo.")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"No se pudo leer el CSV: {exc}")
    st.stop()

missing = [c for c in feature_order if c not in df.columns]
if missing:
    st.error(
        f"Faltan {len(missing)} columnas requeridas. Ejemplo: "
        + ", ".join(missing[:8]) + ("…" if len(missing) > 8 else "")
    )
    st.stop()

X = df[feature_order].copy()
n_nan = int(X.isna().sum().sum())
if n_nan > 0:
    st.warning(
        f"Se detectaron {n_nan} valores faltantes. Se imputan con la moda por columna."
    )
    X = X.fillna(X.mode().iloc[0])

pred, proba = predict_with_proba(model, X)
out = df.copy()
out["pred_class"] = pred
out["pred_label"] = [LABEL_MAP[c] for c in pred]
out["prob_derecha"] = proba.round(4)
out["prob_izquierda"] = (1 - proba).round(4)

c1, c2, c3 = st.columns(3)
c1.metric("Filas procesadas", f"{len(out):,}")
c2.metric("% Derecha", f"{(pred == 1).mean()*100:.1f}%")
c3.metric("% Izquierda", f"{(pred == 0).mean()*100:.1f}%")

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Distribución de probabilidades</div>", unsafe_allow_html=True)
fig = px.histogram(
    out, x="prob_derecha", nbins=30,
    color_discrete_sequence=[ACCENT],
    labels={"prob_derecha": "P(Derecha)"},
)
fig.update_layout(template="simple_white", height=300, margin=dict(l=10, r=10, t=10, b=10), bargap=0.02)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Vista previa</div>", unsafe_allow_html=True)
st.dataframe(
    out[["pred_label", "prob_derecha", "prob_izquierda"] + feature_order[:6]].head(20),
    use_container_width=True,
    height=380,
)

buf = io.BytesIO()
out.to_csv(buf, index=False)
st.download_button(
    "Descargar CSV con predicciones",
    data=buf.getvalue(),
    file_name="predicciones.csv",
    mime="text/csv",
    type="primary",
)
