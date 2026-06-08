import os


class Config:
    MYSQL_HOST = os.getenv("DB_HOST", "127.0.0.1")
    MYSQL_USER = os.getenv("DB_USER", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
    MYSQL_DB = os.getenv("DB_NAME", "Contabilidad2026")
    MYSQL_PORT = int(os.getenv("DB_PORT", "1433"))
