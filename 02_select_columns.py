# 02_select_columns.py
import pandas as pd
import os

print("Paso 2: Seleccionando columnas...")
os.makedirs('/tmp/data', exist_ok=True)

# La ruta del artefacto de entrada la define Argo Workflows
input_path = '/tmp/data/raw_data.csv'
df = pd.read_csv(input_path)

# Seleccionamos solo las columnas que queremos para el modelo
df_selected = df[['timestamp', 'value1']]

# Guardamos el resultado como un nuevo artefacto
output_path = '/tmp/data/selected_data.csv'
df_selected.to_csv(output_path, index=False)

print(f"Columnas seleccionadas y guardadas en {output_path}")