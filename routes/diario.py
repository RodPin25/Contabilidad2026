from flask import Blueprint, jsonify
from Controllers.diario_controller import DiarioController

# CAPA ROUTES 
# @jonas: Creamos el Blueprint oficial. Su unica tarea es mapear los endpoints HTTP 
# y trasladar la ejecucion al controlador respectivo.

router = Blueprint('diario_blueprint', __name__)

@router.route("/partidas", methods=["POST"])
def registrar_partida():
    return DiarioController.crear_partida()

@router.route("/libro-diario", methods=["GET"])
def obtener_libro_diario():
    return DiarioController.listar_diario()

@router.route("/libro-mayor", methods=["GET"])
def obtener_libro_mayor():
    return DiarioController.generar_mayor()

@router.route("/inicializar-transacciones", methods=["POST"])
def precargar_datos():
    # Endpoint clave para llenar la base de datos con las 25 transacciones de la rúbrica.
    return DiarioController.ejecutar_precarga_transacciones()

@router.route("/ejecutar-cierre", methods=["POST"])
def ejecutar_cierre_mensual():
    # Endpoint para automatizar la regularización de IVA y partidas de cierre.
    return DiarioController.ejecutar_corte_operaciones()

@router.route("/cuentas-disponibles", methods=["GET"])
def obtener_cuentas_disponibles():
    # @jonas: Jala las cuentas vivas del catalogo de Sochito para los formularios
    from Database.connection import get_db_connection
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT idCuenta, nombreCuenta FROM CUENTA")
    cuentas = cur.fetchall()
    cur.close()
    conn.close()

    resultado = [{"idCuenta": c[0], "nombreCuenta": c[1]} for c in cuentas]
    return jsonify(resultado), 200