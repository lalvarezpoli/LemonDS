# Data Science Challenge - Predicción de Churn

**Posición**: Semi-Senior Data Scientist  
**Tiempo estimado**: 3-4 días

---

## Contexto

Trabajas en el equipo de Data de una fintech que ofrece servicios de pagos, inversiones y ahorro. El equipo de Growth te pide ayuda para abordar el problema del **churn**: la proporción de usuarios que dejan de utilizar la aplicación.

El foco está puesto en **usuarios previamente comprometidos** que, de manera repentina, dejan de interactuar con la app. El objetivo es identificarlos antes de que se vayan para poder tomar acciones preventivas.

---

## Definiciones

| Concepto | Definición |
|----------|------------|
| **Usuario comprometido** | Usuario que realiza al menos una transacción o inicia sesión en la aplicación una vez por mes durante un mínimo de **2 meses consecutivos** |
| **Churn** | Usuario que deja de transaccionar **y** de iniciar sesión en la app |

---

## Dataset

El archivo `data/user_activity.csv` contiene información agregada de 10,000 usuarios:

| Columna | Descripción |
|---------|-------------|
| `user_id` | Identificador único del usuario |
| `active_month` | Cantidad de meses con actividad |
| `avg_month_logins_amount` | Promedio mensual de logins |
| `days_since_last_login` | Días desde el último login |
| `frecuency_score_last_active_month` | Score de frecuencia de uso |
| `is_churn` | **Target**: 1 si el usuario hizo churn, 0 si no |
| `avg_month_fiat_payment_*` | Pagos en moneda fiat (volumen y cantidad) |
| `avg_month_crypto_payment_*` | Pagos en crypto |
| `avg_month_fiat_cashin_*` | Depósitos fiat |
| `avg_month_fiat_cashout_*` | Retiros fiat |
| `avg_month_crypto_cashin_*` | Compra de crypto |
| `avg_month_crypto_cashout_*` | Venta de crypto |
| `avg_month_earn_*` | Producto de rendimientos/ahorro |

---

## Tareas

### 1. Modelo de Predicción de Churn

Construye un modelo para predecir qué usuarios comprometidos tienen alta probabilidad de hacer churn el próximo mes.

**Requisitos:**
- Reportar las métricas que consideres relevantes
- Explicar todos los tests/validaciones que harías para asegurar que el modelo funciona correctamente
- Identificar los principales drivers de churn

### 2. Estrategia de Growth

Proponer una estrategia que el equipo de Growth podría implementar usando tu modelo para reducir el churn.

**Requisitos:**
- La estrategia debe tener **ROI positivo**
- Supuesto dado: si lográs retener a un usuario, este permanecerá activo **5 meses adicionales**
- Incluir cálculo de ROI estimado

### 3. Diseño de Experimento

Plantear cómo medirías si la estrategia propuesta tuvo éxito.

**Requisitos:**
- Diseño del experimento (A/B test u otro)
- Test estadístico a utilizar
- Cálculo de tamaño de muestra necesario
- Criterios de éxito

---

## Entregables

```
tu_solucion/
├── README.md                    # Instrucciones para ejecutar tu código
├── src/
│   └── model.py                 # Código del modelo (debe ejecutarse)
├── outputs/
│   └── usuarios_a_tratar.csv    # Lista de usuarios a intervenir
└── ESTRATEGIA.md                # Documento con estrategia y experimento
```

### Formato del archivo `usuarios_a_tratar.csv`

| Columna | Descripción |
|---------|-------------|
| `user_id` | ID del usuario |
| `churn_probability` | Probabilidad estimada de churn |
| ... | Otras columnas que consideres útiles |

---

## Criterios de Evaluación

| Aspecto | Peso |
|---------|------|
| **Modelo**: métricas, validación, feature engineering | 40% |
| **Estrategia**: viabilidad, ROI, creatividad | 30% |
| **Experimento**: diseño estadístico, rigor | 20% |
| **Código**: calidad, documentación, reproducibilidad | 10% |

---

## Requisitos Técnicos

- Python 3.8+
- El código debe poder ejecutarse desde cero con las dependencias listadas
- Incluir un `requirements.txt` con las librerías utilizadas

### Dependencias sugeridas (no obligatorias)

```
pandas
numpy
scikit-learn
scipy
```

---

## Preguntas

Si tenés dudas sobre el challenge, podés enviarlas a mateo.esses@lemon.me.

¡Buena suerte!
