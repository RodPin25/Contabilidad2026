from flask import Flask, redirect, url_for, jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Asegúrate de importar tus funciones/clases desde tus otros archivos
from config import Config
from Database import connection
from routes.inventario_routes import inventario_bp

# Variables de entorno
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# 1. Configuración
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')

# 2. Inicialización de Extensiones
jwt = JWTManager(app)

# 3. Swagger UI Config
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'
swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger_json():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "API Contabilidad - Distribuidora Don Bosco",
            "description": "Sistema contable",
            "version": "1.0.0"
        },
        "host": "127.0.0.1:5000",
        "basePath": "/",
        "tags": [{"name": "Inventario"}],
        "paths": {
            # Aquí van tus endpoints definidos en el JSON
        }
    })

# 4. Registro de Blueprints (Rutas)
app.register_blueprint(inventario_bp)


# ============= Llamadas a las rutas para renderizar frontend ==================

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/diario')
def ver_diario():
    return render_template('diario.html')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/mayor')
def mayor():
    return render_template('mayor.html')

if __name__ == '__main__':
    app.run(debug=True)