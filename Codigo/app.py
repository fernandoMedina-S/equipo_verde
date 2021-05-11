from flask import Flask, render_template, request, url_for, redirect, flash, session
import pymysql
import jsonify


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

@app.route("/agregar_empleado", methods=["POST"])
def Agregar_empleado():
    empleado_detalles = request.get_json()
    num_empleado = str(empleado_detalles["num_empleado"])
    nombre_empleado = str(empleado_detalles["nombre_empleado"])
    admin = str(empleado_detalles["admin"])

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "INSERT INTO empleado (idEmpleado, Nombre, Admin) VALUES ('{0}', '{1}', '{2}')".format(num_empleado, nombre_empleado, admin)
    cursor.execute(consulta)
    conexion.commit()
    conexion.close()

    return "Datos recibidos: " + str(empleado_detalles)

@app.route("/agregar_espacio", methods=["POST"])
def agregar_espacio():
    espacio_detalles = request.get_json()
    capacidad_espacio = espacio_detalles["capacidad_espacio"]
    nombre_espacio = espacio_detalles["nombre_espacio"]
    tipo_espacio = espacio_detalles["tipo_espacio"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT idTipo FROM tipo_espacio WHERE Tipo = '{0}'".format(tipo_espacio)
    cursor.execute(consulta)
    datos_tipo = cursor.fetchall()
    tipo_espacio = datos_tipo[0][0]

    consulta = "INSERT INTO espacio (Capacidad, Nombre, Tipo) VALUES ('{0}', '{1}', '{2}')".format(capacidad_espacio, nombre_espacio, tipo_espacio)
    cursor.execute(consulta)
    conexion.commit()
    conexion.close()

    return str(espacio_detalles)

@app.route("/apartar_lugar", methods=["POST"])
def Apartar_lugar():
    reserva_detalles = request.get_json()
    empleado_apartado = reserva_detalles["empleado_apartado"]
    espacio_apartado = reserva_detalles["espacio_apartado"]
    fecha_apartado = reserva_detalles["fecha_apartado"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    

    consulta = "SELECT idEspacio from Espacio where Nombre = '{0}'".format(espacio_apartado)
    cursor.execute(consulta)
    nombre_espacio = cursor.fetchall()
    print(consulta)

    espacio_apartado = nombre_espacio[0][0]

    consulta = "INSERT INTO registro (Empleado, Lugar, Fecha) VALUES ('{0}', '{1}', '{2}')".format(empleado_apartado, espacio_apartado, fecha_apartado)
    cursor.execute(consulta)
    conexion.commit()
    conexion.close()

    return str(reserva_detalles)

@app.route("/pito")
def Pito():
    x="12xd" + "zS"
    return x

if __name__ == "__main__":
    app.run(port = 3000, debug = True)