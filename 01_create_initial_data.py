# 01_create_initial_data.py
import pandas as pd
import numpy as np
import os

print("Paso 1: Creando datos iniciales...")
# Crear un directorio para la salida si no existe
os.makedirs('/tmp/data', exist_ok=True)

# Crear un DataFrame de ejemplo
timestamps = pd.to_datetime(pd.date_range(start='2025-01-01', periods=100, freq='D'))
value1 = 100 + np.cumsum(np.random.randn(100) * 2)
value2 = 50 + np.cumsum(np.random.randn(100) * 0.5)
noise = np.random.randn(100)

df = pd.DataFrame({
    'timestamp': timestamps,
    'value1': value1,
    'value2': value2,
    'noise_col': noise
})

# Guardar en un fichero CSV que será nuestro "artefacto" de salida
output_path = '/tmp/data/raw_data.csv'
df.to_csv(output_path, index=False)

print(f"Datos iniciales guardados en {output_path}")