# 03_train_model.py
import pandas as pd
import json
import os
import argparse

parser = argparse.ArgumentParser(description="Entrena un modelo sencillo")
parser.add_argument("--input-data-path", default="/tmp/selected_columns.dat",
                    help="Ruta del CSV de entrada")
parser.add_argument("--output", default="/tmp/model.json", # El nombre específico del modelo se pasará como argumento en el workflow
                    help="Ruta del JSON con el modelo de salida")
args = parser.parse_args()

print("Paso 3: 'Entrenando' el modelo...")
os.makedirs(os.path.dirname(args.output), exist_ok=True)

df = pd.read_csv(args.input_data_path)

last_value = df['value1'].iloc[-1]
diff_mean = df['value1'].diff().mean()
diff_std = df['value1'].diff().std()

model_params = {
    'last_value': last_value,
    'mean_increment': diff_mean,
    'std_increment': diff_std
}

with open(args.output, 'w') as f:
    json.dump(model_params, f)

print(f"Modelo guardado en {args.output}")
