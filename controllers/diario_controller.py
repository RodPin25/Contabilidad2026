from flask import jsonify, request
from services.diario_service import DiarioService

# CAPA CONTROLLERS - MODULO LIBRO DIARIO Y MAYOR
# @jonas: Esta capa administra las peticiones de Flask. Captura la data entrante,
# dispara las operaciones matematicas en la capa de servicios y responde en JSON estandar.

class DiarioController:
    
    @staticmethod
    def crear_partida():        
        # @jonas: Capturamos el JSON crudo enviado por el cliente o los modulos de los panas.
        partida_data = request.get_json()
        respuesta = DiarioService.registrar_nueva_partida(partida_data)
        
        if respuesta["exito"]:
            return jsonify({"status": "Éxito", "message": respuesta["mensaje"]}), 201
        return jsonify({"status": "Error Contable", "message": respuesta["mensaje"]}), 400

    @staticmethod
    def listar_diario():       
        return jsonify({
            "status": "Éxito", 
            "libro_diario": DiarioService.procesar_libro_diario()
        }), 200

    @staticmethod
    def generar_mayor():      
        return jsonify({
            "status": "Éxito", 
            "libro_mayor": DiarioService.procesar_libro_mayor()
        }), 200

    @staticmethod
    def ejecutar_precarga_transacciones():
        # @jonas: Controlador para disparar las 25 transacciones precargadas obligatorias.
        res = DiarioService.generar_25_transacciones_automaticas()
        return jsonify(res), 200

    @staticmethod
    def ejecutar_corte_operaciones():
        # @jonas: Dispara de golpe la regularizacion del IVA y los cierres a capital.
        DiarioService.regularizar_iva_automatico()
        res_cierre = DiarioService.ejecutar_cierre_contable_mensual()
        return jsonify({"status": "Éxito", "message": "Corte de IVA y partidas de cierre completadas."}), 200