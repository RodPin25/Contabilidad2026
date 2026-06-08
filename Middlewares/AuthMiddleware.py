# middlewares/auth.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 1. El portero verifica el token
        verify_jwt_in_request()
        
        # 2. Opcional: El portero revisa si el usuario tiene rol de admin
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"msg": "No tienes permisos de administrador"}, 403
            
        # 3. Si todo está bien, dejamos que la petición continúe su camino
        return fn(*args, **kwargs)
    return wrapper