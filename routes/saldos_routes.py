from flask import Blueprint, jsonify
from Controllers.balance_controller import BalanceController

router = Blueprint('saldos_blueprint', __name__)

@router.route("/balance-saldos", methods=["GET"])
def obtener_balance():
    return BalanceController.listar_balance_saldos()