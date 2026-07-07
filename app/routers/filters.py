import io
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import soundfile as sf
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse

from app.schemas.filters import (
    BAND_FILTER_RESPONSE_HEADERS,
    SINGLE_BAND_RESPONSE_HEADERS,
    BandFilterHeaders,
    FrequenciesResponse,
    SingleBandFilterHeaders,
)
from app.services.filter import filtro_octava
from app.services.signal_utils import cargar_audio

router = APIRouter()


BANDAS_OCTAVA_COMPLETAS: list[float] = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000]


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


@router.get(
    "/frequencies",
    response_model=FrequenciesResponse,
    summary="Lista las frecuencias centrales disponibles",
    description=(
        """Obtiene las frecuencias centrales para bandas de octava.

    9 bandas (31.25 Hz a 8 kHz)"""
    ),
)
def obtener_frecuencias(
    bandwidth: str = Query("octave", description="Tipo de banda: 'octave' (único soportado)"),
) -> FrequenciesResponse:
    if bandwidth != "octave":
        raise HTTPException(
            status_code=400,
            detail="Solo 'octave' está implementado actualmente (no 'third').",
        )

    return FrequenciesResponse(
        bandwidth=bandwidth,
        frequencies=BANDAS_OCTAVA_COMPLETAS,
        num_bands=len(BANDAS_OCTAVA_COMPLETAS),
    )


@router.post(
    "/band",
    summary="Filtra un WAV en bandas de octava",
    description=("""
        Filtra una señal de audio en las 9 bandas de octava (31.5 Hz a 8 kHz)
        y devuelve un ZIP con un WAV por banda.
        Útil para análisis espectral por bandas.
        """
    ),
    responses={
        200: {
            "description": "ZIP con los WAV filtrados por banda.",
            "content": {"application/zip": {}},
            "headers": BAND_FILTER_RESPONSE_HEADERS,
        },
        422: {"description": "Archivo inválido, o fs demasiado bajo para cualquier banda."},
    },
)
async def filtrar_por_bandas(file: UploadFile) -> StreamingResponse:
    data, fs, _ = await _leer_audio(file)

    zip_buffer = io.BytesIO()
    frecuencias_incluidas: list[float] = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for fc in BANDAS_OCTAVA_COMPLETAS:
            try:
                filtrada = filtro_octava(data, fc=fc, fs=fs)
            except ValueError:
                continue

            wav_buffer = io.BytesIO()
            sf.write(wav_buffer, filtrada, fs, format="WAV")
            zf.writestr(f"filtered_octave_{fc:g}Hz.wav", wav_buffer.getvalue())
            frecuencias_incluidas.append(fc)

    if not frecuencias_incluidas:
        raise HTTPException(
            status_code=422,
            detail=f"fs={fs} Hz es demasiado bajo para filtrar ninguna banda de octava.",
        )

    zip_buffer.seek(0)

    metadata = BandFilterHeaders(
        sample_rate=fs,
        num_samples=len(data),
        bandwidth="octave",
        center_frequencies=frecuencias_incluidas,
    )
    headers = {"Content-Disposition": "attachment; filename=filtered_bands.zip"}
    headers.update(metadata.to_headers())

    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)


@router.post(
    "/single-band",
    summary="Filtra un WAV en una única banda de octava",
    description=(
        """Filtra una señal de audio en la banda especificada en `center_freq`. Devuelve el WAV.
        Permite seleccionar cualquier frecuencia central para el filtro de banda."""
    ),
    responses={
        200: {
            "description": "WAV filtrado en la banda solicitada.",
            "content": {"audio/wav": {}},
            "headers": SINGLE_BAND_RESPONSE_HEADERS,
        },
        400: {"description": "bandwidth no soportado."},
        422: {"description": "Archivo inválido, o banda inválida para el fs del archivo."},
    },
)
async def filtrar_banda_unica(
    file: UploadFile,
    center_freq: float = Query(..., gt=0, description="Frecuencia central en Hz"),
    bandwidth: str = Query("octave", description="Tipo de banda: 'octave' (único soportado)"),
) -> StreamingResponse:
    if bandwidth != "octave":
        raise HTTPException(
            status_code=400,
            detail="Solo 'octave' está implementado actualmente (no 'third').",
        )

    data, fs, _ = await _leer_audio(file)

    try:
        filtrada = filtro_octava(data, fc=center_freq, fs=fs)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Banda inválida para center_freq={center_freq} con fs={fs}: {exc}",
        ) from exc

    wav_buffer = io.BytesIO()
    sf.write(wav_buffer, filtrada, fs, format="WAV")
    wav_buffer.seek(0)

    metadata = SingleBandFilterHeaders(
        sample_rate=fs,
        num_samples=len(data),
        center_freq=center_freq,
        bandwidth=bandwidth,
    )
    headers = {"Content-Disposition": f"attachment; filename=filtered_{center_freq:g}Hz.wav"}
    headers.update(metadata.to_headers())

    return StreamingResponse(wav_buffer, media_type="audio/wav", headers=headers)
