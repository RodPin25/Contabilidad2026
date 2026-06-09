from app import app
from Database.connection import get_db_connection

with app.app_context():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'PARTIDA_CONTIENE_CUENTA'")
    print("Columnas de PARTIDA_CONTIENE_CUENTA:")
    for row in cur.fetchall():
        print(f"- {row[0]} ({row[1]})")
    
    cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'PARTIDAS'")
    print("\nColumnas de PARTIDAS:")
    for row in cur.fetchall():
        print(f"- {row[0]} ({row[1]})")
    conn.close()
