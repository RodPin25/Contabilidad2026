from fastapi import HTTPException
import configuracion.diario_db as diario_db


# CAPA SERVICES (DLL german version)
# @jonas: aca es la capa de sumas para los debe y haber si hizo algo falta solo es agregar

class DiarioService:
    
    @staticmethod
    def registrar_nueva_partida(partida_data):
     
        # @jonas:  aqui se jala la informacion guardada para temas de proteccion 
        suma_debe = sum(d.debe for d in partida_data.detalles)
        suma_haber = sum(d.haber for d in partida_data.detalles)
        
        # NOTA TÉCNICA CRÍTICA: Usamos round(, 2) porque el python me dio muchos problemas 
        # con los decimales flotantes y podría rechazar partidas que sí cuadran como en los ejercicios de clase xd.
        if round(suma_debe, 2) != round(suma_haber, 2):
            # @jonas: Si no cuadra, disparamos un error (400 Bad Request).
            # Así evitamos que la base de datos se altere con información errónea.
            raise HTTPException(
                status_code=400, 
                detail=f"Error Contable: La partida no cuadra. Suma Debe: Q{suma_debe:.2f}, Suma Haber: Q{suma_haber:.2f}"
            )
            
        # para mis tatas @sochito @sebas: la matemática cuadra para la cantidad, 
        # e invocamos la capa 'diario_db' para que clave los datos en MySQL.
        return diario_db.database_guardar_partida(
            partida_data.numero_partida,
            partida_data.fecha,
            partida_data.descripcion,
            partida_data.tipo_partida,
            partida_data.detalles
        )

    @staticmethod
    def procesar_libro_diario():
       
        #@jonas: Solicita el historial del diario a la base de datos para gestion limpia.
       
        return diario_db.database_obtener_libro_diario()

    @staticmethod
    def procesar_libro_mayor():
        
        #@jonas: Solicita los saldos agregados y netos del Libro Mayor.
        
        return diario_db.database_obtener_libro_mayor()