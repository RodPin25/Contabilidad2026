from flask import Blueprint

from controllers.mayor_controller import MayorController


router = Blueprint("mayor_blueprint", __name__, url_prefix="/libro-mayor")


@router.route("", methods=["GET"])
def listar_mayor():
    return MayorController.listar_mayor()


@router.route("/cuentas", methods=["GET"])
def listar_cuentas():
    return MayorController.listar_cuentas()


@router.route("/cuentas/<int:id_cuenta>", methods=["GET"])
def obtener_cuenta(id_cuenta):
    return MayorController.obtener_cuenta()
