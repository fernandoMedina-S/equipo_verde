from flask import Flask, render_template, request, url_for, redirect, flash, session
import pymysql


app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='coffice')


@app.route("/")
def Index():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM espacio JOIN tipo_espacio ON Espacio.Tipo = idTipo"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)

@app.route("/requerir_historial_empleado/<int:id_empleado>", methods=["GET"]) 
def Requerir_empleado(id_empleado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM registro JOIN Empleado ON Empleado.idEmpleado = registro.Empleado"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)


@app.route("/pito")
def Pito():
    x="12xd" + "zS"
    return x

if __name__ == "__main__":
    app.run(port = 3000, debug = True)