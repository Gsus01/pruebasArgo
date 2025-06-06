from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Este es el mensaje que veremos en el navegador
    return "¡Hola Mundo desde Python, desplegado con Argo CD!"

if __name__ == '__main__':
    # Escuchamos en 0.0.0.0 para que sea accesible desde fuera del contenedor
    # Usamos el puerto 8080
    app.run(host='0.0.0.0', port=8080)