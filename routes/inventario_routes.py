from flask import Blueprint
from controllers.inventario_controller import (
    ctrl_ver_inventario,
    ctrl_agregar_cuenta,
    ctrl_eliminar_cuenta,
    ctrl_generar_partida_apertura
)

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET'])
def ver_inventario():
    return ctrl_ver_inventario()

@inventario_bp.route('/inventario/agregar', methods=['POST'])
def agregar_cuenta():
    return ctrl_agregar_cuenta()

@inventario_bp.route('/inventario/eliminar', methods=['POST'])
def eliminar_cuenta():
    return ctrl_eliminar_cuenta()

@inventario_bp.route('/inventario/partida-apertura', methods=['POST'])
def generar_partida_apertura():
    return ctrl_generar_partida_apertura()