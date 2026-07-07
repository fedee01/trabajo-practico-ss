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


class SyntheticIRRequest(BaseModel):
    """Parametros para sintetizar una respuesta al impulso con T60 conocido por banda."""

    t60_por_banda: dict[float, float] = Field(
        description="Diccionario {frecuencia_central_Hz: T60_segundos}."
    )
    fs: int = Field(gt=0, default=48000, description="Frecuencia de muestreo en Hz.")
    duracion: float = Field(gt=0, description="Duracion total de la RI en segundos.")
