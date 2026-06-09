from flask import jsonify, request
from Services.estado_resultado_service import generar_estado_resultados

class EstadoResultadosController:
    @staticmethod
    def listar_estado_resultados():
        # Obtenemos los filtros de fecha
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        try:
            # Llamamos al servicio que preparamos
            datos = generar_estado_resultados(fecha_inicio, fecha_fin)
            
            # Retornamos el JSON estructurado
            return jsonify({
                "status": "Éxito",
                "data": datos
            }), 200
            
        except Exception as e:
            print(f"Error en EstadoResultadosController: {e}")
            return jsonify({
                "status": "Error",
                "mensaje": "Error al generar el Estado de Resultados."
            }), 500