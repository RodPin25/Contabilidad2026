from Services.saldos_service import generar_balance_saldos

def generar_balance_situacion(fecha_corte):
    # 1. Obtenemos el balance de saldos completo
    datos_saldos = generar_balance_saldos(None, fecha_corte)
    
    # 2. Categorizamos usando la seccion (tipo de cuenta)
    estructura = {
        "activo": {"cuentas": [], "total": 0.0},
        "pasivo": {"cuentas": [], "total": 0.0},
        "capital": {"cuentas": [], "total": 0.0}
    }
    
    for item in datos_saldos:
        seccion = item.get('seccion', '').lower()
        saldo = item['saldo_final']
        
        # Clasificación robusta por sección
        if "activo" in seccion:
            estructura["activo"]["cuentas"].append(item)
            estructura["activo"]["total"] += saldo
        elif "pasivo" in seccion:
            estructura["pasivo"]["cuentas"].append(item)
            estructura["pasivo"]["total"] += saldo
        else:
            # Por defecto, capital
            estructura["capital"]["cuentas"].append(item)
            estructura["capital"]["total"] += saldo
            
    # 3. Suma final
    estructura["suma_pasivo_capital"] = estructura["pasivo"]["total"] + estructura["capital"]["total"]
    
    return estructura
