import mysql.connector
from fastapi import HTTPException
#@jonas aqui solo la conexion mucha nomas cambiar que probre con la DB que tenia ya solo modifique algunas cosas pero jala XD
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        
        password="J0n@th4n_DB2026!", 
        database="contabilidad2026"
    )
