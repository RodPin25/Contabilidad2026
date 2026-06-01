from configuracion.DataBase import get_db_connection
from fastapi import HTTPException
import mysql.connector

# CAPA DATABASE - MODULO LIBRO DIARIO Y MAYOR pal muchacho aureo
# @jonas: aqui en esta capa es la única que toca el MySQL/SSMS de forma directa.
# Si la base de datos ('contabilidad2026') cambia de nombre 
# o si se modifican las credenciales globales, el único archivo que se toca es 
# 'configuracion/DataBase.py'. Estos métodos heredan la conexión de allí.


def database_guardar_partida(numero_partida, fecha, descripcion, tipo_partida, detalles):
    """
    Inserta una transacción completa utilizando una operación transaccional (commit/rollback).
    Maneja una relación Maestro-Detalle entre encabezado y líneas de la partida.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # NOTA TECNICA: Primero registramos el encabezado para obtener el ID autonumérico.
        # Este ID es la llave primaria que amarra a todos los movimientos del detalle abajo.
        query_encabezado = """
            INSERT INTO partida_encabezado (numero_partida, fecha, descripcion, tipo_partida)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_encabezado, (numero_partida, fecha, descripcion, tipo_partida))
        id_partida_generado = cursor.lastrowid
        
        # NOTA DE INTEGRACION: 'codigo_cuenta' recibe el idCuenta real que viene de la 
        # tabla 'Cuenta' administrada por Sochito en el inventario.
        query_detalle = """
            INSERT INTO partida_detalle (id_partida, codigo_cuenta, debe, haber)
            VALUES (%s, %s, %s, %s)
        """
        for d in detalles:
            cursor.execute(query_detalle, (id_partida_generado, d.codigo_cuenta, d.debe, d.haber))
            
        # Si todo se ejecutó sin errores en el bucle, confirmamos los datos en la DB
        conn.commit()
        return True
    except mysql.connector.Error as err:
        # @jonas: Si falla una sola línea del detalle (ej. un ID de cuenta que no existe), 
        # deshacemos todo el proceso con rollback para no dejar partidas huérfanas en la DB.
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error en Capa Database: {err.msg}")
    finally:
        cursor.close()
        conn.close()

def database_obtener_libro_diario():
    """
    Extrae el historial completo cronológico de las partidas del Libro Diario.
    Realiza un JOIN con la tabla maestra de Inventarios para jalar los nombres de cuentas.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # @jonas: la logica de aca es algo diferente, en este caso cambió el JOIN hacia la tabla 'Cuenta' 
        # que es la estructura final que definió Sochito. Si se cambia agregamos un 
        # catálogo maestro formal, solo se cambia el último JOIN para mapear el string 'nombreCuenta'.
        query = """
            SELECT e.numero_partida, e.fecha, e.descripcion, e.tipo_partida,
                   d.codigo_cuenta, c.nombreCuenta as nombre_cuenta, d.debe, d.haber
            FROM partida_encabezado e
            JOIN partida_detalle d ON e.id_partida = d.id_partida
            JOIN Cuenta c ON d.codigo_cuenta = c.idCuenta
            ORDER BY e.numero_partida ASC, d.id_detalle ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def database_obtener_libro_mayor():
    """
    Genera la agregación matemática de saldos (Libro Mayor).
    Agrupa por cuenta contable y calcula el saldo neto de forma dinámica.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:       
        # nota tecnica: Esta consulta hace la matemática pesada agrupando por cuenta.
        # nota para: @aureo: De este endpoint podés jalar el JSON limpio para pintar las 'T' contables 
        # en tu frontend sin tener que recalcular nada en tu backend. Ya te devuelve los totales del diario uwu.
        query = """
            SELECT 
                d.codigo_cuenta, 
                c.nombreCuenta as nombre_cuenta, 
                SUM(d.debe) as total_debe, 
                SUM(d.haber) as total_haber,
                (SUM(d.debe) - SUM(d.haber)) as saldo_actual
            FROM partida_detalle d
            JOIN Cuenta c ON d.codigo_cuenta = c.idCuenta
            GROUP BY d.codigo_cuenta, c.nombreCuenta
            ORDER BY d.codigo_cuenta ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()