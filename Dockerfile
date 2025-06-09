FROM python:3.9-slim

# Instalar dependencias
RUN pip install pandas numpy

# Copiar todos nuestros scripts
COPY . /app
WORKDIR /app