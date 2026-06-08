from Database.connection import get_db_connection

def obtener_inventario():
    conn = get_db_connection()
    cur = conn.cursor()
    # Usamos alias claros
    cur.execute("""
        SELECT c.idCuenta, c.nombreCuenta, c.descripcion, c.monto, t.nombreCuenta as seccion
        FROM Cuenta c
        JOIN TiposCuentas t ON c.idTipoCuenta = t.idTipoCuenta
        ORDER BY t.idTipoCuenta, c.idCuenta
    """)
    cuentas = cur.fetchall()

    cur.execute("SELECT idTipoCuenta, nombreCuenta FROM TiposCuentas")
    tipos = cur.fetchall()
    cur.close()
    conn.close()

    datos = {
        "Activo Corriente": [], "Activo No Corriente": [],
        "Pasivo Corriente": [], "Pasivo No Corriente": [],
        "Capital Contable": []
    }
    for cuenta in cuentas:
        # cuenta[4] es 'seccion'
        if cuenta[4] in datos:
            datos[cuenta[4]].append({
                "id": cuenta[0], "nombre": cuenta[1], 
                "descripcion": cuenta[2], "monto": float(cuenta[3])
            })
    return datos, tipos

def agregar_cuenta(nombre, descripcion, monto, idTipo):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT idInventario FROM Inventario WHERE idEmpresa = 1")
    inv = cur.fetchone()
    
    if not inv:
        cur.execute("INSERT INTO Inventario (idEmpresa) VALUES (1)")
        # En SQL Server, obtenemos el ID así:
        cur.execute("SELECT SCOPE_IDENTITY()")
        idInventario = cur.fetchone()[0]
        conn.commit()
    else:
        idInventario = inv[0]

    cur.execute("""
        INSERT INTO Cuenta (nombreCuenta, descripcion, monto, idTipoCuenta, idInventario)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, monto, idTipo, idInventario))

    conn.commit()
    cur.close()
    conn.close()

def eliminar_cuenta(idCuenta):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Cuenta WHERE idCuenta = ?", (idCuenta,))
    conn.commit()
    cur.close()
    conn.close()

def generar_partida_apertura():
    conn = get_db_connection()
    cur = conn.cursor()
    from datetime import date
    hoy = date.today()

    cur.execute("""
        SELECT idLibroDiario FROM LibroDiario 
        WHERE mes = ? AND year = ? AND idEmpresa = 1
    """, (hoy.month, hoy.year))
    libro = cur.fetchone()

    if not libro:
        cur.execute("""
            INSERT INTO LibroDiario (mes, year, idEmpresa)
            VALUES (?, ?, 1)
        """, (hoy.month, hoy.year))
        cur.execute("SELECT SCOPE_IDENTITY()")
        idLibro = cur.fetchone()[0]
        conn.commit()
    else:
        idLibro = libro[0]

    cur.execute("""
        SELECT idPartida FROM Partidas 
        WHERE noPartida = 1 AND idLibroDiario = ?
    """, (idLibro,))
    existe = cur.fetchone()

    if existe:
        cur.close()
        conn.close()
        return {"mensaje": "La partida de apertura ya existe", "existe": True}

    cur.execute("""
        INSERT INTO Partidas (noPartida, descripcionPartida, fechaPartida, idLibroDiario)
        VALUES (1, 'Partida de apertura - Inventario inicial', ?, ?)
    """, (hoy, idLibro))
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Partida generada", "existe": False}

def obtener_partida_apertura():
    conn = get_db_connection()
    cur = conn.cursor()
    from datetime import date
    hoy = date.today()

    cur.execute("""
        SELECT p.idPartida, p.noPartida, p.descripcionPartida, p.fechaPartida
        FROM Partidas p
        JOIN LibroDiario l ON p.idLibroDiario = l.idLibroDiario
        WHERE p.noPartida = 1 AND l.idEmpresa = 1
        AND l.mes = ? AND l.year = ?
    """, (hoy.month, hoy.year))
    partida = cur.fetchone()

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
    conn.close()
    return partida, cuentas