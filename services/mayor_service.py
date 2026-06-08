from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

from database import mayor_db


TIPOS_DEUDORES = {1, 2}
TIPOS_ACREEDORES = {3, 4, 5}


class MayorService:
    @staticmethod
    def generar_libro_mayor(id_cuenta=None, fecha_inicio=None, fecha_fin=None):
        MayorService._validar_filtros(id_cuenta, fecha_inicio, fecha_fin)
        filas = mayor_db.obtener_cuentas_con_movimientos(
            id_cuenta=id_cuenta,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        cuentas = OrderedDict()
        for fila in filas:
            cuenta_id = fila[0]
            tipo_id = fila[2]
            cuenta = cuentas.setdefault(
                cuenta_id,
                {
                    "id_cuenta": cuenta_id,
                    "nombre_cuenta": fila[1],
                    "id_tipo_cuenta": tipo_id,
                    "tipo_cuenta": fila[3],
                    "naturaleza": MayorService._obtener_naturaleza(tipo_id),
                    "movimientos": [],
                    "_total_debe": Decimal("0"),
                    "_total_haber": Decimal("0"),
                    "_saldo": Decimal("0"),
                },
            )

            debe = Decimal(str(fila[9] or 0))
            haber = Decimal(str(fila[10] or 0))
            cuenta["_total_debe"] += debe
            cuenta["_total_haber"] += haber
            cuenta["_saldo"] += MayorService._variacion_saldo(tipo_id, debe, haber)

            cuenta["movimientos"].append(
                {
                    "id_partida": fila[4],
                    "numero_partida": fila[5],
                    "fecha": str(fila[6]),
                    "descripcion": fila[7],
                    "debe": float(debe),
                    "haber": float(haber),
                    "saldo": float(cuenta["_saldo"]),
                }
            )

        resultado = []
        for cuenta in cuentas.values():
            resultado.append(
                {
                    "id_cuenta": cuenta["id_cuenta"],
                    "nombre_cuenta": cuenta["nombre_cuenta"],
                    "id_tipo_cuenta": cuenta["id_tipo_cuenta"],
                    "tipo_cuenta": cuenta["tipo_cuenta"],
                    "naturaleza": cuenta["naturaleza"],
                    "total_debe": float(cuenta["_total_debe"]),
                    "total_haber": float(cuenta["_total_haber"]),
                    "saldo_final": float(cuenta["_saldo"]),
                    "movimientos": cuenta["movimientos"],
                }
            )
        return resultado

    @staticmethod
    def listar_cuentas_disponibles():
        return [
            {
                "id_cuenta": fila[0],
                "nombre_cuenta": fila[1],
                "id_tipo_cuenta": fila[2],
                "tipo_cuenta": fila[3],
                "naturaleza": MayorService._obtener_naturaleza(fila[2]),
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
