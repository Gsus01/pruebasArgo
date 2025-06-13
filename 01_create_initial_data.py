# 01_create_initial_data.py
import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description="Genera un dataset de ejemplo")
parser.add_argument("--output-path", default="/tmp/initial_data.dat",
                    help="Ruta donde guardar el CSV de salida")
args = parser.parse_args()

print("Paso 1: Creando datos iniciales...")
print(f"Output file: {args.output_path}")

# Crear un directorio para la salida si no existe  
os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

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
df.to_csv(args.output_path, index=False)

print(f"Datos iniciales guardados en {args.output_path}")
print(f"Archivo creado correctamente: {os.path.exists(args.output_path)}")
print(f"Tamaño del archivo: {os.path.getsize(args.output_path) if os.path.exists(args.output_path) else 'No existe'} bytes")
