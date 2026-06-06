from database.connection import mysql

# Acá se obtienen todas las cuentas organizadas por sección 
def obtener_inventario():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.idCuenta, c.nombreCuenta, c.descripcion, c.monto, t.nombreCuenta
        FROM Cuenta c
        JOIN TiposCuentas t ON c.idTipoCuenta = t.idTipoCuenta
        ORDER BY t.idTipoCuenta, c.idCuenta
    """)
    cuentas = cur.fetchall()

    cur.execute("SELECT idTipoCuenta, nombreCuenta FROM TiposCuentas")
    tipos = cur.fetchall()
    cur.close()

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

    return datos, tipos

# Acá agregamos las cuentas 
def agregar_cuenta(nombre, descripcion, monto, idTipo):
    cur = mysql.connection.cursor()

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

# Acá eliminamos las cuentas 
def eliminar_cuenta(idCuenta):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Cuenta WHERE idCuenta = %s", (idCuenta,))
    mysql.connection.commit()
    cur.close()
    
# ─── Generar Partida 1 - Apertura ────────────────────────────────
def generar_partida_apertura():
    cur = mysql.connection.cursor()

    # Verificar si ya existe un libro diario para este mes
    from datetime import date
    hoy = date.today()

    cur.execute("""
        SELECT idLibroDiario FROM LibroDiario 
        WHERE mes = %s AND year = %s AND idEmpresa = 1
    """, (hoy.month, hoy.year))
    libro = cur.fetchone()

    if not libro:
        cur.execute("""
            INSERT INTO LibroDiario (mes, year, idEmpresa)
            VALUES (%s, %s, 1)
        """, (hoy.month, hoy.year))
        mysql.connection.commit()
        idLibro = cur.lastrowid
    else:
        idLibro = libro[0]

    # Verificar si ya existe la partida 1
    cur.execute("""
        SELECT idPartida FROM Partidas 
        WHERE noPartida = 1 AND idLibroDiario = %s
    """, (idLibro,))
    existe = cur.fetchone()

    if existe:
        cur.close()
        return {"mensaje": "La partida de apertura ya existe", "existe": True}

    # Crear la partida 1
    cur.execute("""
        INSERT INTO Partidas (noPartida, descripcionPartida, fechaPartida, idLibroDiario)
        VALUES (1, 'Partida de apertura - Inventario inicial', %s, %s)
    """, (hoy, idLibro))
    mysql.connection.commit()
    cur.close()

    return {"mensaje": "Partida de apertura generada exitosamente", "existe": False}


# ─── Obtener Partida 1 para mostrar ──────────────────────────────
def obtener_partida_apertura():
    cur = mysql.connection.cursor()
    from datetime import date
    hoy = date.today()

    cur.execute("""
        SELECT p.idPartida, p.noPartida, p.descripcionPartida, p.fechaPartida
        FROM Partidas p
        JOIN LibroDiario l ON p.idLibroDiario = l.idLibroDiario
        WHERE p.noPartida = 1 AND l.idEmpresa = 1
        AND l.mes = %s AND l.year = %s
    """, (hoy.month, hoy.year))
    partida = cur.fetchone()

    # Traer cuentas del inventario agrupadas
    cur.execute("""
        SELECT t.nombreCuenta, SUM(c.monto) as total
        FROM Cuenta c
        JOIN TiposCuentas t ON c.idTipoCuenta = t.idTipoCuenta
        JOIN Inventario i ON c.idInventario = i.idInventario
        WHERE i.idEmpresa = 1
        GROUP BY t.nombreCuenta, t.idTipoCuenta
        ORDER BY t.idTipoCuenta
    """)
    cuentas = cur.fetchall()
    cur.close()

    return partida, cuentas