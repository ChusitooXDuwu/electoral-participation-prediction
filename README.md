# Predicción de Orientación Política — ECP 2023

App de Streamlit que predice la **orientación política (izquierda / derecha)** de una persona a partir de sus respuestas en la Encuesta de Cultura Política 2023 del DANE (Colombia).

## Estructura

```
.
├── app/
│   ├── streamlit_app.py            # Página de inicio
│   ├── utils.py                    # Carga de modelo y datos (caché)
│   ├── features_metadata.py        # Etiquetas y opciones legibles de las 73 variables
│   ├── best_model.pkl              # Modelo entrenado (XGBoost)
│   └── pages/
│       ├── 1_🧮_Predicción_individual.py
│       ├── 2_📂_Predicción_por_lotes.py
│       ├── 3_📊_Desempeño_del_modelo.py
│       └── 4_🔍_Datos_y_EDA.py
├── data/
│   ├── raw/empalme_politica.csv
│   └── processed/political_orientation_clean.csv
├── notebooks/                      # Pipeline 01–04
├── figures/                        # Matrices de confusión, ROC, EDA
├── .streamlit/config.toml          # Tema visual
└── requirements.txt
```

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

La app abre en <http://localhost:8501>.

> Si `app/best_model.pkl` o `data/processed/political_orientation_clean.csv` no existen, ejecuta primero los notebooks `02_data_preprocessing.ipynb` y `03_model_training.ipynb`.

## Despliegue en Streamlit Community Cloud

1. Sube el repo a GitHub (incluye `app/best_model.pkl` y el CSV procesado para que la app arranque sin necesidad de re-entrenar).
2. Entra a <https://share.streamlit.io> y conecta tu cuenta de GitHub.
3. **New app** → selecciona el repo, branch `main`, y como entrypoint:
   ```
   app/streamlit_app.py
   ```
4. En *Advanced settings* fija la versión de Python a **3.11**.
5. *Deploy*. El build instala lo que está en `requirements.txt`.

> El modelo pesa pocos MB; si lo subes vía Git LFS configura el LFS en Cloud o, alternativamente, súbelo a un release de GitHub y descárgalo al arrancar.

## Modelo

- Algoritmo: **XGBoost** (`n_estimators=200, max_depth=5, learning_rate=0.1`).
- Variable objetivo: `political_orientation` (0 = Izquierda, 1 = Derecha), derivada de P5328 según la convención del Barómetro de las Américas.
- F1 ≈ 0.80, ROC-AUC ≈ 0.79 en test (15% estratificado).

## Datos

- Fuente: [Encuesta de Cultura Política 2023 — DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/gobierno/cultura-politica-encuesta).
- 73 variables sobre demografía, confianza institucional, participación, valores sociales y consumo de información política.
