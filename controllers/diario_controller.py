from fastapi import HTTPException
from services.diario_service import DiarioService

# CAPA CONTROLLERS - MODULO LIBRO DIARIO Y MAYOR pal muchacho
# @jonas: Qué onda muchachos. Esta capa actúa como el intermediario o administrador.
# Su única función es recibir los datos limpios que vienen desde las rutas (HTTP),
# mandárselos al servicio contable para que haga la matemática, y empaquetar la
# respuesta final en un JSON simpel (status 200, 201 o errores 400/500).


class DiarioController:
    
    @staticmethod
    def crear_partida(partida):        
        #Gestiona la recepción de una nueva partida desde el cliente (JSON).
        #Delega la validación contable al servicio y maneja la respuesta HTTP.        
        # @jonas: aqui realizamos el traspaso de informacion del 
        # paquete 'partida' al Service contable,
        # disparamos la respuesta de éxito hacia el frontend.
        exito = DiarioService.registrar_nueva_partida(partida)
        if exito:
            return {
                "status": "Éxito", 
                "message": f"Partida No. {partida.numero_partida} registrada correctamente."
            }
        
        # Nota técnica:
        # uso del error de servidor (500)
        raise HTTPException(status_code=500, detail="No se pudo procesar la transacción.")

    @staticmethod
    def listar_diario():       
        #Retorna el JSON estructurado con el historial del Libro Diario.     
        # @jonas: Simple y directo. Mandamos a pedir la data ya procesada por los 
        # queries y la envolvemos en la estructura estándar de respuesta del grupo.
        return {
            "status": "Éxito", 
            "libro_diario": DiarioService.procesar_libro_diario()
        }

    @staticmethod
    def generar_mayor():      
        #Retorna la agregación de saldos listos para el Libro Mayor.       
        # nota para @aureo: De acá es de donde tu vista va a mandar a llamar los saldos.
        # Este controlador te entrega la lista limpia con los totales calculados por cuenta,
        # así tu módulo solo se preocupa por renderizar las pantallas.
        return {
            "status": "Éxito", 
            "libro_mayor": DiarioService.procesar_libro_mayor()
        }