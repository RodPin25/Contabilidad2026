from flask import Blueprint
from Controllers.estado_resultado_controller import EstadoResultadosController

# Asumiendo que tu router se llama así
router = Blueprint('saldos_routes', __name__)

# --- Esta es la ruta que necesitas agregar ---
@router.route("/estado-resultados", methods=["GET"])
def obtener_estado_resultados():
    return EstadoResultadosController.listar_estado_resultados()