"""Helpers compartidos por las páginas de la app."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "app" / "best_model.pkl"
DATA_PATH = BASE_DIR / "data" / "processed" / "political_orientation_clean.csv"
FIGURES_DIR = BASE_DIR / "figures"


def _ensure_model_exists():
    if not MODEL_PATH.exists():
        st.error(
            f"No se encontró el modelo en `{MODEL_PATH}`. "
            "Ejecute el notebook `03_model_training.ipynb` primero."
        )
        st.stop()


@st.cache_resource(show_spinner=False)
def _load_bundle():
    _ensure_model_exists()
    raw = joblib.load(MODEL_PATH)

    # El pickle puede ser:
    #   - dict con keys {'model', 'selected_features', 'shap_importance'} (formato actual)
    #   - el estimator directo (formato previo)
    if isinstance(raw, dict) and "model" in raw:
        model = raw["model"]
        selected = list(raw.get("selected_features") or getattr(model, "feature_names_in_", []))
        shap_importance = raw.get("shap_importance")
    else:
        model = raw
        selected = list(getattr(model, "feature_names_in_", []))
        shap_importance = None

    selected = [str(c) for c in selected]
    return model, selected, shap_importance


def load_model():
    """Compatibilidad con el código previo: devuelve solo el estimator."""
    model, _, _ = _load_bundle()
    return model


def load_selected_features() -> list[str]:
    """Lista de columnas que el modelo realmente usa."""
    _, selected, _ = _load_bundle()
    return selected


def load_shap_importance() -> pd.DataFrame | None:
    """DataFrame con importancia SHAP global (feature, mean_abs_shap), o None."""
    _, _, shap_imp = _load_bundle()
    return shap_imp


@st.cache_data(show_spinner=False)
def load_processed_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error(
            f"No se encontró el dataset procesado en `{DATA_PATH}`. "
            "Ejecute el notebook `02_data_preprocessing.ipynb` primero."
        )
        st.stop()
    return pd.read_csv(DATA_PATH)


def get_feature_order(model=None) -> list[str]:
    """Orden de columnas que espera el modelo (subset seleccionado)."""
    return load_selected_features()


def figure_path(name: str) -> Path:
    return FIGURES_DIR / name


def predict_with_proba(model, X: pd.DataFrame):
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= 0.5).astype(int)
    return pred, proba


LABEL_MAP = {0: "Izquierda", 1: "Derecha"}
COLOR_MAP = {0: "#d62828", 1: "#1d4ed8"}
