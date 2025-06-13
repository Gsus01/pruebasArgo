# 04_generate_data.py
import pandas as pd
import numpy as np
import json
import os
import argparse

parser = argparse.ArgumentParser(description="Genera datos sintéticos a partir de un modelo")
parser.add_argument("--input", default="/tmp/model.json", # El nombre específico del modelo se pasará como argumento en el workflow
                    help="Ruta del JSON con el modelo de entrada")
parser.add_argument("--output", default="/tmp/synthetic_data.csv", # El nombre específico del csv se pasará como argumento en el workflow
                    help="Ruta donde guardar el CSV generado")
args = parser.parse_args()

print("Paso 4: Generando datos sintéticos...")
os.makedirs(os.path.dirname(args.output), exist_ok=True)

with open(args.input, 'r') as f:
    model_params = json.load(f)

num_points = 50
current_value = model_params['last_value']
mean_inc = model_params['mean_increment']
std_inc = model_params['std_increment']

new_values = []
for _ in range(num_points):
    increment = np.random.normal(loc=mean_inc, scale=std_inc)
    current_value += increment
    new_values.append(current_value)

new_timestamps = pd.to_datetime(pd.date_range(start='2025-04-11', periods=num_points, freq='D'))
df_synthetic = pd.DataFrame({'timestamp': new_timestamps, 'synthetic_value': new_values})

df_synthetic.to_csv(args.output, index=False)

print(f"Datos sintéticos generados y guardados en {args.output}")
