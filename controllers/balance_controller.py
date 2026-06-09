from flask import jsonify, request
from Services.saldos_service import generar_balance_saldos

class BalanceController:
    @staticmethod
    def listar_balance_saldos():
        # 1. Obtenemos los filtros desde la URL (ej: /balance?fecha_inicio=2026-06-01&fecha_fin=2026-06-30)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        try:
            # 2. Llamamos al servicio que hace todo el trabajo pesado
            datos_balance = generar_balance_saldos(fecha_inicio, fecha_fin)
            
            # 3. Retornamos la respuesta exitosa
            return jsonify({
                "status": "Exito",
                "balance": datos_balance
            }), 200
            
        except Exception as e:
            # 4. Manejo de errores por si algo falla en el cálculo
            print(f"Error en BalanceController: {e}")
            return jsonify({
                "status": "Error",
                "mensaje": "Ocurrió un error al generar el balance de saldos."
            }), 500