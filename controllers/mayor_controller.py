from flask import jsonify, request

from Services.mayor_service import MayorService


class MayorController:
    @staticmethod
    def listar_mayor():
        try:
            id_cuenta = MayorController._obtener_id_cuenta_opcional()
            fecha_inicio = request.args.get("fecha_inicio")
            fecha_fin = request.args.get("fecha_fin")
            libro_mayor = MayorService.generar_libro_mayor(
                id_cuenta=id_cuenta,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
            )
            return jsonify({"status": "Exito", "libro_mayor": libro_mayor}), 200
        except ValueError as error:
            return jsonify({"status": "Error", "message": str(error)}), 400
        except Exception as error:
            return jsonify({"status": "Error", "message": str(error)}), 500

    @staticmethod
    def obtener_cuenta():
        try:
            id_cuenta = request.view_args["id_cuenta"]
            cuentas = MayorService.generar_libro_mayor(id_cuenta=id_cuenta)
            if not cuentas:
                return jsonify(
                    {"status": "Error", "message": "La cuenta no posee movimientos."}
                ), 404
            return jsonify({"status": "Exito", "cuenta": cuentas[0]}), 200
        except ValueError as error:
            return jsonify({"status": "Error", "message": str(error)}), 400
        except Exception as error:
            return jsonify({"status": "Error", "message": str(error)}), 500

    @staticmethod
    def listar_cuentas():
        try:
            return jsonify(
                {
                    "status": "Exito",
                    "cuentas": MayorService.listar_cuentas_disponibles(),
                }
            ), 200
        except Exception as error:
            return jsonify({"status": "Error", "message": str(error)}), 500

    @staticmethod
    def _obtener_id_cuenta_opcional():
        valor = request.args.get("id_cuenta")
        if valor is None:
            return None
        try:
            return int(valor)
        except ValueError as error:
            raise ValueError("id_cuenta debe ser un entero positivo.") from error
