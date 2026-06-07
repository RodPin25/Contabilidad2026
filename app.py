from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS                         # <-- 1. Importas la librería
from config import Config                       
from database.connection import init_db
from routes.diario import router as diario_bp  

app = Flask(__name__)
CORS(app)                                      
app.config.from_object(Config)                  
init_db(app)

app.register_blueprint(diario_bp)  

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido al Backend Unificado - Flask Server en ejecucion"}), 200

if __name__ == '__main__':   
    app.run(debug=True)