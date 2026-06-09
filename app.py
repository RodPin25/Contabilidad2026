import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

# Importaciones de configuración y rutas
from config import Config
from routes.inventario_routes import inventario_bp
from routes.auth_routes import auth_bp
from routes.view_routes import views_bp
from routes.diario import router as diario_bp
from routes.mayor import router as mayor_bp

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

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
        "tags": [{"name": "Inventario"}, {"name": "Auth"}],
        "paths": {} # Aquí irían tus definiciones de rutas para Swagger
    })

# 4. Registro de todos los Blueprints
# Cada archivo en la carpeta 'routes' maneja su propia lógica
app.register_blueprint(inventario_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
app.register_blueprint(diario_bp)
app.register_blueprint(mayor_bp)

if __name__ == '__main__':
    # debug=True es ideal para desarrollo; recuerda cambiarlo en producción
    app.run(debug=True)