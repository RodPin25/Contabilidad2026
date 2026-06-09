from Services.inventario_service import obtener_inventario
from Services.mayor_service import MayorService

def generar_balance_saldos(fecha_inicio, fecha_fin):
    """
    Genera el balance de saldos unificando los saldos iniciales del inventario
    con los movimientos del libro mayor en un rango de fechas.
    """
    # 1. Obtener saldos iniciales desde el inventario
    # obtener_inventario() devuelve (datos_agrupados, tipos)
    inventario_datos, _ = obtener_inventario()
    
    balance_map = {}

    # Aplanamos el inventario para inicializar el balance_map
    for seccion in inventario_datos.values():
        for cuenta in seccion:
            c_id = cuenta.get('id')
            if c_id is not None:
                balance_map[c_id] = {
                    "nombre": cuenta.get('nombre', 'Sin nombre'),
                    "inicial": float(cuenta.get('monto', 0) or 0),
                    "debe": 0,
                    "haber": 0
                }

    # 2. Obtener movimientos del Libro Mayor
    # MayorService.generar_libro_mayor devuelve una lista de diccionarios con 'codigo_cuenta'
    datos_mayor = MayorService.generar_libro_mayor(None, fecha_inicio, fecha_fin) or []
    
    for cuenta_mayor in datos_mayor:
        c_id = cuenta_mayor.get('codigo_cuenta')
        if c_id is None:
            continue
        
        if c_id not in balance_map:
            balance_map[c_id] = {
                "nombre": cuenta_mayor.get('nombre_cuenta', 'Cuenta sin nombre'),
                "inicial": 0,
                "debe": 0,
                "haber": 0
            }
        
        balance_map[c_id]["debe"] += float(cuenta_mayor.get('total_debe', 0) or 0)
        balance_map[c_id]["haber"] += float(cuenta_mayor.get('total_haber', 0) or 0)

    # 3. Cálculo final del balance
    balance_final = []
    for c_id, data in balance_map.items():
        # Lógica: Inicial + Debe - Haber
        # Nota: En contabilidad real el saldo final depende de la naturaleza,
        # pero aquí mantenemos la fórmula solicitada por simplicidad.
        saldo_final = data['inicial'] + data['debe'] - data['haber']
        
        balance_final.append({
            "id":          c_id,
            "nombre":      data['nombre'],
            "inicial":     data['inicial'],
            "debe":        data['debe'],
            "haber":       data['haber'],
            "saldo_final": saldo_final
        })
        
    return balance_final
