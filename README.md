# Churn Prediction & Growth Strategy Challenge
#### Luis F. Alvarez


Este repositorio contiene una solución integral para la predicción de abandono (churn) y el diseño de estrategias de crecimiento en una plataforma fintech. El proyecto se divide en tres fases: segmentación de usuarios comprometidos, modelado predictivo de aprendizaje automático y diseño experimental para optimización del ROI.

## 📂 Estructura del Repositorio

```text
Lemon_DS_Challenge/
├── data/
│   ├── user_activity.csv            # Dataset original
│   └── engaged_user_activity.csv    # Dataset filtrado (Fase 1)
├── outputs/
│   ├── churn_model.pkl              # Modelo serializado y threshold
│   ├── usuarios_a_tratar.csv        # Scoring y priorización (Fase 2)
│   └── experimento_growth_final.csv # Asignación de grupos A/B (Fase 3)
├── preprocess_data.py                        # Segmentación de usuarios engaged
├── churn_prediction.py           # Modelado de Machine Learning
├── growth_design.py              # Estrategia y diseño estadístico
├── requirements.txt                 # Dependencias del proyecto
├── INSTRUCTIONS.md                  # Instrucciones del challenge 
└── README.md                        # Documentación sobre el proyecto y ejercicio realizado
``` 

## Guía de Configuración

Pasos para configurar el entorno local y ejecutar el pipeline completo.

### 1. Requisitos Previos
* Python 3.9 o superior.
* Acceso a terminal/línea de comandos.

### 2. Instalación del Entorno Virtual
```bash
# Crear el entorno virtual
python -m venv lemon_env

# Activar el entorno
# En macOS/Linux:
source lemon_env/bin/activate

# En Windows:
.\lemon_env\Scripts\activate 
```

### 3. Instalación de dependencias
```bash 
pip install -r requirements.txt 
```





### 4. Procesos y Fases

| Archivo                  | Fase           | Descripción                                                                 | Output Principal                        |
|--------------------------|----------------|-----------------------------------------------------------------------------|-----------------------------------------|
| `01 preprocess_data.py`              | Segmentación   | Filtra la base original para identificar usuarios "Engaged" (comprometidos).| `data/engaged_user_activity.csv`        |
| `02 churn_prediction.py` | ML Modeling    | Entrenamiento, optimización (GridSearch) y validación del modelo de Churn.  | `outputs/usuarios_a_tratar.csv`         |
| `03 growth_design.py`    | Strategy       | Cálculo de ROI, simulación de negocio y diseño de experimento A/B.          | `outputs/experimento_growth_final.csv`  |


#### Fase 1: Definición de Engagement (preprocess_data.py)
- **Lógica**: Se definió un proxy de actividad para filtrar usuarios que realmente utilizan la app.
- **Criterio:** Antigüedad >= 2 meses y frecuencia >= 1 login o transacción mensual (promedio).

#### Fase 2: Modelo Predctivo (churn_prediction.py)
- **Modelo:** Se utilizó un HistGradientBoostingClassifier con optimización de hiperparámetros y validación cruzada estratificada.
- **Métrica:** El modelo alcanzó un ROC-AUC de 0.95.
- **Feature Engineering:** Se crearon ratios de adherencia como earn_tx_ratio y product_breadth.
- **Control de Leakage:** Se eliminaron variables con informaciøon endógena como days_since_last_login para garantizar un modelo puramente preventivo.

#### Fase 3: Estrategia de Growth (growth_strategy_and_test.py)
- **Acción:** Otorgar un subsidio de tasa a usuarios en riesgo que no utilizan activamente el producto de inversión.
- **Diseño Experimental:** A/B Test estratificado (50/50) para maximizar el poder estadístico con la muestra disponible.
- **ROI Proyectado:** 12.2% basado en la precisión del modelo y una efectividad estimada del bono del 25%.

## Outputs

- *usuarios_a_tratar.csv:* Lista priorizada por probabilidad de churn y métricas de valor transaccional.

