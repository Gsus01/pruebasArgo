# 02_select_columns.py
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description="Selecciona columnas del dataset")
parser.add_argument("--input", default="/tmp/data/raw_data.csv",
                    help="Ruta del CSV de entrada")
parser.add_argument("--output", default="/tmp/data/selected_data.csv",
                    help="Ruta del CSV de salida")
args = parser.parse_args()

print("Paso 2: Seleccionando columnas...")
os.makedirs(os.path.dirname(args.output), exist_ok=True)

df = pd.read_csv(args.input)

df_selected = df[['timestamp', 'value1']]

df_selected.to_csv(args.output, index=False)

print(f"Columnas seleccionadas y guardadas en {args.output}")
