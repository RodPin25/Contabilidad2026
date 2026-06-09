from app import app
from Database.connection import get_db_connection

with app.app_context():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    print("Tablas encontradas:")
    for row in cur.fetchall():
        print(f"- {row[0]}")
    conn.close()
