from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

from Database import mayor_db


TIPOS_DEUDORES = {5, 6}
TIPOS_ACREEDORES = {7, 8, 9}


class MayorService:

    # Asegúrate de usar esta estructura en tu MayorService.py
    @staticmethod
    def generar_libro_mayor(id_cuenta=None, fecha_inicio=None, fecha_fin=None):
        filas = mayor_db.obtener_cuentas_con_movimientos(id_cuenta, fecha_inicio, fecha_fin)
        print(filas)

        cuentas_agrupadas = {}

        for fila in filas:
            c_id = fila['idCuenta']
            if c_id not in cuentas_agrupadas:
                cuentas_agrupadas[c_id] = {
                    "codigo_cuenta": c_id,
                    "nombre_cuenta": fila['nombreCuenta'],
                    "total_debe": 0,
                    "total_haber": 0,
                    "saldo_actual": 0,
                    "movimientos": []  # <--- AQUÍ ESTÁ EL DETALLE
                }

            # Agregamos el movimiento con la descripción
            movimiento = {
                "fecha": str(fila['fechaPartida']),
                "numero_partida": fila['noPartida'],
                "descripcion": fila['descripcionPartida'], # <--- ESTO ES LO QUE TE FALTA
                "debe": float(fila['debe'] or 0),
                "haber": float(fila['haber'] or 0),
                "saldo": 0 # Puedes calcular el saldo acumulado aquí
            }

            cuentas_agrupadas[c_id]["movimientos"].append(movimiento)
            cuentas_agrupadas[c_id]["total_debe"] += movimiento["debe"]
            cuentas_agrupadas[c_id]["total_haber"] += movimiento["haber"]
            cuentas_agrupadas[c_id]["saldo_actual"] = cuentas_agrupadas[c_id]["total_debe"] - cuentas_agrupadas[c_id]["total_haber"]

        return list(cuentas_agrupadas.values())

    @staticmethod
    def listar_cuentas_disponibles():
        return [
            {
                "id_cuenta": fila['idCuenta'],
                "nombre_cuenta": fila['nombreCuenta'],
                "id_tipo_cuenta": fila['idTipoCuenta'],
                "tipo_cuenta": fila['nombreTipo'],
                "naturaleza": MayorService._obtener_naturaleza(fila['idTipoCuenta']),
            }
            for fila in mayor_db.obtener_cuentas_disponibles()
        ]

    @staticmethod
    def _obtener_naturaleza(tipo_id):
        if tipo_id in TIPOS_DEUDORES:
            return "Deudora"
        if tipo_id in TIPOS_ACREEDORES:
            return "Acreedora"
        raise ValueError(f"El tipo de cuenta {tipo_id} no posee naturaleza configurada.")

    @staticmethod
    def _variacion_saldo(tipo_id, debe, haber):
        if tipo_id in TIPOS_DEUDORES:
            return debe - haber
        if tipo_id in TIPOS_ACREEDORES:
            return haber - debe
        raise ValueError(f"El tipo de cuenta {tipo_id} no posee naturaleza configurada.")

    @staticmethod
    def _validar_filtros(id_cuenta, fecha_inicio, fecha_fin):
        if id_cuenta is not None and id_cuenta <= 0:
            raise ValueError("id_cuenta debe ser un entero positivo.")

        inicio = MayorService._convertir_fecha(fecha_inicio, "fecha_inicio")
        fin = MayorService._convertir_fecha(fecha_fin, "fecha_fin")
        if inicio and fin and inicio > fin:
            raise ValueError("fecha_inicio no puede ser posterior a fecha_fin.")

    @staticmethod
    def _convertir_fecha(valor, nombre):
        if valor is None:
            return None
        try:
            return datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError(f"{nombre} debe tener formato YYYY-MM-DD.") from error
