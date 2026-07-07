# app/schemas/responses.py
"""Modelos de respuesta para analisis, acoustics y utils (M3).

Agrupa todo lo que no es request/response de senales (signals.py) ni de
filtrado (filters.py): son en su mayoria modelos de SALIDA, ya que estos
endpoints reciben poco mas que un UploadFile + query params sueltos.
"""

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Compartidos entre acoustics y analysis


class FileInfo(BaseModel):
    """Metadata del archivo de audio analizado."""

    filename: str
    sample_rate: int = Field(..., description="Frecuencia de muestreo en Hz")
    duration: float = Field(..., description="Duración en segundos")
    num_samples: int = Field(..., description="Número total de muestras")


class BandResult(BaseModel):
    """Parámetros acústicos para una única banda de frecuencia."""

    T30: float | None = None
    T20: float | None = None
    T10: float | None = None
    EDT: float | None = None


class ParametersByType(BaseModel):
    """Parámetros organizados por tipo, cada uno con un dict {frecuencia: valor}."""

    T30: dict[str, float]
    T20: dict[str, float]
    T10: dict[str, float]
    EDT: dict[str, float]


# ---------------------------------------------------------------------------
# /api/v1/acoustics/parameters/by-bands


class BandsSettings(BaseModel):
    """Configuración usada para el análisis por bandas."""

    bandwidth: str = Field(default="octave", description="Tipo de banda (octave/third)")
    t_max: float = Field(..., description="Tiempo máximo de análisis en segundos")


class ParametersByBandsResponse(BaseModel):
    """Respuesta completa de /api/v1/acoustics/parameters/by-bands."""

    file_info: FileInfo
    analysis_settings: BandsSettings
    center_frequencies: list[float]
    band_results: dict[str, BandResult] = Field(
        ..., description="Resultados por banda: {frecuencia: {T30, T20, T10, EDT}}"
    )
    parameters: ParametersByType = Field(
        ..., description="Resultados por parámetro: {T30: {frecuencia: valor}, ...}"
    )


# ---------------------------------------------------------------------------
# /api/v1/acoustics/parameters (banda completa)


class BroadbandParameters(BaseModel):
    """Parámetros acústicos de banda completa (sin filtrado por octava)."""

    T10: float
    T20: float
    T30: float
    EDT: float


class ParametersResponse(BaseModel):
    """Respuesta completa de /api/v1/acoustics/parameters."""

    file_info: FileInfo
    parameters: BroadbandParameters
    t_max_used: float = Field(..., description="Tiempo máximo de análisis usado, en segundos")


# ---------------------------------------------------------------------------
# /api/v1/analysis/impulse-response/by-bands


class NoiseAnalysis(BaseModel):
    """Estimación simplificada de ruido de fondo (no usa el método Lundeby)."""

    estimated_noise_level: float = Field(
        ..., description="Energía de ruido estimada en la cola de la RI"
    )
    estimated_snr_db: float = Field(..., description="SNR estimado en dB")


class AnalysisSettings(BaseModel):
    """Configuración usada para el análisis por bandas (/impulse-response/by-bands)."""

    bandwidth: str = Field(default="octave")
    lundeby_applied: bool = Field(
        default=False,
        description="Si se aplicó el método de Lundeby (no implementado en esta versión)",
    )
    cutoff_time: float | None = Field(
        default=None,
        description="Tiempo de corte de Lundeby, en segundos (null si no se aplicó)",
    )


class BroadbandAnalysisSettings(BaseModel):
    """Configuración usada para el análisis de banda completa (/impulse-response).

    Sin bandwidth: este endpoint no filtra por octava (sin_filtrar=True),
    por lo que ese campo no tiene sentido acá.
    """

    lundeby_applied: bool = Field(
        default=False,
        description="Si se aplicó el método de Lundeby (no implementado en esta versión)",
    )
    cutoff_time: float | None = Field(
        default=None,
        description="Tiempo de corte de Lundeby, en segundos (null si no se aplicó)",
    )


class ImpulseResponseByBandsResponse(BaseModel):
    """Respuesta completa de /api/v1/analysis/impulse-response/by-bands."""

    file_info: FileInfo
    analysis_settings: AnalysisSettings
    noise_analysis: NoiseAnalysis
    center_frequencies: list[float]
    band_results: dict[str, BandResult]
    parameters: ParametersByType


class ImpulseResponseResponse(BaseModel):
    """Respuesta completa de /api/v1/analysis/impulse-response (banda completa)."""

    file_info: FileInfo
    analysis_settings: BroadbandAnalysisSettings  # <- el fix
    noise_analysis: NoiseAnalysis
    parameters: BroadbandParameters


# ---------------------------------------------------------------------------
# /api/v1/utils/schroeder


class SchroederHeaders(BaseModel):
    """Metadata de /utils/schroeder, expuesta en headers (el body es un .npy binario)."""

    num_samples: int
    t_max: float = Field(..., description="Duración analizada, en segundos")
    lundeby_applied: bool = Field(default=False)

    def to_headers(self) -> dict[str, str]:
        return {
            "X-Num-Samples": str(self.num_samples),
            "X-T-Max": str(self.t_max),
            "X-Lundeby-Applied": str(self.lundeby_applied).lower(),
        }


SCHROEDER_RESPONSE_HEADERS = {
    "X-Num-Samples": {"schema": {"type": "integer"}},
    "X-T-Max": {"schema": {"type": "number"}, "description": "Duración analizada, en segundos"},
    "X-Lundeby-Applied": {"schema": {"type": "boolean"}},
}


# ---------------------------------------------------------------------------
# /api/v1/utils/log-scale


class LogScaleHeaders(BaseModel):
    """Metadata de /utils/log-scale, expuesta en headers (el body es un .npy binario)."""

    num_samples: int
    min_db: float
    max_db: float

    def to_headers(self) -> dict[str, str]:
        return {
            "X-Num-Samples": str(self.num_samples),
            "X-Min-Db": str(self.min_db),
            "X-Max-Db": str(self.max_db),
        }


LOG_SCALE_RESPONSE_HEADERS = {
    "X-Num-Samples": {"schema": {"type": "integer"}},
    "X-Min-Db": {"schema": {"type": "number"}},
    "X-Max-Db": {"schema": {"type": "number"}},
}


# ---------------------------------------------------------------------------
# /api/v1/utils/smoothing


class SmoothingHeaders(BaseModel):
    """Metadata de /utils/smoothing, expuesta en headers (el body es un WAV binario)."""

    method: str
    window_ms: float | None
    num_samples: int

    def to_headers(self) -> dict[str, str]:
        headers = {
            "X-Method": self.method,
            "X-Num-Samples": str(self.num_samples),
        }
        if self.window_ms is not None:
            headers["X-Window-Ms"] = str(self.window_ms)
        return headers


SMOOTHING_RESPONSE_HEADERS = {
    "X-Method": {"schema": {"type": "string"}},
    "X-Window-Ms": {
        "schema": {"type": "number"},
        "description": "Solo presente si method=moving_average",
    },
    "X-Num-Samples": {"schema": {"type": "integer"}},
}
