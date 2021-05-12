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


@app.route("/requerir_historial_empleado/<int:id_empleado>") 
def Requerir_empleado(id_empleado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM registro JOIN Empleado ON Empleado.idEmpleado = registro.Empleado"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)

    
@app.route("/requerir_estado_sala/<int:id_lugar>") 
def Requerir_sala(id_lugar):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM registro JOIN Espacio ON " + str(id_lugar) + "= registro.lugar"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)

@app.route("/requerir_historial_general/") 
def Requerir_registro():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM registro"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)


if __name__ == "__main__":
    app.run(port = 3000, debug = True)