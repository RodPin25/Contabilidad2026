from app import app
from Database.connection import get_db_connection
import pyodbc

with app.app_context():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        print("Conectado exitosamente.")
        
        for table in ["CUENTA", "PARTIDA_CONTIENE_CUENTA", "PARTIDAS"]:
            try:
                cur.execute(f"SELECT TOP 1 * FROM {table}")
                print(f"Table '{table}' columns:", [col[0] for col in cur.description])
            except Exception as e:
                print(f"Error checking {table}: {e}")

        conn.close()
    except Exception as e:
        print(f"Error general: {e}")
