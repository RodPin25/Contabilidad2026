from database.connection import mysql

# CAPA DATABASE - MODULO LIBRO DIARIO Y MAYOR pal muchacho aureo
# @jonas: en esta capa consumimos la conexion global compartida que inicializo tio soch.
# Modificamos los queries para apuntar a las tablas oficiales: 'partidas', 'cuenta' y 
# la nueva tabla intermedia 'AsientoDiario' para que no queden datos huerfanos.

def database_guardar_partida(numero_partida, fecha, descripcion, tipo_partida, detalles):
    """
    Inserta una transaccion completa utilizando una operacion transaccional de Flask (commit/rollback).
    Maneja la relacion Maestro-Detalle usando la tabla puente AsientoDiario.
    """
    cur = mysql.connection.cursor()
    try:
        # NOTA TECNICA: Primero registramos el encabezado en la tabla oficial 'partidas' del grupo.
        # Asumimos que idLibroDiario = 1 de manera predeterminada para el mes de trabajo.
        query_encabezado = """
            INSERT INTO partidas (noPartida, descripcionPartida, fechaPartida, idLibroDiario)
            VALUES (%s, %s, %s, 1)
        """
        cur.execute(query_encabezado, (numero_partida, descripcion, fecha))
        id_partida_generado = cur.lastrowid
        
        # NOTA DE INTEGRACION: Mapeamos los asientos contables en la tabla intermedia 'AsientoDiario'.
        # 'idCuenta' se amarra directamente con el inventario de Sochito.
        query_detalle = """
            INSERT INTO AsientoDiario (idPartida, idCuenta, debe, haber)
            VALUES (%s, %s, %s, %s)
        """
        for d in detalles:
            # Aceptamos tanto diccionarios nativos como objetos para maxima flexibilidad contable
            id_cuenta = d['idCuenta'] if isinstance(d, dict) else d.idCuenta
            debe = d['debe'] if isinstance(d, dict) else d.debe
            haber = d['haber'] if isinstance(d, dict) else d.haber
            cur.execute(query_detalle, (id_partida_generado, id_cuenta, debe, haber))
            
        mysql.connection.commit()
        return True
    except Exception as err:
        # @jonas: Si falla un solo asiento de la partida, tiramos rollback inmediato 
        # para que la contabilidad de la empresa no se descuadre en Laragon.
        mysql.connection.rollback()
        raise Exception(f"Error en Capa Database (Flask-MySQL): {str(err)}")
    finally:
        cur.close()

def database_obtener_libro_diario():
    """
    Extrae el historial completo cronologico de las partidas del Libro Diario.
    Realiza un JOIN para jalar los nombres de cuentas del modulo de inventario.
    """
    cur = mysql.connection.cursor()
    try:
        # @jonas: Cambiamos el JOIN hacia 'AsientoDiario' y 'cuenta' mapeando la estructura real.
        query = """
            SELECT p.noPartida as numero_partida, p.fechaPartida as fecha, p.descripcionPartida as descripcion,
                   a.idCuenta as codigo_cuenta, c.nombreCuenta as nombre_cuenta, a.debe, a.haber
            FROM partidas p
            JOIN AsientoDiario a ON p.idPartida = a.idPartida
            JOIN cuenta c ON a.idCuenta = c.idCuenta
            ORDER BY p.noPartida ASC, a.idAsiento ASC
        """
        cur.execute(query)
        filas = cur.fetchall()
        
        # Convertimos las tuplas de Flask a diccionarios limpios para el frontend de Aureo
        resultado = []
        for f in filas:
            resultado.append({
                "numero_partida": f[0],
                "fecha": str(f[1]),
                "descripcion": f[2],
                "codigo_cuenta": f[3],
                "nombre_cuenta": f[4],
                "debe": float(f[5]),
                "haber": float(f[6])
            })
        return resultado
    finally:
        cur.close()

def database_obtener_libro_mayor():
    """
    Genera la agregacion matematica de saldos (Libro Mayor).
    Agrupa por cuenta contable de forma dinamica extrayendo los totales del diario.
    """
    cur = mysql.connection.cursor()
    try:       
        # nota tecnica: Hacemos la matematica pesada agrupando por cuenta contable.
        # nota para @aureo: De aca extraes los saldos netos calculados para pintar tus pantallas sin esfuerzo.
        query = """
            SELECT 
                a.idCuenta as codigo_cuenta, 
                c.nombreCuenta as nombre_cuenta, 
                SUM(a.debe) as total_debe, 
                SUM(a.haber) as total_haber,
                (SUM(a.debe) - SUM(a.haber)) as saldo_actual
            FROM AsientoDiario a
            JOIN cuenta c ON a.idCuenta = c.idCuenta
            GROUP BY a.idCuenta, c.nombreCuenta
            ORDER BY a.idCuenta ASC
        """
        cur.execute(query)
        filas = cur.fetchall()
        
        resultado = []
        for f in filas:
            resultado.append({
                "codigo_cuenta": f[0],
                "nombre_cuenta": f[1],
                "total_debe": float(f[2]),
                "total_haber": float(f[3]),
                "saldo_actual": float(f[4])
            })
        return resultado
    finally:
        cur.close()