from Database.connection import get_db_connection
from datetime import date

def obtener_inventario():
    conn = get_db_connection()
    cur = conn.cursor()
    # Consulta optimizada para tu esquema actual
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
        # cuenta[4] es el nombre de la sección
        if cuenta[4] in datos:
            datos[cuenta[4]].append({
                "id": cuenta[0], 
                "nombre": cuenta[1], 
                "descripcion": cuenta[2], 
                "monto": float(cuenta[3])
            })
    return datos, tipos

def agregar_cuenta(nombre, descripcion, monto, idTipo):
    conn = get_db_connection()
    cur = conn.cursor()
    # Inserción directa según tu esquema
    cur.execute("""
        INSERT INTO Cuenta (nombreCuenta, descripcion, monto, idTipoCuenta)
        VALUES (?, ?, ?, ?)
    """, (nombre, descripcion, monto, idTipo))
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

    # 1. Buscar si ya existe el libro para este mes y año
    cur.execute("""
        SELECT idLibroDiario FROM LIBRODIARIO 
        WHERE mes = ? AND year = ? AND idEmpresa = 1
    """, (hoy.month, hoy.year))
    libro = cur.fetchone()

    if not libro:
        # Usamos OUTPUT para obtener el ID recién creado de forma más confiable
        cur.execute("""
            INSERT INTO LIBRODIARIO (mes, year, idEmpresa)
            OUTPUT INSERTED.idLibroDiario
            VALUES (?, ?, 1)
        """, (hoy.month, hoy.year))
        
        idLibro = int(cur.fetchone()[0])
    else:
        idLibro = libro[0]

    # 2. Verificar si ya existe la partida 1 en ese libro
    cur.execute("""
        SELECT idPartida FROM PARTIDAS 
        WHERE noPartida = 1 AND idLibroDiario = ?
    """, (idLibro,))
    existe = cur.fetchone()

    if existe:
        cur.close()
        conn.close()
        return {"mensaje": "La partida de apertura ya existe", "existe": True}

    # 3. Insertar la partida
    cur.execute("""
        INSERT INTO PARTIDAS (noPartida, descripcionPartida, fechaPartida, idLibroDiario)
        VALUES (1, 'Partida de apertura - Inventario inicial', ?, ?)
    """, (hoy, idLibro))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {"mensaje": "Partida de apertura generada exitosamente", "existe": False}

def obtener_partida_apertura():
    conn = get_db_connection()
    cur = conn.cursor()
    hoy = date.today()

    # Obtener cabecera de la partida
    cur.execute("""
        SELECT p.idPartida, p.noPartida, p.descripcionPartida, p.fechaPartida
        FROM Partidas p
        JOIN LibroDiario l ON p.idLibroDiario = l.idLibroDiario
        WHERE p.noPartida = 1 AND l.idEmpresa = 1
        AND l.mes = ? AND l.year = ?
    """, (hoy.month, hoy.year))
    partida = cur.fetchone()

    # Sumar montos por tipo de cuenta
    cur.execute("""
        SELECT t.nombreCuenta, SUM(c.monto) as total
        FROM Cuenta c
        JOIN TiposCuentas t ON c.idTipoCuenta = t.idTipoCuenta
        GROUP BY t.nombreCuenta, t.idTipoCuenta
        ORDER BY t.idTipoCuenta
    """)
    res_cuentas = cur.fetchall()
    cur.close()
    conn.close()

    # Procesar para que el HTML reciba listas con Debe y Haber
    cuentas_procesadas = []
    for c in res_cuentas:
        nombre_tipo = c[0]
        monto = float(c[1])
        if nombre_tipo in ['Activo Corriente', 'Activo No Corriente']:
            # Estructura: (Nombre, Debe, Haber)
            cuentas_procesadas.append((nombre_tipo, monto, 0))
        else:
            cuentas_procesadas.append((nombre_tipo, 0, monto))

    return partida, cuentas_procesadas