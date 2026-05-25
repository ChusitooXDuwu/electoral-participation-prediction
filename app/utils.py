"""Helpers compartidos por las páginas de la app."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "app" / "best_model.pkl"
DATA_PATH = BASE_DIR / "data" / "processed" / "political_orientation_clean.csv"
FIGURES_DIR = BASE_DIR / "figures"


@st.cache_resource(show_spinner=False)
def load_model():
    if not MODEL_PATH.exists():
        st.error(
            f"No se encontró el modelo en `{MODEL_PATH}`. "
            "Ejecute el notebook `03_model_training.ipynb` primero."
        )
        st.stop()
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_processed_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error(
            f"No se encontró el dataset procesado en `{DATA_PATH}`. "
            "Ejecute el notebook `02_data_preprocessing.ipynb` primero."
        )
        st.stop()
    return pd.read_csv(DATA_PATH)


def get_feature_order(model):
    if hasattr(model, "feature_names_in_"):
        return [str(c) for c in model.feature_names_in_]
    data = load_processed_data()
    return [c for c in data.columns if c != "political_orientation"]


def figure_path(name: str) -> Path:
    return FIGURES_DIR / name


def predict_with_proba(model, X: pd.DataFrame):
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= 0.5).astype(int)
    return pred, proba


LABEL_MAP = {0: "Izquierda", 1: "Derecha"}
COLOR_MAP = {0: "#d62828", 1: "#1d4ed8"}
