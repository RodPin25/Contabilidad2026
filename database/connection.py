from flask_mysqldb import MySQL

# @jonas: Volvemos al esquema limpio. El objeto global consume la clase Config de la raiz.
mysql = MySQL()

def init_db(app):
    mysql.init_app(app)