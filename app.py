from flask import Flask, redirect, url_for, jsonify
from config import Config                     
from database.connection import init_db
from routes.diario import router as diario_bp  

app = Flask(__name__)
app.config.from_object(Config)                
init_db(app)

# Registro de tu Blueprint contable en la arquitectura global
app.register_blueprint(diario_bp)  

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido al Backend Unificado - Flask Server en ejecucion"}), 200

if __name__ == '__main__':   
    app.run(debug=True)