# Guía de entrenamiento y ejecución del modelo

Esta guía describe paso a paso cómo reproducir el modelo de predicción de orientación política y cómo ejecutar la aplicación que lo expone.

- Repositorio: <https://github.com/ChusitooXDuwu/electoral-participation-prediction>
- App pública: desplegada en Streamlit Community Cloud.

---

## 1. Requisitos previos

- Python 3.11 (probado en 3.11.3).
- Git instalado.
- Un cliente Jupyter para ejecutar los notebooks (`jupyter`, VS Code, etc.).
- Conexión a internet para descargar dependencias.

---

## 2. Obtener el código

```bash
git clone https://github.com/ChusitooXDuwu/electoral-participation-prediction.git
cd electoral-participation-prediction
```

---

## 3. Crear entorno e instalar dependencias

Se recomienda usar un entorno virtual.

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux o macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Las dependencias principales son: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `joblib`, `matplotlib`, `plotly` y `streamlit`.

---

## 4. Estructura del repositorio

```
.
├── app/                            # Aplicación Streamlit
│   ├── streamlit_app.py            # Página de inicio
│   ├── utils.py                    # Carga del modelo y datos
│   ├── features_metadata.py        # Etiquetas legibles de las variables
│   ├── theme.py                    # Estilos compartidos
│   ├── best_model.pkl              # Modelo entrenado (bundle)
│   ├── shap_importance.csv         # Importancia SHAP global exportada
│   └── pages/                      # Subpáginas de la app
├── data/
│   ├── raw/empalme_politica.csv    # Datos originales (ECP 2023, DANE)
│   ├── processed/                  # Dataset limpio para entrenamiento
│   └── sample_batch.csv            # Muestra para probar la predicción por lotes
├── notebooks/                      # Pipeline 01 a 03
├── figures/                        # Gráficos generados por los notebooks
├── .streamlit/config.toml          # Configuración visual de la app
├── requirements.txt
└── README.md
```

---

## 5. Reproducir el modelo

El pipeline está compuesto por tres notebooks en `notebooks/`, que deben ejecutarse en orden.

### 5.1. Análisis exploratorio

Archivo: `01_data_understanding_and_eda.ipynb`

- Carga los datos crudos de la Encuesta de Cultura Política 2023.
- Realiza el perfilado del conjunto de datos.
- Analiza la variable objetivo original `P5328` (escala 1–10) y justifica su binarización siguiendo la convención del Barómetro de las Américas.
- Produce visualizaciones en `figures/`.

Este notebook no genera artefactos requeridos por la app, pero documenta las decisiones de preprocesamiento.

### 5.2. Preprocesamiento

Archivo: `02_data_preprocessing.ipynb`

- Selecciona 74 columnas relevantes del cuestionario.
- Elimina observaciones con valores faltantes.
- Excluye las categorías de no respuesta (`98`, `99`) y las posiciones centrales de la escala (`5`, `6`).
- Construye la variable objetivo binaria `political_orientation`:
  - `0` → izquierda (P5328 entre 1 y 4)
  - `1` → derecha (P5328 entre 7 y 10)
- Elimina la columna `P5328` para evitar fuga de información.

Salida:

```
data/processed/political_orientation_clean.csv
```

Dimensiones finales: 16 383 filas × 74 columnas (73 predictoras + el objetivo).

### 5.3. Entrenamiento, evaluación y selección

Archivo: `03_model_training.ipynb`

- Divide el dataset en entrenamiento y prueba (`test_size = 0.15`, estratificado, `random_state = 42`).
- Entrena y evalúa cinco modelos:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Gradient Boosting
  - XGBoost
- Optimiza hiperparámetros con `GridSearchCV` (5 folds).
- Evalúa con accuracy, precisión, recall, F1, ROC-AUC, matrices de confusión y curvas ROC.
- Calcula la importancia global de variables mediante valores SHAP y descarta las menos influyentes.
- Re-entrena el modelo ganador (XGBoost) sobre el subconjunto seleccionado de 58 variables.
- Serializa el modelo final en un diccionario.

Salidas principales:

```
app/best_model.pkl          # dict con keys: model, selected_features, shap_importance
app/shap_importance.csv     # importancia SHAP global exportada
figures/*.png               # matrices de confusión, curvas ROC y comparativas
```

Métricas de referencia del modelo final:

- Accuracy ≈ 74 %
- F1 (clase derecha) ≈ 0.80
- ROC-AUC ≈ 0.79

### 5.4. Cómo ejecutar los notebooks

Desde la raíz del proyecto:

```bash
jupyter notebook
```

Abrir los archivos dentro de `notebooks/` y ejecutarlos en orden con *Run All*. También pueden ejecutarse en lote:

```bash
jupyter nbconvert --to notebook --execute notebooks/02_data_preprocessing.ipynb --output 02_data_preprocessing.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_model_training.ipynb     --output 03_model_training.ipynb
```

> El paso 5.1 (EDA) es opcional para la reproducción del modelo, pero recomendado para contexto.

---

## 6. Ejecutar la aplicación localmente

Una vez generados `app/best_model.pkl` y `data/processed/political_orientation_clean.csv`:

```bash
streamlit run app/streamlit_app.py
```

La app abre en <http://localhost:8501> y expone cuatro secciones:

1. Predicción individual con explicación SHAP por predicción.
2. Predicción por lotes a partir de un archivo CSV.
3. Desempeño del modelo (métricas, figuras, importancia global SHAP).
4. Datos y exploración por variable.

Para probar la predicción por lotes se puede usar `data/sample_batch.csv`, que contiene 20 filas reales del conjunto procesado.


---

## 7. Notas

- El archivo `app/best_model.pkl` se versiona en el repositorio para que la app pueda arrancar sin necesidad de re-entrenar.
- Los notebooks dependen de rutas relativas a la raíz del proyecto.
- Si se modifica el preprocesamiento (notebook 02) es necesario re-ejecutar también el entrenamiento (notebook 03).
- El modelo ganador puede variar entre ejecuciones por la naturaleza estocástica de algunos algoritmos, aunque los `random_state` están fijados.
