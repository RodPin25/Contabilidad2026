from flask import Flask, redirect, url_for, jsonify
from config import Config
from database.connection import init_db
from routes.inventario_routes import inventario_bp
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

# ─── Swagger UI ──────────────────────────────────────────────────
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
            "description": "Sistema contable Distribuidora Don Bosco",
            "version": "1.0.0"
        },
        "host": "127.0.0.1:5000",
        "basePath": "/",
        "tags": [{"name": "Inventario"}],
        "paths": {
            "/inventario": {
                "get": {
                    "tags": ["Inventario"],
                    "summary": "Ver inventario completo",
                    "responses": {"200": {"description": "Página HTML con inventario"}}
                }
            },
            "/inventario/agregar": {
                "post": {
                    "tags": ["Inventario"],
                    "summary": "Agregar cuenta contable",
                    "parameters": [
                        {"name": "nombre", "in": "formData", "type": "string", "required": True},
                        {"name": "descripcion", "in": "formData", "type": "string", "required": True},
                        {"name": "monto", "in": "formData", "type": "number", "required": True},
                        {"name": "idTipoCuenta", "in": "formData", "type": "integer", "required": True}
                    ],
                    "responses": {"302": {"description": "Redirige al inventario"}}
                }
            },
            "/inventario/eliminar": {
                "post": {
                    "tags": ["Inventario"],
                    "summary": "Eliminar cuenta contable",
                    "parameters": [
                        {"name": "idCuenta", "in": "formData", "type": "integer", "required": True}
                    ],
                    "responses": {"302": {"description": "Redirige al inventario"}}
                }
            }
        }
    })

# ─── Rutas ───────────────────────────────────────────────────────
app.register_blueprint(inventario_bp)

@app.route('/')
def index():
    return redirect(url_for('inventario.ver_inventario'))

if __name__ == '__main__':
    app.run(debug=True)