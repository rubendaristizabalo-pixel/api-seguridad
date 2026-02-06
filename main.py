from fastapi import FastAPI
from auth import router as auth_router
from comparendos.routes import router as comparendos_router
from homicidios.routes import router as homicidios_router
from vbg.routes import router as vbg_router

app = FastAPI(title="API Seguridad y Justicia")

@app.get("/")
def root():
    return {"status": "API unificada funcionando"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(
    comparendos_router,
    prefix="/api/v1",
    tags=["Comparendos"]
)

app.include_router(
    homicidios_router,
    prefix="/api/v1",
    tags=["Homicidios"]
)

app.include_router(
    vbg_router,
    prefix="/api/v1",
    tags=["VbG"]
)

