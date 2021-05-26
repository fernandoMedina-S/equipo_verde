import requests
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    diccionario = {}
    diccionario['empleado'] = 12345
    url = 'http://127.0.0.1:3000/requerir_historial_empleado'
    respuesta = requests.get(url, json=diccionario)
    espacios = json.loads(respuesta.text)
    listaPrincipal = []
    for i in range(0, len(espacios)):
        diccionarioAux = espacios[str(i+1)]
        listaAux = []
        for clave in diccionarioAux:
            listaAux.append(diccionarioAux[clave])
        listaPrincipal.append(listaAux)
    print(listaPrincipal)
    print(len(espacios))
    return render_template('index.html', espacios = listaPrincipal)

@app.route("/admin.html")
def admin():
    return render_template('admin.html')

@app.route("/recepcion.html")
def recepcion():
    return render_template('recepcion.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)