from typing import Tuple
from flask import Flask, render_template, request, url_for, redirect, flash, session, make_response, jsonify
from jinja2.utils import consume
import pymysql


app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(host='equipoverde.mysql.pythonanywhere-services.com',
                                user='equipoverde',
                                password='rootroot',
                                db='equipoverde$default')

# def obtener_conexion():
#     return pymysql.connect(host='localhost',
#                                 user='root',
#                                 password='',
#                                 db='coffice')

@app.route("/")
def Index():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM Espacio JOIN Tipo_Espacio ON Espacio.Tipo = idTipo"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    return str(datos)


@app.route("/requerir_historial_empleado")
def Requerir_empleado():
    datos_pedir = request.get_json()
    empleado = datos_pedir["empleado"]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "select Empleado.idEmpleado, Empleado.Nombre, Espacio.Nombre, Fecha from Empleado join Registro on Empleado.idEmpleado = Registro.Empleado join Espacio on Espacio.idEspacio = Registro.Lugar where Empleado.idEmpleado = {0};".format(empleado)
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    dict = {}

    if(len(datos) == 0):
        return jsonify({"0":"Datos no encontrados"}), 404

    for i in range (0, len(datos)):
        dict_aux = {}

        dict_aux["idEmpleado"] = datos[i][0]
        dict_aux["NombreEmpleado"] = datos[i][1]
        dict_aux["NombreEspacio"] = datos[i][2]
        dict_aux["Fecha"] = datos[i][3]

        dict[str(i + 1)]=dict_aux


    return jsonify(dict), 200


@app.route("/agregar_empleado", methods=["POST"])
def Agregar_empleado():
    empleado_detalles = request.get_json()
    num_empleado = str(empleado_detalles["num_empleado"])
    nombre_empleado = str(empleado_detalles["nombre_empleado"])
    admin = str(empleado_detalles["admin"])

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "INSERT INTO Empleado (idEmpleado, Nombre, Admin) VALUES ('{0}', '{1}', '{2}')".format(num_empleado, nombre_empleado, admin)
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
    except:
        return jsonify({"EmpleadoAgregado":False}), 401

    return jsonify({"EmpleadoAgregado":True}), 201

@app.route("/agregar_espacio", methods=["POST"])
def agregar_espacio():
    espacio_detalles = request.get_json()
    capacidad_espacio = espacio_detalles["capacidad_espacio"]
    nombre_espacio = espacio_detalles["nombre_espacio"]
    tipo_espacio = espacio_detalles["tipo_espacio"]

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT idTipo FROM Tipo_Espacio WHERE Tipo = '{0}'".format(tipo_espacio)
        cursor.execute(consulta)
        datos_tipo = cursor.fetchall()
        tipo_espacio = datos_tipo[0][0]

        consulta = "INSERT INTO Espacio (Capacidad, Nombre, Tipo) VALUES ('{0}', '{1}', '{2}')".format(capacidad_espacio, nombre_espacio, tipo_espacio)
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
        flash('Lugar apartado exitosamente')
    except:
        return jsonify({"EspacioAgregado":False}), 401

    return jsonify({"EspacioAgregado":True}), 201

