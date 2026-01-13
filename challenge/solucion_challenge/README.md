# 🍋 Lemon Data Science Case: Credit Risk/Fraud Analysis

Este repositorio contiene la resolución del caso técnico para el equipo de Data Science. El objetivo es desarrollar un modelo predictivo robusto, reproducible y listo para una transición hacia producción.

## 1. Replicabilidad y Configuración del Entorno

Este proyecto utiliza un entorno virtual aislado para garantizar que las dependencias no entren en conflicto con otros proyectos locales.

### Requisitos previos
* **Python 3.12.x**
* `pip`

### Configuración del Entorno Virtual

1. **Crear el entorno virtual:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activarlo :**
   ```
   - En macOS/Linux: source .venv/bin/activate

   - En Windows: .\.venv\Scripts\activate
   ```

3. **Dependencias:**
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

Nota sobre gestión de paquetes: Aunque se utiliza pip por defecto, este proyecto es totalmente compatible con uv. Si prefieres una resolución de dependencias más rápida y robusta contra conflictos, puedes usar: uv pip install -r requirements.txt.

4. **Estructura del Proyecto**
```
challenge-fintech/
├── data/               # Datos del reto (excluidos del control de versiones)
│   ├── raw/            # Datos originales (inmutables)
│   └── processed/      # Datos limpios y transformados
├── notebooks/          # Experimentación y análisis paso a paso
│   ├── 01_eda.ipynb    # Análisis Exploratorio de Datos
│   └── 02_model.ipynb  # Entrenamiento, validación y métricas
├── src/                # Código fuente modular (funciones auxiliares)
│   ├── __init__.py
│   ├── preprocess.py   # Limpieza y preparación de datos
│   └── features.py     # Ingeniería de variables
├── models/             # Artefactos de modelos entrenados (pikl, xgboost)
├── reports/            # Gráficos e informe final de resultados
├── .gitignore          # Exclusión de archivos pesados y temporales
├── requirements.txt    # Librerías base con rangos de versiones
└── requirements-lock.txt # Versiones exactas para replicabilidad total```
