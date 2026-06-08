# CAPA MODELOS / ESTRUCTURAS - MODULO LIBRO DIARIO
# @jonas: Al cambiar a Flask retiramos Pydantic del core para evitar errores de librerias.
# Dejo documentada la estructura exacta que debe enviar el Frontend de Aureo en el JSON de peticiones:

"""
PAYLOAD ESPERADO PARA REGISTRO DE PARTIDAS:
{
    "numero_partida": int,
    "fecha": "YYYY-MM-DD",
    "descripcion": str,
    "tipo_partida": "Normal" | "Regularizacion" | "Cierre",
    "detalles": [
        {
            "idCuenta": int,
            "debe": float,
            "haber": float
        }
    ]
}
"""