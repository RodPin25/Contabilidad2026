from flask import jsonify, request
from Services.estado_service import generar_balance_situacion

class BalanceSituacionController:
    @staticmethod
    def listar_balance_situacion():
        # Obtenemos la fecha de corte del reporte
        fecha_corte = request.args.get('fecha_corte')
        
        # Validamos que la fecha venga en la petición
        if not fecha_corte:
            return jsonify({
                "status": "Error", 
                "mensaje": "Es necesario proporcionar una fecha_corte"
            }), 400
        
        try:
            # Llamamos al servicio que agrupa Activos, Pasivos y Capital
            datos = generar_balance_situacion(fecha_corte)
            
            # Retornamos el JSON con el Balance General
            return jsonify({
                "status": "Éxito",
                "fecha_corte": fecha_corte,
                "data": datos
            }), 200
            
        except Exception as e:
            # Capturamos cualquier error técnico para que no se detenga el servidor
            print(f"Error en BalanceSituacionController: {e}")
            return jsonify({
                "status": "Error",
                "mensaje": "Ocurrió un problema al generar el Balance de Situación."
            }), 500