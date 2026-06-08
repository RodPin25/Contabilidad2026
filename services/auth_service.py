from Database import connection
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

def get_database():
    conn = connection.get_db_connection()
    cursor = conn.cursor()
    return cursor, conn

def login_user(username, password):
    cursor, conn = get_database()
    # 1. Buscamos al usuario (la contraseña la validaremos en memoria)
    cursor.execute("SELECT idUsuario, idRol, pwd FROM USUARIO WHERE nombreUsuario=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    # 2. Validar que el usuario existe Y que el hash de la contraseña coincide
    if user and check_password_hash(user.pwd, password):
        # user.idRol es el tercer campo del SELECT (index 1)
        access_token = create_access_token(
            identity=str(user.idUsuario),
            additional_claims={"role": user.idRol, "username": username}
        )
        return access_token
    return None

def sign_up_user(username, password, idEmpresa, idRol):
    # 1. Encriptar contraseña antes de guardarla
    hashed_password = generate_password_hash(password)
    
    cursor, conn = get_database()
    # 2. Insertar con el hash (estado=1 por defecto)
    try:
        cursor.execute(
            "INSERT INTO USUARIO(nombreUsuario, pwd, estado, idEmpresa, idRol) VALUES(?,?,?,?,?)",
            (username, hashed_password, 1, idEmpresa, idRol)
        )
        conn.commit() # ¡IMPORTANTE! Si no haces commit, no se guarda nada
        return True
    except Exception as e:
        print(f"Error al registrar: {e}")
        return False
    finally:
        conn.close()