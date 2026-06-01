from fastapi import APIRouter
from modelos.partida import PartidaInput
from controllers.diario_controller import DiarioController
# CAPA routes  

# @jonas:aca es la cara pública de nuestro módulo.
# Siguiendo la arquitectura de TATSebas, las rutas están "limpias". Su única función 
# es definir los endpoints HTTP y pasarle la bola rápido a 'DiarioController'.
router = APIRouter()
@router.post("/partidas/", status_code=201)
def registrar_partida(partida: PartidaInput):
    
    #Endpoint para recibir y procesar una nueva partida desde el frontend.    
    # @jonas: Recibe el JSON validado por Pydantic y se lo tira al controlador.
    return DiarioController.crear_partida(partida)


@router.get("/libro-diario/")
def obtener_libro_diario():
    
    #Endpoint para consultar el reporte completo del Libro Diario.  
    return DiarioController.listar_diario()


@router.get("/libro-mayor/")
def obtener_libro_mayor():
    
    #Endpoint para consultar los saldos acumulados (Libro Mayor) <-- pal muchacho aureo.
    
    #nota para: @aureo: De esta URL es clave para tu fetch para las 'T' gráficas.
    return DiarioController.generar_mayor()


@router.get("/cuentas-disponibles/")
def obtener_cuentas_disponibles():

    # NOTA DE INTEGRACIÓN: Hacemos una lectura rápida a la tabla 'cuenta' 
    # de Sochito para que el frontend pinte los nombres reales en el formulario de partidas.
    from configuracion.DataBase import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT idCuenta, nombreCuenta FROM Cuenta")
    cuentas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return cuentas