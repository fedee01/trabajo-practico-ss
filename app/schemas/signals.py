"""Schemas Pydantic para el router de generacion de senales (M3)."""

from pydantic import BaseModel, Field


class PinkNoiseRequest(BaseModel):
    """Parametros para generar ruido rosa."""

    duracion: float = Field(gt=0, description="Duracion en segundos.")
    fs: int = Field(gt=0, default=48000, description="Frecuencia de muestreo en Hz.")


class SineSweepRequest(BaseModel):
    """Parametros para generar un sine sweep logaritmico."""

    f1: float = Field(gt=0, description="Frecuencia inicial en Hz.")
    f2: float = Field(gt=0, description="Frecuencia final en Hz.")
    duracion: float = Field(gt=0, description="Duracion en segundos.")
    fs: int = Field(gt=0, default=48000, description="Frecuencia de muestreo en Hz.")
    inverse: bool = Field(
        default=False, description="Si True, devuelve el filtro inverso en lugar del sweep."
    )


class SineSweepResponse(BaseModel):
    """Metadata + audio de un sine sweep (o su filtro inverso), embebido en base64."""

    duration: float = Field(description="Duracion en segundos.")
    sample_rate: int = Field(description="Frecuencia de muestreo en Hz.")
    num_samples: int = Field(description="Numero de muestras.")
    start_freq: float = Field(description="Frecuencia inicial en Hz.")
    end_freq: float = Field(description="Frecuencia final en Hz.")
    is_inverse: bool = Field(description="Si True, es el filtro inverso; si False, es el sweep.")
    audio_base64: str = Field(description="Audio WAV codificado en base64.")


class SineSweepPairResponse(BaseModel):
    """Respuesta de /sine-sweep/pair: el sweep y su filtro inverso juntos."""

    sweep: SineSweepResponse
    inverse_filter: SineSweepResponse


class SyntheticIRRequest(BaseModel):
    """Parametros para sintetizar una respuesta al impulso con T60 conocido por banda."""

    t60_por_banda: dict[float, float] = Field(
        description="Diccionario {frecuencia_central_Hz: T60_segundos}."
    )
    fs: int = Field(gt=0, default=48000, description="Frecuencia de muestreo en Hz.")
    duracion: float = Field(gt=0, description="Duracion total de la RI en segundos.")
