from types import MethodDescriptorType
from flask.helpers import url_for
from pymysql.cursors import DictCursorMixin
import requests
import json
from flask import Flask, render_template, jsonify, request, redirect

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    diccionario = {}
    diccionario['empleado'] = 12345
    url = 'http://127.0.0.1:3000/Requerir_lugares'
    respuesta = requests.get(url, json=diccionario)
    espacios = json.loads(respuesta.text)
    listaPrincipal = []
    for i in range(0, len(espacios)):
        diccionarioAux = espacios[str(i+1)]
        listaAux = []
        for clave in diccionarioAux:
            listaAux.append(diccionarioAux[clave])
        listaPrincipal.append(listaAux)

    
    return render_template('index.html', espacios = listaPrincipal)

@app.route("/admin.html")
def admin():
    diccionario = {}
    diccionario['empleado'] = 2345
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

    
    #Historial general
    diccionarioGeneral = {}
    diccionarioGeneral['empleado'] = 12345
    urlGeneral = 'http://127.0.0.1:3000/requerir_historial_general'
    respuestaGeneral = requests.get(urlGeneral, json=diccionarioGeneral)
    historial = json.loads(respuestaGeneral.text)
    listaPrincipalG = []
    for i in range(0, len(historial)):
        diccionarioAuxGeneral = historial[str(i)]
        listaAuxG = []
        for claveG in diccionarioAuxGeneral:
            listaAuxG.append(diccionarioAuxGeneral[claveG])
        listaPrincipalG.append(listaAuxG)
    print(listaPrincipalG[0])

    return render_template('admin.html', espacios = listaPrincipal ,historial = listaPrincipalG)

@app.route("/recepcion.html")
def recepcion():
    return render_template('recepcion.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/apartarLugar", methods = ['POST'])
def apartarLugar():
    empleado = request.form['empleado']
    espacio = request.form['espacio']
    fecha = request.form['fecha']

    diccionario = {}
    diccionario['empleado_apartado'] = empleado
    diccionario['espacio_apartado'] = espacio
    diccionario['fecha_apartado'] = fecha
    url = "http://127.0.0.1:3000/apartar_lugar"
    respuesta = requests.post(url, json=diccionario)

    #print(diccionario)
    return redirect(url_for("index"))

@app.route("/agregarEmpleado", methods = ['POST'])
def agregarEmpleado():
    idEmpleado = request.form['empleado']
    nombreEmpleado = request.form['nombre']
    adminEmpleado = request.form['admin']

    diccionario = {}
    diccionario['num_empleado'] = idEmpleado
    diccionario['nombre_empleado'] = nombreEmpleado
    diccionario['admin'] = adminEmpleado
    url = "http://127.0.0.1:3000/agregar_empleado"
    respuesta = requests.post(url, json=diccionario)

    print(diccionario)
    return redirect(url_for("admin"))

if __name__ == '__main__':
    app.run(debug = True)