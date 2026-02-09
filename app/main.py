from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.homicidios.routes import router as homicidios_router
from app.vbg.routes import router as vbg_router
from app.auth.routes import router as auth_router
from app.comparendos.routes import router as comparendos_router

app = FastAPI(
    title="API Seguridad y Justicia",
    description="API unificada para análisis de seguridad, justicia y violencias",
    version="1.0.0",
    openotispec_version="3.0.3",
    servers=[
        {"url": "https://api-seguridad.cali.gov.co", "description": "Producción"},
        {"url": "http://localhost:8000", "description": "Local"}
    ]
)

# ---------------------------
# Trusted hosts (IIS)
# ---------------------------
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "api-seguridad.cali.gov.co",
        "localhost",
        "127.0.0.1"
    ]
)

# ---------------------------
# CORS (OAuth2 compatible)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://api-seguridad.cali.gov.co",
        "https://rubendaristizabalo-pixel.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Health
# ---------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "API funcionando correctamente"}

# ---------------------------
# Routers
# ---------------------------
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(comparendos_router, prefix="/api/v1/comparendos", tags=["Comparendos"])
app.include_router(homicidios_router, prefix="/api/v1/homicidios", tags=["Homicidios"])
app.include_router(vbg_router, prefix="/api/v1/vbg", tags=["Violencias Basadas en Género"])
