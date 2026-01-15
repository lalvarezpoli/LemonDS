import pandas as pd
import numpy as np
import logging

# --- LOGGING CONFIG ---
# Configuramos el logging para tener trazabilidad de los pasos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, filepath=None):
        """
        Si se pasa un filepath, carga los datos. 
        Si no, se puede usar para llamar a métodos estáticos.
        """
        if filepath:
            self.df = pd.read_csv(filepath)
            logger.info(f"Datos cargados desde {filepath}")
        else:
            self.df = None

    def define_engagement(self):
        """
        FILTRADO INICIAL: Identifica usuarios 'Engaged'.
        Regla: (Antigüedad >= 2) Y (Logins promedio >= 1 O Transacciones promedio >= 1)
        """
        if self.df is None:
            raise ValueError("No hay datos cargados en la instancia para definir engagement.")

        logger.info("Iniciando segmentación de usuarios comprometidos...")

        # 1. Identificar columnas de cantidad de transacciones (basado en el sufijo del dataset)
        tx_quantity_cols = [col for col in self.df.columns if '_tx_amount' in col]
        
        # 2. Calcular el total de transacciones promedio por mes (frecuencia)
        self.df['total_avg_tx_count'] = self.df[tx_quantity_cols].sum(axis=1)
        
        # 3. Aplicar la lógica de segmentación
        condition_history = self.df['active_month'] >= 2 
        condition_activity = (self.df['avg_month_logins_amount'] >= 1) | (self.df['total_avg_tx_count'] >= 1)

        # Mantenemos el criterio amplio: no filtramos por actividad del último mes 
        # para no perder usuarios que están justamente entrando en churn (fase de inactividad).
        self.df['is_engaged'] = condition_history & condition_activity

        # Filtrar el dataset
        engaged_df = self.df[self.df['is_engaged'] == True].copy()
        
        logger.info(f"Segmentación finalizada: {engaged_df.shape[0]} usuarios encontrados.")
        return engaged_df

    @staticmethod
    def transform(df):
        """
        PIPELINE DE INGENIERÍA DE FEATURES: 
        Este método es estático porque recibe un DataFrame y devuelve los sets de entrenamiento.
        Se usa en la Fase 2 (Modelado) sobre el dataset de usuarios engaged.
        """
        logger.info("Ejecutando Pipeline de Pre-procesamiento y Feature Engineering...")
        df = df.copy()
        
        # 1. Limpieza y tipado
        target = 'is_churn'
        if target in df.columns:
            df[target] = df[target].astype(int)
        
        # Aseguramos que todo sea numérico para el modelo
        cols_to_exclude = ['user_id', target]
        for col in [c for c in df.columns if c not in cols_to_exclude]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.fillna(0)

        # 2. Winsorization (Capping al percentil 99 para mitigar outliers extremos)
        tx_cols = [c for c in df.columns if 'volumen' in c or 'amount' in c]
        for col in tx_cols:
            df[col] = df[col].clip(upper=df[col].quantile(0.99))

        # 3. Feature Engineering: Stickiness & Diversificación
        # Ratio de inversión: ¿Qué tanto de su actividad es ahorro?
        df['earn_tx_ratio'] = df['avg_month_earn_tx_amount'] / (df['total_avg_tx_count'] + 1)
        
        # Diversidad de productos: Fiat, Crypto, Earn.
        df['product_breadth'] = (
            (df['avg_month_fiat_payment_volumen'] > 0).astype(int) + 
            (df['avg_month_crypto_payment_volumen'] > 0).astype(int) + 
            (df['avg_month_earn_volumen'] > 0).astype(int)
        )
        
        # Flujo neto de capital Fiat
        df['net_fiat_flow'] = df['avg_month_fiat_cashin_volumen'] - df['avg_month_fiat_cashout_volumen']

        # 4. Eliminación de Leaks (Fuga de datos del futuro)
        leaks = [
            'user_id', 'is_churn', 'is_engaged', 
            'days_since_last_login', 'frecuency_score_last_active_month'
        ]
        
        X = df.drop(columns=[c for c in leaks if c in df.columns], errors='ignore')
        y = df[target] if target in df.columns else None
        
        return X, y, df['user_id']

def __main__():
    # 1. Instanciar y procesar
    processor = DataProcessor('data/user_activity.csv')
    df_engaged = processor.define_engagement()

    # 2. Reporte rápido en consola
    print("\n" + "="*30)
    print("REPORTE DE SEGMENTACIÓN")
    print("="*30)
    print(f"Total Engaged: {df_engaged.shape[0]}")
    if 'is_churn' in df_engaged.columns:
        print(f"Tasa de Churn en este segmento: {df_engaged['is_churn'].mean():.2%}")
    
    # 3. Guardado del dataset para la Fase 2 (Modeling)
    df_engaged.to_csv('data/engaged_user_activity.csv', index=False)
    logger.info("Archivo 'data/engaged_user_activity.csv' guardado con éxito.")

if __name__ == "__main__":
    __main__()