import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import logging
import shap
import os
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import (classification_report, roc_auc_score, 
                             precision_recall_curve)
from sklearn.utils.class_weight import compute_sample_weight

# --- IMPORTACIÓN MODULAR ---
try:
    from preprocess_data import DataProcessor
except ImportError:
    # Workaround si decides mantener el nombre con números
    import importlib
    _preprocess = importlib.import_module("01_preprocess")
    DataProcessor = _preprocess.DataProcessor

# --- LOGGING CONFIG ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.threshold = 0.5

    def train_optimized(self, X_train, y_train):
        logger.info(f"Iniciando Optimización sobre {X_train.shape[0]} muestras...")
        
        # Balanceo mediante pesos (Fundamental por el 75% de Churn)
        weights = compute_sample_weight(class_weight='balanced', y=y_train)
        
        hgb = HistGradientBoostingClassifier(random_state=42)
        
        param_grid = {
            'max_iter': [100, 150],
            'max_depth': [3, 4],
            'learning_rate': [0.05, 0.1],
            'l2_regularization': [1.0, 10.0]
        }
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid = GridSearchCV(hgb, param_grid, cv=cv, scoring='f1', n_jobs=-1)
        
        grid.fit(X_train, y_train, sample_weight=weights)
        self.model = grid.best_estimator_
        logger.info(f"Optimización finalizada. Mejores Params: {grid.best_params_}")

    def evaluate(self, X_test, y_test):
        probs = self.model.predict_proba(X_test)[:, 1]
        
        # Optimización dinámica de Threshold para maximizar F1-Score
        precision, recall, thresholds = precision_recall_curve(y_test, probs)
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-9)
        self.threshold = thresholds[np.argmax(f1_scores)]
        
        preds = (probs >= self.threshold).astype(int)
        
        print("\n" + "="*45)
        print(f"REPORT FINAL DEL MODELO (ROC-AUC: {roc_auc_score(y_test, probs):.4f})")
        print(f"THRESHOLD ÓPTIMO APLICADO: {self.threshold:.4f}")
        print("="*45)
        print(classification_report(y_test, preds))
        return probs

    def generate_shap_visual(self, X):
        logger.info("Generando Visualización SHAP...")
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        
        plt.figure(figsize=(12, 8))
        shap.summary_plot(shap_values, X, plot_type="bar", show=False)
        plt.title("Drivers de Churn: Impacto en la Predicción")
        plt.tight_layout()
        plt.show()

    def save_artifact(self, folder='outputs'):
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, 'churn_model.pkl')
        joblib.dump({'model': self.model, 'threshold': self.threshold}, path)
        logger.info(f"Artefacto guardado en {path}")

def __main__():
    # 1. Carga de datos ya segmentados (Engaged)
    raw_df = pd.read_csv('data/engaged_user_activity.csv')
    
    # 2. Pre-procesamiento usando la clase importada (Modularidad)
    X, y, user_ids = DataProcessor.transform(raw_df)
    X_full = X.copy() 

    # 3. Split Estratificado
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # 4. Entrenamiento y Evaluación
    predictor = ChurnPredictor()
    predictor.train_optimized(X_train, y_train)
    predictor.evaluate(X_test, y_test)
    
    # 5. Generación de Explicabilidad (SHAP)
    predictor.generate_shap_visual(X_train)
    
    # 6. GENERACIÓN DE "USUARIOS A TRATAR"
    logger.info("Generando scores para la campaña de Growth...")
    all_probs = predictor.model.predict_proba(X_full)[:, 1]
    
    usuarios_a_tratar = pd.DataFrame({
            'user_id': user_ids.values,
            'churn_probability': all_probs,
            'is_target': (all_probs >= predictor.threshold).astype(int),
            'antiguedad_meses': raw_df['active_month'].values,
            'frecuencia_mensual': raw_df['avg_month_logins_amount'].values,
            'volumen_fiat_mensual': raw_df['avg_month_fiat_payment_volumen'].values,
            'volumen_crypto_mensual': raw_df['avg_month_crypto_payment_volumen'].values,
            'volumen_earn_total': raw_df['avg_month_earn_volumen'].values,
            'diversificacion_productos': X_full['product_breadth'].values,
            'uso_earn_ratio': X_full['earn_tx_ratio'].values
        })
    
    # Filtramos solo los que el modelo recomienda intervenir
    intervencion_df = usuarios_a_tratar[usuarios_a_tratar['is_target'] == 1].copy()

    # 7. Persistencia
    os.makedirs('outputs', exist_ok=True)
    intervencion_df.to_csv('outputs/usuarios_a_tratar.csv', index=False)
    predictor.save_artifact()
    
    logger.info(f"✅ Proceso finalizado. {len(intervencion_df)} usuarios priorizados en 'outputs/usuarios_a_tratar.csv'.")

if __name__ == "__main__":
    __main__()