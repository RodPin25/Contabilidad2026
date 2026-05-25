from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# ─── Archivo donde se guarda todo ───────────────────────────────
ARCHIVO_DATOS = 'datos.json'

# ─── Datos de la empresa ────────────────────────────────────────
empresa = {
    "nombre":    "Distribuidora Don Bosco",
    "nit":       "123456-7",
    "direccion": "Quetzaltenango, Guatemala",
    "giro":      "Distribución de productos electrónicos"
}

# ─── Cargar datos desde archivo ─────────────────────────────────
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "activo_corriente":     [],
        "activo_no_corriente":  [],
        "pasivo_corriente":     [],
        "pasivo_no_corriente":  [],
        "capital":              []
    }

# ─── Guardar datos en archivo ───────────────────────────────────
def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

# ─── Página principal → redirige al inventario ──────────────────
@app.route('/')
def index():
    return redirect(url_for('inventario'))

# ─── Ver inventario ─────────────────────────────────────────────
@app.route('/inventario')
def inventario():
    datos = cargar_datos()
    return render_template('inventario.html', empresa=empresa, datos=datos)

# ─── Agregar partida ────────────────────────────────────────────
@app.route('/agregar', methods=['POST'])
def agregar():
    datos = cargar_datos()
    seccion = request.form['seccion']
    partida = {
        "codigo":      request.form['codigo'],
        "nombre":      request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "monto":       float(request.form['monto'])
    }
    datos[seccion].append(partida)
    guardar_datos(datos)
    return redirect(url_for('inventario'))

# ─── Eliminar partida ───────────────────────────────────────────
@app.route('/eliminar', methods=['POST'])
def eliminar():
    datos = cargar_datos()
    seccion = request.form['seccion']
    indice  = int(request.form['indice'])
    datos[seccion].pop(indice)
    guardar_datos(datos)
    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app.run(debug=True)