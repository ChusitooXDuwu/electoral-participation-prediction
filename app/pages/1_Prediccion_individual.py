"""Formulario guiado para una predicción individual + explicación SHAP."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import shap
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from features_metadata import FEATURES, get_default_row, get_sections
from theme import ACCENT, ACCENT_ALT, MUTED, PRIMARY, inject
from utils import LABEL_MAP, get_feature_order, load_model, predict_with_proba

st.set_page_config(page_title="Predicción individual", layout="wide")
inject()

st.markdown("<div class='eyebrow'>01 — Predicción</div>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top:0.1rem'>Predicción individual</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p style='color:{MUTED}; max-width: 720px;'>Responde las preguntas agrupadas por tema "
    "para obtener la estimación de orientación política. Todos los campos tienen valores por defecto.</p>",
    unsafe_allow_html=True,
)

model = load_model()
feature_order = get_feature_order(model)

sections = get_sections()

with st.form("predict_form", border=False):
    defaults = get_default_row()
    responses: dict[str, float] = {}

    for section_name, codes in sections.items():
        if not codes:
            continue
        with st.expander(section_name, expanded=(section_name == "Demografía")):
            cols = st.columns(2)
            for i, code in enumerate(codes):
                meta = FEATURES[code]
                options = meta["options"]
                default = defaults[code]
                with cols[i % 2]:
                    if options is None:
                        responses[code] = st.number_input(
                            meta["label"], value=float(default), key=f"in_{code}"
                        )
                    else:
                        keys = list(options.keys())
                        default_idx = keys.index(default) if default in keys else 0
                        choice = st.selectbox(
                            meta["label"],
                            options=keys,
                            index=default_idx,
                            format_func=lambda v, m=options: m[v],
                            key=f"in_{code}",
                        )
                        responses[code] = float(choice)

    submitted = st.form_submit_button(
        "Generar predicción", type="primary", use_container_width=True
    )

if submitted:
    row = pd.DataFrame([{c: responses[c] for c in feature_order}])
    pred, proba = predict_with_proba(model, row)
    pred_class = int(pred[0])
    p_right = float(proba[0])
    label = LABEL_MAP[pred_class]
    color = ACCENT if pred_class == 1 else ACCENT_ALT

    st.divider()
    st.markdown("<div class='eyebrow'>Resultado</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1.3])

    with col_a:
        st.markdown(
            f"""
            <div class="result-banner" style="--accent:{color};">
                <div style="color:{MUTED}; font-size:0.82rem; text-transform:uppercase; letter-spacing:0.06em;">
                    Clase predicha
                </div>
                <div style="font-size:2rem; font-weight:600; color:{color}; margin-top:0.2rem;">{label}</div>
                <div style="margin-top:0.8rem; color:{PRIMARY}; font-size:0.95rem;">
                    P(Derecha) = <b>{p_right*100:.1f}%</b><br/>
                    P(Izquierda) = <b>{(1-p_right)*100:.1f}%</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        bar = go.Figure()
        bar.add_trace(go.Bar(
            x=[(1 - p_right) * 100], y=[""], orientation="h",
            marker=dict(color=ACCENT_ALT), name="Izquierda",
            hovertemplate="Izquierda: %{x:.1f}%<extra></extra>",
        ))
        bar.add_trace(go.Bar(
            x=[p_right * 100], y=[""], orientation="h",
            marker=dict(color=ACCENT), name="Derecha",
            hovertemplate="Derecha: %{x:.1f}%<extra></extra>",
        ))
        bar.update_layout(
            barmode="stack",
            height=140,
            margin=dict(l=10, r=10, t=30, b=10),
            template="simple_white",
            showlegend=True,
            legend=dict(orientation="h", x=0, y=1.25),
            xaxis=dict(range=[0, 100], ticksuffix="%", showgrid=False),
            yaxis=dict(showticklabels=False),
        )
        st.plotly_chart(bar, use_container_width=True)

    st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Variables más influyentes</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='small-caption'>Barras a la derecha empujan la predicción hacia "
        "<b style='color:" + ACCENT + ";'>Derecha</b>; a la izquierda, hacia "
        "<b style='color:" + ACCENT_ALT + ";'>Izquierda</b>. Se muestran las 12 con mayor impacto.</p>",
        unsafe_allow_html=True,
    )

    try:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer(row, check_additivity=False)
        values = shap_vals.values
        if values.ndim == 3:
            values = values[:, :, 1]

        contrib = pd.DataFrame({
            "feature": row.columns,
            "value": row.iloc[0].values,
            "shap": values[0],
        })
        contrib["abs"] = contrib["shap"].abs()
        contrib = contrib.sort_values("abs", ascending=False).head(12).iloc[::-1]
        contrib["label"] = contrib["feature"].map(lambda c: FEATURES.get(c, {}).get("label", c))
        contrib["value_label"] = contrib.apply(
            lambda r: (FEATURES.get(r["feature"], {}).get("options") or {}).get(int(r["value"]), str(r["value"])),
            axis=1,
        )
        contrib["display"] = contrib["label"] + " — " + contrib["value_label"].astype(str)
        contrib["color"] = np.where(contrib["shap"] > 0, ACCENT, ACCENT_ALT)

        fig2 = go.Figure(
            go.Bar(
                x=contrib["shap"],
                y=contrib["display"],
                orientation="h",
                marker=dict(color=contrib["color"]),
                text=[f"{v:+.3f}" for v in contrib["shap"]],
                textposition="outside",
            )
        )
        fig2.update_layout(
            height=480,
            margin=dict(l=10, r=80, t=10, b=20),
            xaxis_title="Contribución SHAP a P(Derecha)",
            yaxis_title="",
            template="simple_white",
        )
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as exc:
        st.warning(f"No fue posible generar la explicación SHAP: {exc}")
