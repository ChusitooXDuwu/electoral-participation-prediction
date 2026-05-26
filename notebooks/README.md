# Notebooks del proyecto

Esta carpeta contiene los notebooks utilizados para el desarrollo del proyecto **Electoral Participation Prediction**, cuyo objetivo es predecir la orientación política binaria de los individuos a partir de variables sociodemográficas, percepciones políticas y variables relacionadas con la participación ciudadana utilizando técnicas de aprendizaje automático.

Los notebooks deben ejecutarse en el orden presentado a continuación.

---

## Estructura de notebooks

### 01_data_understanding_and_eda.ipynb

Este notebook realiza el análisis exploratorio inicial del conjunto de datos.

Actividades principales:

- Carga y exploración del conjunto de datos.
- Identificación de dimensiones y tipos de variables.
- Análisis de valores faltantes.
- Exploración de la variable objetivo original (`P5328`).
- Visualización de distribuciones.
- Análisis descriptivo de variables relevantes.
- Generación de visualizaciones utilizadas posteriormente en el documento.

Resultado esperado:

- Comprensión inicial de los datos.
- Identificación de decisiones necesarias para el preprocesamiento.

---

### 02_data_preprocessing.ipynb

Este notebook aplica las decisiones de limpieza y transformación definidas durante el análisis exploratorio.

Actividades principales:

- Selección de variables relevantes.
- Eliminación de valores faltantes.
- Exclusión de categorías no válidas (`98` y `99`).
- Eliminación de categorías ideológicas centrales.
- Construcción de la variable objetivo binaria:

    - 0 → orientación política hacia izquierda
    - 1 → orientación política hacia derecha

- Eliminación de variables que puedan generar fuga de información.
- Generación del conjunto de datos limpio para entrenamiento.

Resultado esperado:

- Creación del archivo:

```text
../data/processed/political_orientation_clean.csv
```

---

### 03_model_training.ipynb

Este notebook realiza el entrenamiento, evaluación e interpretabilidad de los modelos de aprendizaje automático.

Actividades principales:

#### Entrenamiento y evaluación

- División entrenamiento/prueba.
- Entrenamiento de múltiples modelos:

    - Logistic Regression
    - Decision Tree
    - Random Forest
    - Gradient Boosting
    - XGBoost

- Evaluación mediante:

    - Accuracy
    - Precision
    - Recall
    - F1-score
    - ROC-AUC
    - Matrices de confusión
    - Curvas ROC

- Optimización de hiperparámetros mediante GridSearchCV para Random Forest.
- Selección del mejor modelo.

#### Interpretabilidad

- Cálculo de importancia de variables.
- Análisis mediante SHAP values.
- Visualización global del impacto de las variables.
- Interpretación del comportamiento del modelo.

Resultado esperado:

- Modelo final entrenado.
- Gráficos de evaluación.
- Gráficos de interpretabilidad.
- Archivos auxiliares para despliegue.

---

## Orden recomendado de ejecución

Ejecutar los notebooks en el siguiente orden:

```text
01_data_understanding_and_eda.ipynb

↓

02_data_preprocessing.ipynb

↓

03_model_training.ipynb
```

---

## Dependencias

Instalar las librerías necesarias desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

---

## Notas

- Los notebooks dependen de las rutas definidas dentro de la estructura del repositorio.
- Se recomienda ejecutar los notebooks desde la carpeta raíz del proyecto.
- Los modelos serializados (`.pkl` o `.joblib`) no se almacenan en el repositorio debido a restricciones de tamaño en GitHub.
- Los modelos pueden regenerarse ejecutando nuevamente el notebook de entrenamiento.

