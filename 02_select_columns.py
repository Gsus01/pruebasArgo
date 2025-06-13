# 02_select_columns.py
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description="Selecciona columnas del dataset")
parser.add_argument("--input-path", default="/tmp/initial_data.dat",
                    help="Ruta del CSV de entrada")
parser.add_argument("--output-path", default="/tmp/selected_columns.dat",
                    help="Ruta del CSV de salida")
args = parser.parse_args()

print("Paso 2: Seleccionando columnas...")
print(f"Input file: {args.input_path}")
print(f"Output file: {args.output_path}")

# Verificar que el archivo de entrada existe
if not os.path.exists(args.input_path):
    print(f"Error: El archivo de entrada {args.input_path} no existe")
    print("Archivos en /tmp:")
    if os.path.exists("/tmp"):
        print(os.listdir("/tmp"))
    else:
        print("El directorio /tmp no existe")
    exit(1)

# Crear directorio de salida si no existe
os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

df = pd.read_csv(args.input_path)

df_selected = df[['timestamp', 'value1']]

df_selected.to_csv(args.output_path, index=False)

print(f"Columnas seleccionadas y guardadas en {args.output_path}")
