from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database.connection import init_db
from routes.mayor import router as mayor_bp


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
init_db(app)

app.register_blueprint(mayor_bp)


@app.route("/")
def index():
    return jsonify(
        {"message": "Backend del Libro Mayor - Flask Server en ejecucion"}
    ), 200


if __name__ == "__main__":
    app.run(debug=True)
