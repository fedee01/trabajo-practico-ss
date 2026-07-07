import io

import numpy as np
import soundfile as sf
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.signals import PinkNoiseRequest, SineSweepRequest, SyntheticIRRequest
from app.services.pink_noise import generar_ruido_rosa
from app.services.signal_utils import sintetizar_ri
from app.services.sine_sweep import generar_sine_sweep

router = APIRouter()


def _array_a_wav_response(signal: np.ndarray, fs: int, filename: str) -> StreamingResponse:
    """Serializa un np.ndarray como respuesta HTTP de tipo audio/wav.

    Usa subtype="FLOAT" (32-bit) en vez del PCM_16 por defecto: estas señales
    se usan como excitacion para mediciones acusticas reales (no para
    escuchar), asi que se prioriza rango dinamico sobre tamano de archivo.
    """
    buffer = io.BytesIO()
    sf.write(buffer, signal, fs, format="WAV", subtype="FLOAT")
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="audio/wav",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/pink-noise")
def crear_ruido_rosa(payload: PinkNoiseRequest) -> StreamingResponse:
    """Genera ruido rosa aplicando algoritmo de Voss-Mccartney y lo devuelve como archivo WAV.

    El ruido rosa tiene una densidad espectral de potencia inversamente proporcional
    a la frecuencia (1/f). Como resultado tiene igual energía por octava.

    El método Voss produce ruido rosa con mejor distribución espectral por octava,
    ideal para aplicaciones que requieren precisión en las bandas de frecuencia.
    """
    try:
        signal = generar_ruido_rosa(duracion=payload.duracion, fs=payload.fs)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _array_a_wav_response(signal, payload.fs, "pink_noise.wav")


@router.post("/sine-sweep")
def crear_sine_sweep(payload: SineSweepRequest) -> StreamingResponse:
    """Genera un sine sweep logaritmico para mediciones de respuesta en frecuencia y respuesta al
    impulso, o su filtro inverso si inverse=True.

    El audio se codifica en 32-bit float: al usarse como señal de excitacion para mediciones reales,
    se prioriza rango dinamico sobre tamano de archivo.
    """
    try:
        sweep, filtro_inverso = generar_sine_sweep(
            f1=payload.f1, f2=payload.f2, duracion=payload.duracion, fs=payload.fs
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if payload.inverse:
        return _array_a_wav_response(filtro_inverso, payload.fs, "inverse_filter.wav")
    return _array_a_wav_response(sweep, payload.fs, "sweep.wav")


@router.post("/synthetic-ir")
def crear_ir_sintetica(payload: SyntheticIRRequest) -> StreamingResponse:
    """Sintetiza una respuesta al impulso con T60 conocido por banda."""
    try:
        ri = sintetizar_ri(
            t60_por_banda=payload.t60_por_banda, fs=payload.fs, duracion=payload.duracion
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _array_a_wav_response(ri, payload.fs, "synthetic_ir.wav")
