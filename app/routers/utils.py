import io
import tempfile
from pathlib import Path
from typing import Literal

import numpy as np
import soundfile as sf
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse

from app.schemas.responses import (
    LOG_SCALE_RESPONSE_HEADERS,
    SCHROEDER_RESPONSE_HEADERS,
    SMOOTHING_RESPONSE_HEADERS,
    LogScaleHeaders,
    SchroederHeaders,
    SmoothingHeaders,
)
from app.services.acoustic_parameters import integral_schroeder, suavizar_signal
from app.services.signal_utils import a_escala_log, cargar_audio

router = APIRouter()


async def _leer_audio(file: UploadFile) -> tuple[np.ndarray, int, str]:
    """Lee un UploadFile reusando cargar_audio de M2 (valida, mono, normaliza).

    Devuelve también el filename ya validado como str (no str | None).
    """
    if not file.filename or not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(status_code=422, detail="El archivo debe ser WAV o FLAC.")

    filename = file.filename
    contenido = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(contenido)
        tmp_path = tmp.name

    try:
        data, fs = cargar_audio(tmp_path)
    except (FileNotFoundError, TypeError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return data, fs, filename


def _empaquetar_npy(array: np.ndarray) -> io.BytesIO:
    """Serializa un array numpy a .npy en memoria, sin tocar disco."""
    buffer = io.BytesIO()
    np.save(buffer, array)
    buffer.seek(0)
    return buffer


@router.post(
    "/schroeder",
    summary="Calcula la integral de Schroeder de una RI",
    description=(
        "Calcula la integral de Schroeder de una respuesta al impulso."
        "La integral de Schroeder es una técnica para evaluar el decaimiento de energía en una"
        "respuesta al impulso, especialmente útil para análisis de reverberación."
        "No implementa el método de Lundeby"
    ),
    responses={
        200: {
            "description": "Curva de Schroeder serializada como .npy (float64, 1D).",
            "content": {"application/octet-stream": {}},
            "headers": SCHROEDER_RESPONSE_HEADERS,
        },
        422: {"description": "Archivo inválido."},
    },
)
async def aplicar_schroeder(file: UploadFile) -> StreamingResponse:
    data, fs, _ = await _leer_audio(file)

    try:
        curva_db = integral_schroeder(data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    buffer = _empaquetar_npy(curva_db)

    metadata = SchroederHeaders(
        num_samples=len(curva_db),
        t_max=len(curva_db) / fs,
        lundeby_applied=False,
    )
    headers = {"Content-Disposition": "attachment; filename=schroeder.npy"}
    headers.update(metadata.to_headers())

    return StreamingResponse(buffer, media_type="application/octet-stream", headers=headers)


@router.post(
    "/log-scale",
    summary="Convierte una señal a escala logarítmica (dB)",
    description=(
        "Convierte una señal a escala logarítmica (dB)."
        """Útil para visualización y análisis de decaimiento de señales.
        El resultado se normaliza al valor máximo (0 dB = máximo)."""
    ),
    responses={
        200: {
            "description": "Señal en escala dB serializada como .npy (float64, 1D).",
            "content": {"application/octet-stream": {}},
            "headers": LOG_SCALE_RESPONSE_HEADERS,
        },
        422: {"description": "Archivo inválido."},
    },
)
async def aplicar_log_scale(file: UploadFile) -> StreamingResponse:
    data, _, _ = await _leer_audio(file)

    try:
        curva_db = a_escala_log(data)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    buffer = _empaquetar_npy(curva_db)

    metadata = LogScaleHeaders(
        num_samples=len(curva_db),
        min_db=float(np.min(curva_db)),
        max_db=float(np.max(curva_db)),
    )
    headers = {"Content-Disposition": "attachment; filename=logscale.npy"}
    headers.update(metadata.to_headers())

    return StreamingResponse(buffer, media_type="application/octet-stream", headers=headers)


@router.post(
    "/smoothing",
    summary="Suaviza una señal para extraer su envolvente",
    description=(
        "Aplica suavizado a una señal para extraer su envolvente"
        "Suaviza la señal con la envolvente de Hilbert (recomendado, no requiere "
        "elegir ventana) o con media móvil de energía (requiere window_ms)."
    ),
    responses={
        200: {
            "description": "WAV con la señal suavizada.",
            "content": {"audio/wav": {}},
            "headers": SMOOTHING_RESPONSE_HEADERS,
        },
        422: {"description": "Archivo inválido, o window_ms faltante para moving_average."},
    },
)
async def aplicar_suavizado(
    file: UploadFile,
    method: Literal["hilbert", "moving_average"] = Query(
        "hilbert", description="Método de suavizado"
    ),
    window_ms: float | None = Query(
        None, gt=0, description="Ventana en ms (requerida si method=moving_average)"
    ),
) -> StreamingResponse:
    data, fs, _ = await _leer_audio(file)

    if method == "hilbert":
        suavizada = suavizar_signal(data, ventana="hilbert")
    else:
        if window_ms is None:
            raise HTTPException(
                status_code=422,
                detail="window_ms es requerido cuando method='moving_average'.",
            )
        ventana_muestras = max(int(window_ms / 1000 * fs), 1)
        suavizada = suavizar_signal(data, ventana=ventana_muestras)

    wav_buffer = io.BytesIO()
    sf.write(wav_buffer, suavizada, fs, format="WAV")
    wav_buffer.seek(0)

    metadata = SmoothingHeaders(method=method, window_ms=window_ms, num_samples=len(suavizada))
    headers = {"Content-Disposition": f"attachment; filename=smoothed_{method}.wav"}
    headers.update(metadata.to_headers())

    return StreamingResponse(wav_buffer, media_type="audio/wav", headers=headers)
