# Database/connection.py
import pyodbc
from flask import current_app

def get_db_connection():
    config = current_app.config
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['DB_SERVER']};"
        f"DATABASE={config['DB_DATABASE']};"
        f"UID={config['DB_USER']};"
        f"PWD={config['DB_PASSWORD']}"
    )
    return pyodbc.connect(conn_str)