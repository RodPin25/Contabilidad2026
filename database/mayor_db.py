from database.connection import mysql


def obtener_cuentas_con_movimientos(id_cuenta=None, fecha_inicio=None, fecha_fin=None):
    """Obtiene los movimientos del diario necesarios para construir el mayor."""
    condiciones = []
    parametros = []

    if id_cuenta is not None:
        condiciones.append("c.idCuenta = %s")
        parametros.append(id_cuenta)
    if fecha_inicio is not None:
        condiciones.append("p.fechaPartida >= %s")
        parametros.append(fecha_inicio)
    if fecha_fin is not None:
        condiciones.append("p.fechaPartida <= %s")
        parametros.append(fecha_fin)

    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
    query = f"""
        SELECT
            c.idCuenta,
            c.nombreCuenta,
            tc.idTipoCuenta,
            tc.nombreCuenta,
            p.idPartida,
            p.noPartida,
            p.fechaPartida,
            p.descripcionPartida,
            a.idAsiento,
            a.debe,
            a.haber
        FROM AsientoDiario a
        JOIN Partidas p ON a.idPartida = p.idPartida
        JOIN Cuenta c ON a.idCuenta = c.idCuenta
        JOIN TiposCuentas tc ON c.idTipoCuenta = tc.idTipoCuenta
        {where}
        ORDER BY c.idCuenta, p.fechaPartida, p.noPartida, a.idAsiento
    """

    cur = mysql.connection.cursor()
    try:
        cur.execute(query, tuple(parametros))
        return cur.fetchall()
    finally:
        cur.close()


def obtener_cuentas_disponibles():
    """Lista las cuentas que poseen al menos un asiento registrado."""
    query = """
        SELECT DISTINCT
            c.idCuenta,
            c.nombreCuenta,
            tc.idTipoCuenta,
            tc.nombreCuenta
        FROM Cuenta c
        JOIN TiposCuentas tc ON c.idTipoCuenta = tc.idTipoCuenta
        JOIN AsientoDiario a ON c.idCuenta = a.idCuenta
        ORDER BY c.idCuenta
    """

    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        return cur.fetchall()
    finally:
        cur.close()
