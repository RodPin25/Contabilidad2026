# config.py
import os

class Config:
    DB_SERVER = os.getenv("DB_SERVER", "tu_ip_servidor")
    DB_DATABASE = os.getenv("DB_DATABASE", "Contabilidad2026")
    DB_USER = os.getenv("DB_USER", "SA")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "TuPasswordFuerte")