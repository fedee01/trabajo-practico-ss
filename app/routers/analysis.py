# app/routers/analysis.py

import tempfile
from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas.responses import (
    AnalysisSettings,
    BandResult,
    BroadbandAnalysisSettings,
    BroadbandParameters,
    FileInfo,
    ImpulseResponseByBandsResponse,
    ImpulseResponseResponse,
    NoiseAnalysis,
    ParametersByType,
)
from app.services.acoustic_parameters import calcular_parametros_acusticos, estimar_ruido_de_fondo
from app.services.signal_utils import cargar_audio

router = APIRouter()

_PARAMETROS_ISO3382 = ("T30", "T20", "T10", "EDT")
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


@router.post(
    "/impulse-response/by-bands",
    response_model=ImpulseResponseByBandsResponse,
    summary="Análisis completo de la RI por banda de octava",
    description=(
        "Analiza una RI en las 9 bandas de octava completas (31.5 Hz a 8 kHz): "
        "calcula EDT/T10/T20/T30 por banda, y estima el nivel de ruido y SNR "
        "sobre la señal completa. Al cubrir el espectro completo (a diferencia "
        "de /acoustics/parameters/by-bands, que usa solo las 6 bandas de la "
        "tabla de validación), permite diagnosticar en qué bandas la medición "
        "es mas confiable segun el SNR. No implementa el método de Lundeby "
        "(lundeby_applied siempre False)."
    ),
)
async def analizar_ri_por_bandas(file: UploadFile) -> ImpulseResponseByBandsResponse:
    data, fs, filename = await _leer_audio(file)

    try:
        resultado = calcular_parametros_acusticos(data, fs, bandas=BANDAS_OCTAVA_COMPLETAS)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    energia_ruido, snr_db = estimar_ruido_de_fondo(data)

    parameters = ParametersByType(
        **{p: {f"{fc:g}": v for fc, v in resultado[p].items()} for p in _PARAMETROS_ISO3382}
    )
    frecuencias = list(resultado["T30"].keys())
    band_results = {
        f"{fc:g}": BandResult(**{p: resultado[p][fc] for p in _PARAMETROS_ISO3382})
        for fc in frecuencias
    }

    return ImpulseResponseByBandsResponse(
        file_info=FileInfo(
            filename=filename,
            sample_rate=fs,
            duration=len(data) / fs,
            num_samples=len(data),
        ),
        analysis_settings=AnalysisSettings(
            bandwidth="octave", lundeby_applied=False, cutoff_time=None
        ),
        noise_analysis=NoiseAnalysis(estimated_noise_level=energia_ruido, estimated_snr_db=snr_db),
        center_frequencies=frecuencias,
        band_results=band_results,
        parameters=parameters,
    )


@router.post(
    "/impulse-response",
    response_model=ImpulseResponseResponse,
    summary="Análisis completo de la RI (banda completa)",
    description=(
        "Calcula EDT/T10/T20/T30 sobre la RI completa (sin filtrado por bandas) "
        "y estima el nivel de ruido y SNR. No implementa el método de Lundeby "
        "(lundeby_applied siempre False)."
    ),
)
async def analizar_ri(file: UploadFile) -> ImpulseResponseResponse:
    data, fs, filename = await _leer_audio(file)

    try:
        resultado = calcular_parametros_acusticos(data, fs, sin_filtrar=True)
        parametros = {p: resultado[p][0.0] for p in _PARAMETROS_ISO3382}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    energia_ruido, snr_db = estimar_ruido_de_fondo(data)

    return ImpulseResponseResponse(
        file_info=FileInfo(
            filename=filename,
            sample_rate=fs,
            duration=len(data) / fs,
            num_samples=len(data),
        ),
        analysis_settings=BroadbandAnalysisSettings(lundeby_applied=False, cutoff_time=None),
        noise_analysis=NoiseAnalysis(estimated_noise_level=energia_ruido, estimated_snr_db=snr_db),
        parameters=BroadbandParameters(**parametros),
    )
