from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.comparendos.routes import router as comparendos_router
from app.homicidios.routes import router as homicidios_router
from app.vbg.routes import router as vbg_router
from app.auth.routes import router as auth_router

app = FastAPI(
    title="API Seguridad y Justicia",
    description="API unificada para análisis de seguridad, justicia y violencias",
    version="1.0.0",
    openapi_version="3.0.3",
        servers=[
        {
        {"url": "http://127.0.0.1:8000", "description": "Local"},
        {"url": "https://api-seguridad.cali.gov.co", "description": "Producción"},
        }
    ]
)

# ---------------------------
# CORS (clave para GitHub Pages)
# ---------------------------

origins = [
    "https://rubendaristizabalo-pixel.github.io/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Root / Health
# ---------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "API funcionando correctamente"}

# ---------------------------
# Routers
# ---------------------------
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)

app.include_router(
    comparendos_router,
    prefix="/api/v1/comparendos",
    tags=["Comparendos"]
)

app.include_router(
    homicidios_router,
    prefix="/api/v1/homicidios",
    tags=["Homicidios"]
)

app.include_router(
    vbg_router,
    prefix="/api/v1/vbg",
    tags=["Violencias Basadas en Género"]
)