- *experimento_growth.csv:* Base con asignación aleatoria de grupos (Tratamiento vs Control) lista para ejecución.


### Diccionario de supuestos

Disclaimer: Los supuestos son arbitrarios y simples, no para modelar un comportamiento real de la industria, si no mas para llevar adelante el ejercicio práctico.

| Parámetro        | Valor   | Definición Teórica                                              | Aplicación en el Caso                                                                 |
|------------------|---------|-----------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Alpha (α)        | 0.05    | Probabilidad de Falso Positivo (Error Tipo I).                  | Riesgo aceptado de concluir que la campaña funciona cuando fue azar.                  |
| Power (1-β)      | 0.80    | Probabilidad de detectar un efecto real (Poder estadístico).     | Probabilidad de capturar el impacto real del incentivo propuesto.                     |
| Effect Size (MDE)| 0.10    | Magnitud mínima del cambio que se desea detectar.                | Buscamos detectar un incremento mínimo del 10% en la tasa de retención.               |
| LTV Recuperado   | $20.00  | Valor neto ganado por cada usuario salvado.                     | Resultado de $4/mes de margen durante 5 meses extra de vida.                          |
| Costo Bono       | $4.10   | Inversión unitaria por usuario en el grupo de tratamiento.       | Costo del incentivo "Earn Booster" para fomentar la retención.                        |
| Precisión ML     | 0.92    | Capacidad del modelo para identificar churners reales.           | Asegura que el presupuesto se asigne a usuarios con riesgo real.                      |


## 📊 Conclusiones de Negocio y Rigurosidad Estadística

### Impacto en el Negocio (Profitability)
La implementación del modelo permite una **optimización quirúrgica del presupuesto de marketing**. Al contar con una **precisión del 92%**, la campaña minimiza el desperdicio de capital en usuarios que no requieren incentivos (falsos positivos), logrando que por cada dólar invertido se genere un retorno neto que posiciona el **ROI en un 12.20%**. 

El beneficio neto estimado de **$616.00 USD** para este segmento de usuarios demuestra que el modelo no solo es una herramienta técnica, sino un motor de rentabilidad que permite recuperar valor (LTV) mediante el uso estratégico del producto **Earn**.

#### Cálculo de Retorno Estimado
Para asegurar la transparencia financiera, se utiliza la siguiente lógica de cálculo para el retorno bruto:

$$\text{Retorno Bruto} = (N_{A} \times P) \times E \times \text{LTV}_{5m}$$

Donde:
* **$N_{A}$**: Usuarios en el grupo de tratamiento (1,232).
* **$P$**: Precisión del modelo (0.92), que garantiza que el incentivo se dirige a churners reales.
* **$E$**: Efectividad estimada del incentivo o tasa de conversión (0.25).
* **$\text{LTV}_{5m}$**: Margen neto recuperado por usuario activo durante 5 meses adicionales ($20.00).



### Rigurosidad y Validez del Experimento
Para garantizar que los resultados obtenidos no sean fruto del azar, el diseño experimental se apoya en los siguientes pilares:

1. **Poder Estadístico:** Con una población en riesgo de **2,489** usuarios, contamos con una muestra en el grupo de tratamiento de **1,232** individuos. Esto supera ampliamente la muestra mínima requerida (**327**) para detectar un efecto de mejora del 10% (MDE) con un nivel de confianza del 95% y un poder del 80%.
2. **Control de Sesgo:** La asignación aleatoria (A/B Split 50/50) asegura que factores externos (como fluctuaciones en el mercado crypto: UNA BAJA FUERTE DE BTC) afecten a ambos grupos por igual, permitiendo atribuir el éxito de la retención exclusivamente a la intervención del modelo.
3. **Reproducibilidad:** Se ha fijado una semilla aleatoria (`random seed`) en el script `03_growth_design.py` para garantizar que la segmentación de grupos sea consistente y replicable.