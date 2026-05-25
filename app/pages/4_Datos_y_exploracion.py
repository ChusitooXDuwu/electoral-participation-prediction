"""Página de exploración de datos."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from features_metadata import FEATURES
from theme import ACCENT, ACCENT_ALT, MUTED, PRIMARY, inject
from utils import figure_path, load_processed_data

st.set_page_config(page_title="Datos y exploración", layout="wide")
inject()

st.markdown("<div class='eyebrow'>04 — Datos</div>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top:0.1rem'>Datos y exploración</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p style='color:{MUTED}; max-width: 720px;'>Composición del dataset procesado y "
    "exploración interactiva de cada variable contra la orientación política.</p>",
    unsafe_allow_html=True,
)

data = load_processed_data()

left_n = int((data["political_orientation"] == 0).sum())
right_n = int((data["political_orientation"] == 1).sum())

c1, c2, c3 = st.columns(3)
c1.metric("Observaciones", f"{len(data):,}")
c2.metric("Izquierda (0)", f"{left_n:,} · {left_n/len(data)*100:.1f}%")
c3.metric("Derecha (1)", f"{right_n:,} · {right_n/len(data)*100:.1f}%")

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Variable objetivo</div>", unsafe_allow_html=True)
target_df = pd.DataFrame({
    "Orientación": ["Izquierda", "Derecha"],
    "Frecuencia": [left_n, right_n],
})
fig = px.bar(
    target_df, x="Orientación", y="Frecuencia",
    color="Orientación",
    color_discrete_map={"Izquierda": ACCENT_ALT, "Derecha": ACCENT},
    text="Frecuencia",
)
fig.update_layout(template="simple_white", height=340, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Explorador por variable</div>", unsafe_allow_html=True)
feature_codes = [c for c in data.columns if c != "political_orientation"]
labels_map = {c: f"{c} — {FEATURES.get(c, {}).get('label', '')}" for c in feature_codes}
selected = st.selectbox("Variable", options=feature_codes, format_func=lambda c: labels_map[c])

meta = FEATURES.get(selected, {})
opts = meta.get("options")

vc = data[selected].value_counts().sort_index().reset_index()
vc.columns = ["valor", "frecuencia"]
if opts:
    vc["etiqueta"] = vc["valor"].map(lambda v: opts.get(int(v), str(v)))
else:
    vc["etiqueta"] = vc["valor"].astype(str)

fig2 = px.bar(
    vc, x="etiqueta", y="frecuencia", text="frecuencia",
    color_discrete_sequence=[PRIMARY],
)
fig2.update_layout(template="simple_white", height=360, xaxis_title="", yaxis_title="Frecuencia",
                   margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='small-caption' style='margin-top:-0.6rem'>Distribución por orientación política</div>", unsafe_allow_html=True)
cross = data.groupby([selected, "political_orientation"]).size().reset_index(name="frecuencia")
cross["Orientación"] = cross["political_orientation"].map({0: "Izquierda", 1: "Derecha"})
if opts:
    cross["etiqueta"] = cross[selected].map(lambda v: opts.get(int(v), str(v)))
else:
    cross["etiqueta"] = cross[selected].astype(str)
fig3 = px.bar(
    cross, x="etiqueta", y="frecuencia", color="Orientación", barmode="group",
    color_discrete_map={"Izquierda": ACCENT_ALT, "Derecha": ACCENT},
)
fig3.update_layout(template="simple_white", height=360, xaxis_title="", yaxis_title="Frecuencia",
                   margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Figuras del análisis exploratorio</div>", unsafe_allow_html=True)
eda_figs = [
    ("distribucionOgPosicionIdeologica.png", "Distribución original de P5328 (escala 1–10)"),
    ("distribucionIdeologicaSinCentralesNoValidas.png", "Distribución sin valores centrales ni no-respuestas"),
    ("distribucibinariaOrientaciPoltica.png", "Distribución binaria final"),
    ("americas_barometer_scale.png", "Escala del Barómetro de las Américas"),
]
cols = st.columns(2)
for i, (fname, caption) in enumerate(eda_figs):
    p = figure_path(fname)
    if p.exists():
        cols[i % 2].image(str(p), caption=caption, use_container_width=True)
