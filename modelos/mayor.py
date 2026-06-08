"""
Estructura de respuesta de una cuenta del Libro Mayor:

{
    "id_cuenta": int,
    "nombre_cuenta": str,
    "id_tipo_cuenta": int,
    "tipo_cuenta": str,
    "naturaleza": "Deudora" | "Acreedora",
    "total_debe": float,
    "total_haber": float,
    "saldo_final": float,
    "movimientos": [
        {
            "id_partida": int,
            "numero_partida": int,
            "fecha": "YYYY-MM-DD",
            "descripcion": str,
            "debe": float,
            "haber": float,
            "saldo": float
        }
    ]
}
"""
