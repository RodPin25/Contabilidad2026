from flask import render_template, request, redirect, url_for
from services.inventario_service import (
    obtener_inventario,
    agregar_cuenta,
    eliminar_cuenta,
    generar_partida_apertura,
    obtener_partida_apertura
)

# Datos de la empresa
empresa = {
    "nombre":    "Distribuidora Don Bosco",
    "nit":       "123456-7",
    "direccion": "Quetzaltenango, Guatemala",
    "giro":      "Distribución de productos electrónicos"
}

# Nuestra función para ver nuestro inventario 
def ctrl_ver_inventario():
    datos, tipos = obtener_inventario()
    partida, cuentas_partida = obtener_partida_apertura()
    return render_template('inventario.html',
                        empresa=empresa,
                        datos=datos,
                        tipos=tipos,
                        partida=partida,
                        cuentas_partida=cuentas_partida)

# Nuestra función para crear una cuenta 
def ctrl_agregar_cuenta():
    nombre      = request.form['nombre']
    descripcion = request.form['descripcion']
    monto       = float(request.form['monto'])
    idTipo      = int(request.form['idTipoCuenta'])
    agregar_cuenta(nombre, descripcion, monto, idTipo)
    return redirect(url_for('inventario.ver_inventario'))

# Nuestra función para eliminar una cuenta 
def ctrl_eliminar_cuenta():
    idCuenta = int(request.form['idCuenta'])
    eliminar_cuenta(idCuenta)
    return redirect(url_for('inventario.ver_inventario'))

# Nuestra función para generar la partida de apertura
def ctrl_generar_partida_apertura():
    resultado = generar_partida_apertura()
    return redirect(url_for('inventario.ver_inventario'))

# Nuestra partida pata obtener la partida de apertura (si existe)
def ctrl_obtener_partida_apertura():
    partida, cuentas = obtener_partida_apertura()
    return partida, cuentas