@app.route("/apartar_lugar", methods=["POST"])
def Apartar_lugar():
    reserva_detalles = request.get_json()
    empleado_apartado = reserva_detalles["empleado_apartado"]
    espacio_apartado = reserva_detalles["espacio_apartado"]
    fecha_apartado = reserva_detalles["fecha_apartado"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()


    try:
        consulta = "SELECT idEspacio from Espacio where Nombre = '{0}'".format(espacio_apartado)
        cursor.execute(consulta)
        nombre_espacio = cursor.fetchall()


        espacio_apartado = nombre_espacio[0][0]

        consulta = "INSERT INTO Registro (Empleado, Lugar, Fecha) VALUES ('{0}', '{1}', '{2}')".format(empleado_apartado, espacio_apartado, fecha_apartado)
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
    except:
        return jsonify({"ApartadoAgregado":False}), 401

    return jsonify({"ApartadoAgregado":True}), 201

@app.route("/Requerir_lugares")
def Lugares_disponibles():
    espacio = request.get_json()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "select * from Espacio ;".format(espacio)
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()
    dict = {}

    if(len(datos) == 0):
        return jsonify({"0":"Datos no encontrados"}), 404

    for i in range (0, len(datos)):
        dict_aux = {}

        dict_aux["idEspacio"] = datos[i][0]
        dict_aux["Capacidad"] = datos[i][1]
        dict_aux["Nombre"] = datos[i][2]
        dict_aux["Tipo"] = datos[i][3]

        dict[str(i + 1)]=dict_aux


    return jsonify(dict), 200

@app.route("/requerir_estado_espacio")
def Requerir_sala():
    datos_solicitados = request.get_json()
    espacio_pedido = datos_solicitados["espacio"]
    fecha_pedida = datos_solicitados["fecha"]

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "select count(*) from Registro join Espacio on idEspacio = Lugar where Fecha = '" + str(fecha_pedida) + "' and Nombre = '" + str(espacio_pedido) + "'"
        cursor.execute(consulta)
        ocupados = cursor.fetchall()

        consulta = "select Capacidad from Espacio where Nombre = '" + str(espacio_pedido) + "'"
        cursor.execute(consulta)
        totales = cursor.fetchall()
        espacios_restantes = int(totales[0][0]) - int(ocupados[0][0])
        conexion.close()
    except:
        return jsonify({"libres":"Error"}), 404

    return jsonify({"libres":espacios_restantes}), 200

@app.route("/requerir_historial_general")
def Requerir_registro():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "select Empleado.idEmpleado, Empleado.Nombre, Espacio.Nombre, Fecha from Registro join Espacio on Registro.Lugar = Espacio.idEspacio join Empleado on Registro.Empleado = Empleado.idEmpleado order by Fecha;"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conexion.close()

    dict = {}

    for i in range(0, len(datos)):
        dict_aux = {}
        dict_aux["idEmpleado"] = datos[i][0]
        dict_aux["NombreEmpleado"] = datos[i][1]
        dict_aux["NombreLugar"] = datos[i][2]
        dict_aux["Fecha"] = datos[i][3]

        dict[str(i)]=dict_aux

    return jsonify(dict), 200

@app.route("/modificar_empleado", methods=["PUT"])
def modificar_empleado():
    datos_nuevos=request.get_json()
    num_empleado=datos_nuevos["num_empleado"]
    nombre_empleado = datos_nuevos["nombre_empleado"]
    admin=datos_nuevos["admin"]

    try:
        consulta = "update Empleado set Nombre = '" + str(nombre_empleado) +"' where idEmpleado = '"+str(num_empleado)+"';"
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()

        consulta = "update Empleado set Admin = '" + str(admin) +"' where idEmpleado = '"+str(num_empleado)+"';"

        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
    except:
        return jsonify({"actualizado":False}), 400

    return jsonify({"actualizado":True}), 201

@app.route("/modificar_espacio", methods=["PUT"])
def modificar_espacio():
    datos_espacio = request.get_json()
    nombre_original = datos_espacio["nombre_original"]
    nombre_cambiar = datos_espacio["nombre_cambiar"]
    tipo = datos_espacio["tipo"]
    capacidad = datos_espacio["capacidad"]

    try:
        consulta = "select idEspacio from Espacio where Nombre = '{0}';".format(nombre_original)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        idEspacio = cursor.fetchall()
        print("\n\n\n", idEspacio)

        consulta = "select idTipo from Tipo_Espacio where Tipo = '{0}';".format(tipo)
        cursor.execute(consulta)
        idTipo = cursor.fetchall()

        consulta = "update Espacio set Nombre = '{0}' where idEspacio = {1}".format(nombre_cambiar, idEspacio[0][0])
        cursor.execute(consulta)
        conexion.commit()

        consulta = "update Espacio set Tipo = {0} where idEspacio = {1}".format(idTipo[0][0], idEspacio[0][0])
        cursor.execute(consulta)
        conexion.commit()

        consulta = "update Espacio set Capacidad = {0} where idEspacio = {1};".format(capacidad, idEspacio[0][0])
        cursor.execute(consulta)
        conexion.commit()
    except:
        return jsonify({"actualizado":False}), 400

    return jsonify({"actualizado":True}), 201

@app.route("/modificar_registro", methods=["PUT"])
def modificar_registro():
    datos_registro = request.get_json()
    idRegistro = datos_registro["idRegistro"]
    empleado = datos_registro["empleado"]
    lugar = datos_registro["nombre_sala"]
    fecha = datos_registro["fecha"]

    return "xD"

@app.route("/requerir_espacios")
def requerir_salas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT idEspacio, Nombre FROM Espacio"
    cursor.execute(consulta)

    datos = cursor.fetchall()
    conexion.close()
    dict = {}

    if(len(datos) == 0):
        return jsonify({"0":"Datos no encontrados"}), 404

    for i in range (0, len(datos)):
        dict_aux = {}

        dict_aux["ID"] = datos[i][0]
        dict_aux["nombre"] = datos[i][1]

        dict[str(i + 1)] = dict_aux

    return jsonify(dict), 200

@app.route("/es_admin")
def es_admin():
    datos = request.get_json()
    empleado = datos["empleado"]
    consulta = "select admin from Empleado where idEmpleado = " + str(empleado) + ";"
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(consulta)
    admin = cursor.fetchall()

    if(len(admin) == 0):
        return jsonify({"admin":"No encontrado"}), 404
    

    return jsonify({"admin":str(admin[0][0])}), 200


if __name__ == "__main__":
    app.run(port = 3000, debug = True)