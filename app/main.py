"""RIR-API - Room Impulse Response API.

Punto de entrada de la aplicacion FastAPI.

Uso:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.routers import health
from app.services.sine_sweep import generar_sine_sweep
from app.services.pink_noise import generar_ruido_rosa
from app.services.reproducir_grabar import reproducir_y_grabar
import sounddevice as sd

app = FastAPI(
    title="RIR-API",
    description="API para procesamiento y analisis de respuestas al impulso segun ISO 3382.",
    version="0.1.0",
)

# Routers
app.include_router(health.router)

# TODO (M3): Agregar routers de signals, filters, acoustics, analysis, utils
# app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])
# app.include_router(filters.router, prefix="/api/v1/filters", tags=["filters"])
# app.include_router(acoustics.router, prefix="/api/v1/acoustics", tags=["acoustics"])
# app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
# app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])


@app.get("/")
async def root():
    """Informacion basica de la API."""
    return {
        "name": "RIR-API",
        "version": "0.1.0",
        "description": "Room Impulse Response API",
        "docs": "/docs",
    }

sine_sweep = generar_sine_sweep(400,4000,1,44100)
pink_noise = generar_ruido_rosa(1,44100)

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    reproducir_y_grabar(sine_sweep,44100)
