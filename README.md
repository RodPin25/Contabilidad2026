# Proyecto de Contabilidad 2026

Dentro de este repositorio estará alojado el código backend de nuestro proyecto de contabilidad, desarrollado sobre **FastAPI** ⚡.

## 👥 Organización del Equipo
El trabajo se dividirá por módulos de la siguiente forma:
* **Inventario inicial** ➔ Sochito
* **Libro diario** ➔ Jonathan
* **Libro mayor** ➔ Aureo
* **Libros de estados financieros** ➔ Sebastian

---

## 🏗️ Arquitectura del Proyecto (N-Capas)
Para mantener el código ordenado, escalable y limpio, adoptaremos una arquitectura de **N-Capas**. El flujo de una petición HTTP seguirá estrictamente este orden de carpetas:

```
text
[Cliente] ➔ Routers ➔ Middlewares ➔ Controllers ➔ Services ➔ Database ➔ [BD]
                 ↳ (Schemas/Pydantic)
```
## Routes
Son los encargados de establecer los endpoints, mismos que llamaran a los controladores para recibir la información de la lógica de negocio.
## Middlewares
Son el paso intermedio entre la ruta y los controladores, serán los encargados de todo aquel proceso que no sea como tal lógica de negocio ni control de servicios. Principalmente se encargan de toda la autenticación, validación de rol, etc.
### Autenticación
La autenticación estará controlada por `Tokens JWT`, que tendrán una estructura básica de: 
```
token = {
    idUser: 1,
    usernameUser: ejemplo,
    roleUser: admin
}
```
## Controllers
Es la parte que se encarga de recibir la petición HTTP. Desde acá es donde se lleva el control de los servicios, para poder gestionarlos y acceder al servicio correspondiente a la petición y la recepción de parámetros de petición.
## Services
Es la parte donde se encuentra como tal toda la lógica de negocio. Se maneja toda la información proveniente de la base de datos, se realizan operaciones matemáticas, etc.

Son llamados y controlados por un `Controller` respectivo a cada uno de los servicios. 
## Database
Actua como mensajero, es la capa encargada de establecer conexión con la base de datos y comunicarse con ella. 

Se ejecutan `queries`, `stored procedures` (`procedimientos almacenados`) y se entrega la información o el resultado proveniente de la base de datos a los servicios para que puedan hacer uso de esa información.
# Uso de .gitignore
El archivo `.gitignore` se encuentra dentro de la carpeta raíz del proyecto, dentro del mismo tendra que ir configurado, con las dependencias del proyecto y variables de entorno. 

Ya que este archivo se utiliza para indicarle a git que archivos no tiene que subir al repositorio al hacer un commit. Si tienen archivos como por ejemplo `GEMINI.md` que son archivos para contextualizacion de herramientas de IA que funcionan en la terminal, tambien agreguenlos dentro de `.gitignore` 