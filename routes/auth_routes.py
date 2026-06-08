from flask import Blueprint
from Controllers.auth_controller import login_controller, signup_controller

# Definimos el blueprint
auth_bp = Blueprint('auth', __name__)

# Registramos las rutas
@auth_bp.route('/login', methods=['POST'])
def login():
    return login_controller()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    return signup_controller()