from Services.mayor_service import MayorService

def generar_estado_resultados(fecha_inicio, fecha_fin):
    # 1. Obtener movimientos del periodo (Reutilizando tu lógica de mayor)
    movimientos = MayorService.generar_libro_mayor(None, fecha_inicio, fecha_fin)
    
    # 2. Categorizar cuentas
    resultado = {
        "ventas": 0.0,
        "costo_ventas": 0.0,
        "gastos_administrativos": [],
        "gastos_ventas": [],
        "total_gastos": 0.0
    }
    
    for mov in movimientos:
        nombre = mov['nombre_cuenta'].lower()
        debe = float(mov['total_debe'])
        haber = float(mov['total_haber'])
        
        # Clasificación (Ajusta los nombres según tus cuentas reales)
        if "venta" in nombre:
            resultado["ventas"] += haber
        elif "costo" in nombre:
            resultado["costo_ventas"] += debe
        elif "gasto" in nombre or "alquiler" in nombre or "sueldo" in nombre:
            gasto = {"nombre": mov['nombre_cuenta'], "monto": debe}
            resultado["gastos_administrativos"].append(gasto)
            resultado["total_gastos"] += debe
            
    # 3. Cálculos finales
    resultado["utilidad_bruta"] = resultado["ventas"] - resultado["costo_ventas"]
    resultado["resultado_ejercicio"] = resultado["utilidad_bruta"] - resultado["total_gastos"]
    
    return resultado