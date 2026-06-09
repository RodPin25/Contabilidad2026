from Database.connection import get_db_connection
from datetime import datetime

def database_guardar_partida(numero_partida, fecha, descripcion, tipo_partida, detalles):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if isinstance(fecha, str):
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        else:
            fecha_dt = fecha
        
        mes, year = fecha_dt.month, fecha_dt.year

        # 1. Obtener o crear LibroDiario
        cur.execute("SELECT idLibroDiario FROM LIBRODIARIO WHERE mes = ? AND year = ? AND idEmpresa = 1", (mes, year))
        libro = cur.fetchone()

        if not libro:
            cur.execute("INSERT INTO LIBRODIARIO (mes, year, idEmpresa) OUTPUT INSERTED.idLibroDiario VALUES (?, ?, 1)", (mes, year))
            id_libro = cur.fetchone()[0]
        else:
            id_libro = libro[0]

        # 2. Registrar encabezado en PARTIDAS
        cur.execute("""
            INSERT INTO PARTIDAS (noPartida, descripcionPartida, fechaPartida, idLibroDiario)
            OUTPUT INSERTED.idPartida
            VALUES (?, ?, ?, ?)
        """, (numero_partida, descripcion, fecha, id_libro))
        id_partida_generado = cur.fetchone()[0]
        
        # 3. Registrar detalles en PARTIDA_CONTIENE_CUENTA (tabla puente correcta)
        # Ajusta los nombres de columnas (debe, haber) si en tu tabla se llaman distinto
        query_detalle = """
            INSERT INTO PARTIDA_CONTIENE_CUENTA (idPartida, idCuenta, debe, haber)
            VALUES (?, ?, ?, ?)
        """
        for d in detalles:
            cur.execute(query_detalle, (id_partida_generado, d['idCuenta'], d['debe'], d['haber']))
            
        conn.commit()
        return True
    except Exception as err:
        conn.rollback()
        raise Exception(f"Error en Capa Database: {str(err)}")
    finally:
        cur.close()
        conn.close()

def database_obtener_libro_diario():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT p.noPartida, p.fechaPartida, p.descripcionPartida, 
                   pc.idCuenta, c.nombreCuenta, pc.debe, pc.haber
            FROM PARTIDAS p
            JOIN PARTIDA_CONTIENE_CUENTA pc ON p.idPartida = pc.idPartida
            JOIN CUENTA c ON pc.idCuenta = c.idCuenta
            ORDER BY p.noPartida ASC
        """
        cur.execute(query)
        return [{"numero_partida": f[0], "fecha": str(f[1]), "descripcion": f[2], 
                 "codigo_cuenta": f[3], "nombre_cuenta": f[4], "debe": float(f[5]), "haber": float(f[6])} 
                for f in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def database_obtener_libro_mayor():
    conn = get_db_connection()
    cur = conn.cursor()
    try: 
        query = """
            SELECT pc.idCuenta, c.nombreCuenta, SUM(pc.debe), SUM(pc.haber), 
                   (SUM(pc.debe) - SUM(pc.haber))
            FROM PARTIDA_CONTIENE_CUENTA pc
            JOIN CUENTA c ON pc.idCuenta = c.idCuenta
            GROUP BY pc.idCuenta, c.nombreCuenta
        """
        cur.execute(query)
        return [{"codigo_cuenta": f[0], "nombre_cuenta": f[1], "total_debe": float(f[2]), 
                 "total_haber": float(f[3]), "saldo_actual": float(f[4])} 
                for f in cur.fetchall()]
    finally:
        cur.close()
        conn.close()