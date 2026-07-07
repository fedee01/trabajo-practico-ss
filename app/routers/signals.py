import base64
import io

import numpy as np
import soundfile as sf
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.signals import (
    PinkNoiseRequest,
    SineSweepPairResponse,
    SineSweepRequest,
    SineSweepResponse,
    SyntheticIRRequest,
)
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
    buffer.seek(0)  # seek(0) mueve el puntero del buffer para que la lectura sea desde el inicio
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


def _array_a_base64_wav(signal: np.ndarray, fs: int) -> str:
    """Serializa un np.ndarray a WAV y lo codifica en base64 (sin tocar disco)."""
    buffer = io.BytesIO()
    sf.write(buffer, signal, fs, format="WAV", subtype="FLOAT")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


@router.post("/sine-sweep/pair", response_model=SineSweepPairResponse)
def crear_sine_sweep_par(payload: SineSweepRequest) -> SineSweepPairResponse:
    """Genera un sine sweep logaritmico para mediciones de respuesta en frecuencia y respuesta al
    impulso, o su filtroinverso si inverse=True.

    El audio se codifica en 32-bit float: al usarse como señal de excitacion para mediciones reales,
    se prioriza rango dinamico sobre tamano de archivo.
    """
    try:
        sweep, filtro_inverso = generar_sine_sweep(
            f1=payload.f1, f2=payload.f2, duracion=payload.duracion, fs=payload.fs
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    def _empaquetar(señal: np.ndarray, es_inverso: bool) -> SineSweepResponse:
        return SineSweepResponse(
            duration=payload.duracion,
            sample_rate=payload.fs,
            num_samples=len(señal),
            start_freq=payload.f1,
            end_freq=payload.f2,
            is_inverse=es_inverso,
            audio_base64=_array_a_base64_wav(señal, payload.fs),
        )

    return SineSweepPairResponse(
        sweep=_empaquetar(sweep, es_inverso=False),
        inverse_filter=_empaquetar(filtro_inverso, es_inverso=True),
    )


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
