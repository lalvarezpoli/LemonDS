import pandas as pd
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
import logging

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_growth_design():
    # 0. FIJAR SEMILLA PARA REPRODUCIBILIDAD
    # Crucial para que la asignación de grupos sea consistente
    np.random.seed(42)

    # 1. CARGA DE DATOS
    try:
        df = pd.read_csv('outputs/usuarios_a_tratar.csv')
    except FileNotFoundError:
        logger.error("Error: No se encuentra 'outputs/usuarios_a_tratar.csv'.")
        return

    # 2. DISEÑO DEL EXPERIMENTO (A/B Split 50/50)
    # Grupo A: Tratamiento | Grupo B: Control
    df['group'] = np.random.choice(['A', 'B'], size=len(df), p=[0.50, 0.50])
    
    # 3. SUPUESTOS DE NEGOCIO (ROI ~12.2%)
    costo_incentivo = 4.10      # USD (Costo del 'Earn Booster')
    precision_modelo = 0.92    # Del archivo 02_churn_prediction.py
    ltv_mensual_recup = 4.00   # Margen promedio mensual
    meses_extra = 5            # Supuesto del challenge
    efectividad_bono = 0.25    # Tasa de conversión del incentivo
    
    ltv_total_recup = ltv_mensual_recup * meses_extra # $20.00
    
    # 4. CÁLCULO DE ROI ESTIMADO
    n_tratados = len(df[df['group'] == 'A'])
    costo_total = n_tratados * costo_incentivo
    
    # Churners reales que se quedan gracias al bono
    usuarios_salvados = (n_tratados * precision_modelo) * efectividad_bono
    retorno_total = usuarios_salvados * ltv_total_recup
    
    roi_estimado = (retorno_total - costo_total) / costo_total
    
    # 5. CÁLCULO DE RIGOR ESTADÍSTICO
    # MDE = 0.10 significa que queremos detectar si la retención sube 10 puntos
    mde = 0.10
    h = proportion_effectsize(0.25, 0.25 + mde) # h de Cohen
    
    analysis = NormalIndPower()
    n_req_per_group = analysis.solve_power(
        effect_size=h, 
        alpha=0.05, 
        power=0.80, 
        ratio=1.0 
    )
    
    # 6. RESULTADOS FINALES
    print("\n" + "="*45)
    print("      BUSINESS CASE: ESTRATEGIA GROWTH      ")
    print("="*45)
    logger.info(f"Población total identificada: {len(df)}")
    logger.info(f"Usuarios en Grupo Tratamiento: {n_tratados}")
    logger.info(f"Muestra mínima requerida p/grupo: {int(n_req_per_group)}")
    
    status = "SÍ" if (len(df)/2) >= n_req_per_group else "NO (Ajustar MDE)"
    logger.info(f"¿Poder estadístico suficiente?: {status}")
    
    print("-" * 45)
    logger.info(f"ROI PROYECTADO: {roi_estimado:.2%}")
    logger.info(f"Inversión Estimada: ${costo_total:,.2f} USD")
    logger.info(f"Beneficio Neto Est.: ${(retorno_total - costo_total):,.2f} USD")
    print("="*45)
    
    # 7. EXPORTACIÓN
    output_path = 'outputs/experimento_growth.csv'
    df.to_csv(output_path, index=False)
    logger.info(f"Asignación de grupos guardada en: {output_path}")

if __name__ == "__main__":
    run_growth_design()