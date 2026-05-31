from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# ─── Configuración de MySQL (Laragon) ───────────────────────────
app.config['MYSQL_HOST']     = '127.0.0.1'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'contabilidad2026'
app.config['MYSQL_PORT']     = 3306

mysql = MySQL(app)

# ─── Datos de la empresa ────────────────────────────────────────
empresa = {
    "nombre":    "Distribuidora Don Bosco",
    "nit":       "123456-7",
    "direccion": "Quetzaltenango, Guatemala",
    "giro":      "Distribución de productos electrónicos"
}

# ─── Página principal ────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('inventario'))

# ─── Ver inventario ──────────────────────────────────────────────
@app.route('/inventario')
def inventario():
    cur = mysql.connection.cursor()

    # Traer todas las cuentas con su tipo
    cur.execute("""
        SELECT c.idCuenta, c.nombreCuenta, c.descripcion, c.monto, t.nombreCuenta
        FROM Cuenta c
        JOIN TiposCuentas t ON c.idTipoCuenta = t.idTipoCuenta
        ORDER BY t.idTipoCuenta, c.idCuenta
    """)
    cuentas = cur.fetchall()

    # Traer tipos de cuentas para el formulario
    cur.execute("SELECT idTipoCuenta, nombreCuenta FROM TiposCuentas")
    tipos = cur.fetchall()

    cur.close()

    # Organizar por sección
    datos = {
        "Activo Corriente":    [],
        "Activo No Corriente": [],
        "Pasivo Corriente":    [],
        "Pasivo No Corriente": [],
        "Capital Contable":    []
    }
    for cuenta in cuentas:
        seccion = cuenta[4]
        if seccion in datos:
            datos[seccion].append({
                "id":          cuenta[0],
                "nombre":      cuenta[1],
                "descripcion": cuenta[2],
                "monto":       float(cuenta[3])
            })

    return render_template('inventario.html',
                        empresa=empresa,
                        datos=datos,
                        tipos=tipos)

# ─── Agregar cuenta ──────────────────────────────────────────────
@app.route('/agregar', methods=['POST'])
def agregar():
    nombre      = request.form['nombre']
    descripcion = request.form['descripcion']
    monto       = float(request.form['monto'])
    idTipo      = int(request.form['idTipoCuenta'])

    cur = mysql.connection.cursor()

    # Buscar o crear inventario de la empresa (usamos idEmpresa=1)
    cur.execute("SELECT idInventario FROM Inventario WHERE idEmpresa = 1")
    inv = cur.fetchone()
    if not inv:
        cur.execute("INSERT INTO Inventario (idEmpresa) VALUES (1)")
        mysql.connection.commit()
        idInventario = cur.lastrowid
    else:
        idInventario = inv[0]

    cur.execute("""
        INSERT INTO Cuenta (nombreCuenta, descripcion, monto, idTipoCuenta, idInventario)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, monto, idTipo, idInventario))

    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario'))

# ─── Eliminar cuenta ─────────────────────────────────────────────
@app.route('/eliminar', methods=['POST'])
def eliminar():
    idCuenta = int(request.form['idCuenta'])
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Cuenta WHERE idCuenta = %s", (idCuenta,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app.run(debug=True)