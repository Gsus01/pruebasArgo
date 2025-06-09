# 04_generate_data.py
import pandas as pd
import numpy as np
import json
import os

print("Paso 4: Generando datos sintéticos...")
os.makedirs('/tmp/data', exist_ok=True)

input_path = '/tmp/data/model.json'
with open(input_path, 'r') as f:
    model_params = json.load(f)

# Generamos 50 nuevos puntos
num_points = 50
current_value = model_params['last_value']
mean_inc = model_params['mean_increment']
std_inc = model_params['std_increment']

new_values = []
for _ in range(num_points):
    increment = np.random.normal(loc=mean_inc, scale=std_inc)
    current_value += increment
    new_values.append(current_value)

# Creamos un nuevo DataFrame
new_timestamps = pd.to_datetime(pd.date_range(start='2025-04-11', periods=num_points, freq='D'))
df_synthetic = pd.DataFrame({'timestamp': new_timestamps, 'synthetic_value': new_values})

# Guardamos el resultado final
output_path = '/tmp/data/synthetic_data.csv'
df_synthetic.to_csv(output_path, index=False)

print(f"Datos sintéticos generados y guardados en {output_path}")