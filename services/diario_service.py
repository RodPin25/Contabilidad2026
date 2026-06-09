import Database.diario_db as diario_db
from datetime import date

# CAPA SERVICES (DLL Contable de la Empresa)
# @jonas: aca eliminamos las simulaciones fijas y conectamos la matematica contable 
# con consultas vivas a la BD para cumplir con el ciclo automatico del PDF.

class DiarioService:
    
    @staticmethod
    def registrar_nueva_partida(partida_data):
        detalles = partida_data.get('detalles', []) if isinstance(partida_data, dict) else partida_data.detalles
        
        suma_debe = sum(float(d['debe'] if isinstance(d, dict) else d.debe) for d in detalles)
        suma_haber = sum(float(d['haber'] if isinstance(d, dict) else d.haber) for d in detalles)
        
        if round(suma_debe, 2) != round(suma_haber, 2):
            return {"exito": False, "mensaje": f"Error Contable: La partida no cuadra. Debe: Q{suma_debe:.2f}, Haber: Q{suma_haber:.2f}"}
            
        no_partida = partida_data.get('numero_partida') if isinstance(partida_data, dict) else partida_data.numero_partida
        fecha = partida_data.get('fecha') if isinstance(partida_data, dict) else partida_data.fecha
        descripcion = partida_data.get('descripcion') if isinstance(partida_data, dict) else partida_data.descripcion
        tipo_partida = partida_data.get('tipo_partida', 'Normal') if isinstance(partida_data, dict) else partida_data.tipo_partida
        
        res = diario_db.database_guardar_partida(no_partida, fecha, descripcion, tipo_partida, detalles)
        return {"exito": res, "mensaje": "Partida registrada con exito."}

    @staticmethod
    def procesar_libro_diario():
        return diario_db.database_obtener_libro_diario()

    @staticmethod
    def procesar_libro_mayor():
        return diario_db.database_obtener_libro_mayor()

    @staticmethod
    def generar_25_transacciones_automaticas():
        """
        NOTA TECNICA: Inserta las 25 transacciones base precargadas exigidas por la rubrica.
        Mapea el 12% del IVA de forma automatica aplicando logica relacional con IDs de cuenta reales.
        """
        # @jonas: Asumimos IDs de cuentas basados en nuestro script: 2=Caja, 6=Ventas, 7=IVA Débito, 8=IVA Crédito, 10=Gastos
        transacciones_demo = []
        
        # 1. Generamos compras y ventas ciclicamente para alcanzar las 25 requeridas
        for i in range(1, 14):
            monto_base = 1000.00 * i
            iva_calculado = monto_base * 0.12 # 12% SAT guatemalteco
            total_factura = monto_base + iva_calculado
            
            # Transacciones del tipo: VENTAS AL CONTADO (13 transacciones)
            transacciones_demo.append({
                "numero_partida": i + 1, # La partida 1 es la de apertura de Soch
                "fecha": str(date.today()),
                "descripcion": f"Venta de productos electronicos al contado - Doc No. {100 + i}",
                "tipo_partida": "Normal",
                "detalles": [
                    {"idCuenta": 2, "debe": total_factura, "haber": 0.00},  # Caja
                    {"idCuenta": 6, "debe": 0.00, "haber": monto_base},    # Ventas (Neto)
                    {"idCuenta": 7, "debe": 0.00, "haber": iva_calculado}  # IVA Débito Fiscal
                ]
            })

        for i in range(1, 13):
            monto_base = 500.00 * i
            iva_calculado = monto_base * 0.12
            total_factura = monto_base + iva_calculado
            
            # Transacciones del tipo: COMPRAS / GASTOS DEL MES (12 transacciones)
            transacciones_demo.append({
                "numero_partida": i + 14,
                "fecha": str(date.today()),
                "descripcion": f"Compra de suministros operativos de oficina - Fac No. {500 + i}",
                "tipo_partida": "Normal",
                "detalles": [
                    {"idCuenta": 10, "debe": monto_base, "haber": 0.00},   # Gastos Generales
                    {"idCuenta": 8, "debe": iva_calculado, "haber": 0.00},  # IVA Crédito Fiscal
                    {"idCuenta": 2, "debe": 0.00, "haber": total_factura}   # Caja (Sale efectivo)
                ]
            })

        contador = 0
        for t in transacciones_demo:
            DiarioService.registrar_nueva_partida(t)
            contador += 1
        return {"exito": True, "mensaje": f"Se inyectaron {contador} transacciones reales al Libro Diario con calculo de IVA automatico."}

    @staticmethod
    def regularizar_iva_automatico():
        """
        PROCESO DE CORTE REAL: Consulta los saldos acumulados en el Libro Mayor 
        para restar de forma exacta las cuentas de IVA SAT.
        """
        # @jonas: Extraemos los saldos agregados reales desde el Libro Mayor
        saldos_mayor = diario_db.database_obtener_libro_mayor()
        
        credito_fiscal = 0.00
        debito_fiscal = 0.00
        
        for s in saldos_mayor:
            if s['codigo_cuenta'] == 7: # IVA Débito Fiscal
                debito_fiscal = float(s['total_haber'] - s['total_debe'])
            if s['codigo_cuenta'] == 8: # IVA Crédito Fiscal
                credito_fiscal = float(s['total_debe'] - s['total_haber'])
        
        # @jonas: Aplicamos logica fiscal guatemalteca: restamos los saldos reales calculados
        iva_por_pagar = debito_fiscal - credito_fiscal
        
        partida_iva = {
            "numero_partida": 27,
            "fecha": str(date.today()),
            "descripcion": "Regularizacion automatica del IVA determinada por los saldos del periodo",
            "tipo_partida": "Regularizacion",
            "detalles": [
                {"idCuenta": 7, "debe": debito_fiscal, "haber": 0.00},    # Eliminamos el debito
                {"idCuenta": 8, "debe": 0.00, "haber": credito_fiscal},   # Eliminamos el credito
                {"idCuenta": 2, "debe": 0.00, "haber": iva_por_pagar}     # La diferencia real por pagar (Caja/Pasivo)
            ]
        }
        return DiarioService.registrar_nueva_partida(partida_iva)

    @staticmethod
    def ejecutar_cierre_contable_mensual():
        """
        EFECTUA EL CIERRE DINÁMICO: Calcula la utilidad restando ingresos y gastos 
        reales de la base de datos y liquida las cuentas a cero.
        """
        saldos_mayor = diario_db.database_obtener_libro_mayor()
        
        total_ingresos = 0.00
        total_gastos = 0.00
        
        for s in saldos_mayor:
            if s['codigo_cuenta'] == 6: # Cuenta de Ventas (Ingresos)
                total_ingresos = float(s['total_haber'] - s['total_debe'])
            if s['codigo_cuenta'] == 10: # Cuenta de Gastos
                total_gastos = float(s['total_debe'] - s['total_haber'])
                
        # @jonas: Sacamos el Estado de Resultados de forma dinamica en una resta limpia
        utilidad_neta = total_ingresos - total_gastos
        
        partida_cierre = {
            "numero_partida": 28,
            "fecha": str(date.today()),
            "descripcion": "Partida de cierre definitivo mensual de las cuentas de resultados reales",
            "tipo_partida": "Cierre",
            "detalles": [
                {"idCuenta": 6, "debe": total_ingresos, "haber": 0.00},   # Cargamos ingresos para saldar a Q0
                {"idCuenta": 10, "debe": 0.00, "haber": total_gastos},   # Abonamos gastos para saldar a Q0
                {"idCuenta": 5, "debe": 0.00, "haber": utilidad_neta}    # Se traslada el remanente real a Capital Contable
            ]
        }
        return DiarioService.registrar_nueva_partida(partida_cierre)