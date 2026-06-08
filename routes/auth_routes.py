from flask import Blueprint, request, render_template
from Controllers.auth_controller import login_controller, signup_controller

# Definimos el blueprint
auth_bp = Blueprint('auth', __name__)

# Registramos las rutas
# routes/auth_routes.py

@auth_bp.route('/login', methods=['GET', 'POST']) # <--- AQUÍ está el secreto
def login():
    if request.method == 'POST':
        return login_controller()
    return render_template('login.html')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    return signup_controller()