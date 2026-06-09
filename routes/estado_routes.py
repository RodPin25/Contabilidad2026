from flask import Blueprint
from Controllers.estado_controller import BalanceSituacionController

router = Blueprint('estado_general', __name__)

# Si ya tienes un router definido, solo agrega esta parte:
@router.route("/balance-situacion", methods=["GET"])
def obtener_balance_general():
    return BalanceSituacionController.listar_balance_situacion()