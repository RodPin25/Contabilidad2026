from Database.connection import get_db_connection # Importamos nuestra función de conexión

def obtener_cuentas_con_movimientos(id_cuenta=None, fecha_inicio=None, fecha_fin=None):
    condiciones = []
    parametros = []

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
    
    # IMPORTANTE: Eliminé el comentario y añadí {where} al final
    query = f"""
        SELECT 
            c.idCuenta, c.nombreCuenta, p.fechaPartida, 
            p.noPartida, p.descripcionPartida, pc.debe, pc.haber
        FROM PARTIDA_CONTIENE_CUENTA pc
        INNER JOIN Partidas p ON pc.idPartida = p.idPartida -- Aseguramos que la partida exista
        JOIN Cuenta c ON pc.idcuenta = c.idCuenta
        WHERE p.descripcionPartida IS NOT NULL 
          AND p.descripcionPartida <> '' -- Excluimos registros vacíos
          {where} -- Aquí concatenas tu filtro dinámico
        ORDER BY p.fechaPartida, p.noPartida
    """

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Pasamos los parámetros aquí
        cur.execute(query, tuple(parametros))
        columns = [column[0] for column in cur.description]
        data = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        # --- AGREGA ESTO ---
        print("DEBUG DB:", data[:1]) # Imprime la primera fila para ver si tiene 'descripcionPartida'
        # -------------------
        
        return data
    except Exception as e:
        print(f"Error en SQL: {e}") # Esto te dirá si hay error de columna
        return []
    finally:
        cur.close()
        conn.close()

def obtener_cuentas_disponibles():
    query = """
        SELECT DISTINCT
            c.idCuenta, c.nombreCuenta, tc.idTipoCuenta, tc.nombreCuenta as nombreTipo
        FROM Cuenta c
        JOIN TiposCuentas tc ON c.idTipoCuenta = tc.idTipoCuenta
        JOIN PARTIDA_CONTIENE_CUENTA pc ON c.idCuenta = pc.idcuenta
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