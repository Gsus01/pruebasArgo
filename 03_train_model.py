# 03_train_model.py
import pandas as pd
import json
import os

print("Paso 3: 'Entrenando' el modelo...")
os.makedirs('/tmp/data', exist_ok=True)

input_path = '/tmp/data/selected_data.csv'
df = pd.read_csv(input_path)

# Modelo "tonto": se basa en el último valor y la media/std de los cambios
last_value = df['value1'].iloc[-1]
diff_mean = df['value1'].diff().mean()
diff_std = df['value1'].diff().std()

model_params = {
    'last_value': last_value,
    'mean_increment': diff_mean,
    'std_increment': diff_std
}

# Guardamos los parámetros del "modelo" en un JSON
output_path = '/tmp/data/model.json'
with open(output_path, 'w') as f:
    json.dump(model_params, f)

print(f"Modelo guardado en {output_path}")