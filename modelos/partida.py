from pydantic import BaseModel
from typing import List
from datetime import date


# CAPA MODELOS / SCHEMAS (VALIDACIÓN DE ENTRADA DE DATOS)
# @jonas: use Pydantic para filtrar y asegurar 
# que cualquier dato que venga del frontend (o de sus módulos tio soch) sea correcto 
# antes de que toque los controladores o los servicios. 
# Si alguien manda un texto en lugar de un número, FastAPI lo rebota automáticamente.

class PartidaDetalleInput(BaseModel):
    
    # @jonas: 'codigo_cuenta' recibe el idCuenta como string  
    # Mapea directo con la llave primaria de la tabla 'Cuenta' de Sochito.
    codigo_cuenta: str
    debe: float
    haber: float


class PartidaInput(BaseModel):
    """
    Define la estructura del JSON global que debe enviar el cliente para registrar 
    cualquier partida en el Libro Diario.
    """
    numero_partida: int
    fecha: date  # Pydantic valida automáticamente el formato ISO estándar (YYYY-MM-DD)
    descripcion: str  # Esta es la glosa descriptiva de la partida  
    # NOTA TECNICA: 'tipo_partida' acepta únicamente los estados que hemos visto o los que hemos trabajado si se agrega o falto algo mas aca no se toca nomas recibe.
    # tanto para el cierre y la partida en teoria aca enviamos lo que le corresponde a c/u
    tipo_partida: str  # segun lo del documento regularizacion/cierre inicio   
    # NOTA TÉCNICA: Esto crea una lista anidada con los movimientos .
    # En el frontend se junta en el array 'payload.detalles' antes de hacer el fetch.
    detalles: List[PartidaDetalleInput]