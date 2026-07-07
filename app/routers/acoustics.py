import tempfile
from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException, Query, UploadFile

from app.schemas.responses import (
    BandResult,
    BandsSettings,
    BroadbandParameters,
    FileInfo,
    ParametersByBandsResponse,
    ParametersByType,
    ParametersResponse,
)
from app.services.acoustic_parameters import calcular_parametros_acusticos
from app.services.signal_utils import cargar_audio

router = APIRouter()

_PARAMETROS_EXPUESTOS = ("T30", "T20", "T10", "EDT")

BANDAS_VALIDACION_IEC61260: list[float] = [125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0]


async def _leer_audio(file: UploadFile) -> tuple[np.ndarray, int, str]:
    """Lee un UploadFile reusando cargar_audio de M2 (valida, mono, normaliza).

    Devuelve también el filename ya validado como str (no str | None),
    para que el resto del código no tenga que volver a chequearlo.
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
    "/parameters/by-bands",
    response_model=ParametersByBandsResponse,
    summary="Calcula parámetros acústicos por banda de octava",
    description=(
        """Filtra la respuesta al impulso en las bandas de octava de la tabla de validación
        IEC 61260 (125 Hz a 4 kHz) y calcula EDT, T10, T20, T30 para cada una. """
        """Implementa el método ISO 3382 para el cálculo de tiempos de reverberación:

        - EDT: Early Decay Time (0 a -10 dB)
        - T10: Tiempo de reverberación (-5 a -15 dB, extrapolado a -60 dB)
        - T20: Tiempo de reverberación (-5 a -25 dB, extrapolado a -60 dB)
        - T30: Tiempo de reverberación (-5 a -35 dB, extrapolado a -60 dB)"""
    ),
)
async def calcular_parametros_por_bandas(
    file: UploadFile,
    t_max: float | None = Query(None, description="Tiempo máximo de análisis en segundos"),
) -> ParametersByBandsResponse:
    data, fs, filename = await _leer_audio(file)

    duracion_total = len(data) / fs
    t_max_usado = t_max if t_max is not None else duracion_total

    if t_max is not None:
        n_max = int(t_max * fs)
        data = data[:n_max]

    try:
        resultado = calcular_parametros_acusticos(data, fs, bandas=BANDAS_VALIDACION_IEC61260)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    parameters = ParametersByType(
        **{
            parametro: {f"{fc:g}": valor for fc, valor in resultado[parametro].items()}
            for parametro in _PARAMETROS_EXPUESTOS
        }
    )

    frecuencias_calculadas = list(resultado["T30"].keys())
    band_results = {
        f"{fc:g}": BandResult(
            **{parametro: resultado[parametro][fc] for parametro in _PARAMETROS_EXPUESTOS}
        )
        for fc in frecuencias_calculadas
    }

    return ParametersByBandsResponse(
        file_info=FileInfo(
            filename=filename,
            sample_rate=fs,
            duration=duracion_total,
            num_samples=len(data),
        ),
        analysis_settings=BandsSettings(bandwidth="octave", t_max=t_max_usado),
        center_frequencies=frecuencias_calculadas,
        band_results=band_results,
        parameters=parameters,
    )


@router.post(
    "/parameters",
    response_model=ParametersResponse,
    summary="Calcula parámetros acústicos de banda completa",
    description=(
        """Calcula EDT, T10, T20, T30 sobre la respuesta al impulso completa,
        sin filtrado por bandas de octava."""
    ),
)
async def calcular_parametros(
    file: UploadFile,
    t_max: float | None = Query(None, description="Tiempo máximo de análisis en segundos"),
) -> ParametersResponse:
    data, fs, filename = await _leer_audio(file)

    duracion_total = len(data) / fs
    t_max_usado = t_max if t_max is not None else duracion_total

    if t_max is not None:
        n_max = int(t_max * fs)
        data = data[:n_max]

    try:
        resultado = calcular_parametros_acusticos(data, fs, sin_filtrar=True)
        parametros = {p: resultado[p][0.0] for p in ("T10", "T20", "T30", "EDT")}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ParametersResponse(
        file_info=FileInfo(
            filename=filename,
            sample_rate=fs,
            duration=duracion_total,
            num_samples=len(data),
        ),
        parameters=BroadbandParameters(**parametros),
        t_max_used=t_max_usado,
    )
