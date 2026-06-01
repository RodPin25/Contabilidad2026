from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.diario import router as diario_router

app = FastAPI(title="API Contable - Módulo Libro Diario")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas en la capa de Routes :V
app.include_router(diario_router)