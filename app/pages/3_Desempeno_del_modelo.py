"""Página de métricas y figuras del modelo."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).resolve().parent.parent))

from theme import ACCENT, MUTED, inject
from utils import figure_path, get_feature_order, load_model, load_processed_data

st.set_page_config(page_title="Desempeño del modelo", layout="wide")
inject()

st.markdown("<div class='eyebrow'>03 — Modelo</div>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top:0.1rem'>Desempeño del modelo</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p style='color:{MUTED}; max-width: 720px;'>Métricas calculadas sobre el 20% del dataset "
    "reservado para prueba (estratificado por clase, <code>random_state=42</code>).</p>",
    unsafe_allow_html=True,
)

model = load_model()
data = load_processed_data()
feature_order = get_feature_order(model)

X = data[feature_order]
y = data["political_orientation"]
_, X_te, _, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pred = model.predict(X_te)
proba = model.predict_proba(X_te)[:, 1]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Algoritmo", type(model).__name__)
c2.metric("Accuracy", f"{accuracy_score(y_te, pred)*100:.1f}%")
c3.metric("F1 Derecha", f"{f1_score(y_te, pred)*100:.1f}%")
c4.metric("Recall Derecha", f"{recall_score(y_te, pred)*100:.1f}%")
c5.metric("ROC-AUC", f"{roc_auc_score(y_te, proba):.3f}")

left, right = st.columns([1.1, 1])

with left:
    st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Reporte de clasificación</div>", unsafe_allow_html=True)
    report = classification_report(y_te, pred, target_names=["Izquierda", "Derecha"], output_dict=True)
    report_df = pd.DataFrame(report).T.round(3)
    st.dataframe(report_df, use_container_width=True)

with right:
    st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Probabilidades en test</div>", unsafe_allow_html=True)
    fig = px.histogram(
        x=proba, nbins=30, color_discrete_sequence=[ACCENT],
        labels={"x": "P(Derecha)"},
    )
    fig.update_layout(template="simple_white", height=320, margin=dict(l=10, r=10, t=10, b=10), bargap=0.02)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Figuras del entrenamiento</div>", unsafe_allow_html=True)

candidates = {
    "XGBClassifier": ("confusion_matrix_xgboost.png", "roc_curve_xgboost.png"),
    "RandomForestClassifier": (
        "confusion_matrix_optimized_random_forest.png",
        "roc_curve_optimized_random_forest.png",
    ),
    "GradientBoostingClassifier": (
        "confusion_matrix_gradient_boosting.png",
        "roc_curve_gradient_boosting.png",
    ),
    "DecisionTreeClassifier": (
        "confusion_matrix_decision_tree.png",
        "roc_curve_decision_tree.png",
    ),
    "LogisticRegression": (
        "confusion_matrix_logistic_regression.png",
        "roc_curve_logistic_regression.png",
    ),
}
cm_name, roc_name = candidates.get(type(model).__name__, ("", ""))

cols = st.columns(2)
cm_path = figure_path(cm_name)
roc_path = figure_path(roc_name)

if cm_path.exists():
    cols[0].image(str(cm_path), caption=f"Matriz de confusión — {type(model).__name__}", use_container_width=True)
else:
    cols[0].info("Matriz de confusión no disponible para este modelo.")

if roc_path.exists():
    cols[1].image(str(roc_path), caption=f"Curva ROC — {type(model).__name__}", use_container_width=True)
else:
    cols[1].info("Curva ROC no disponible para este modelo.")

st.markdown("<div class='eyebrow' style='margin-top:1.4rem'>Comparación entre modelos</div>", unsafe_allow_html=True)
cmp_cols = st.columns(2)
f1_cmp = figure_path("model_comparison_f1_score.png")
roc_cmp = figure_path("model_comparison_roc_auc.png")
if f1_cmp.exists():
    cmp_cols[0].image(str(f1_cmp), caption="F1 por modelo", use_container_width=True)
if roc_cmp.exists():
    cmp_cols[1].image(str(roc_cmp), caption="ROC-AUC por modelo", use_container_width=True)
