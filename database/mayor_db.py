from Database.connection import get_db_connection # Importamos nuestra función de conexión

def obtener_cuentas_con_movimientos(id_cuenta=None, fecha_inicio=None, fecha_fin=None):
    condiciones = []
    parametros = []

    # Ajuste: pyodbc usa '?' en lugar de '%s'
    if id_cuenta is not None:
        condiciones.append("c.idCuenta = ?")
        parametros.append(id_cuenta)
    if fecha_inicio is not None:
        condiciones.append("p.fechaPartida >= ?")
        parametros.append(fecha_inicio)
    if fecha_fin is not None:
        condiciones.append("p.fechaPartida <= ?")
        parametros.append(fecha_fin)

    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
    
    query = f"""
        SELECT
            c.idCuenta, c.nombreCuenta, tc.idTipoCuenta, tc.nombreCuenta as nombreTipo,
            p.idPartida, p.noPartida, p.fechaPartida, p.descripcionPartida,
            a.idAsiento, a.debe, a.haber
        FROM AsientoDiario a
        JOIN Partidas p ON a.idPartida = p.idPartida
        JOIN Cuenta c ON a.idCuenta = c.idCuenta
        JOIN TiposCuentas tc ON c.idTipoCuenta = tc.idTipoCuenta
        {where}
        ORDER BY c.idCuenta, p.fechaPartida, p.noPartida, a.idAsiento
    """

    conn = get_db_connection() # Nueva forma de conectar
    cur = conn.cursor()
    try:
        cur.execute(query, tuple(parametros))
        # Para que sea más fácil de usar en el frontend, devolvemos como lista de diccionarios
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close() # Siempre cerrar conexión en SQL Server

def obtener_cuentas_disponibles():
    query = """
        SELECT DISTINCT
            c.idCuenta, c.nombreCuenta, tc.idTipoCuenta, tc.nombreCuenta as nombreTipo
        FROM Cuenta c
        JOIN TiposCuentas tc ON c.idTipoCuenta = tc.idTipoCuenta
        JOIN AsientoDiario a ON c.idCuenta = a.idCuenta
        ORDER BY c.idCuenta
    """

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()