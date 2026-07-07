"""Schemas para el filtrado por bandas de octava.

La respuesta de /api/v1/filters/band es un archivo binario (ZIP), por lo que
no hay un modelo Pydantic de body. Este schema documenta la metadata que
viaja en los headers HTTP de la respuesta.
"""

from pydantic import BaseModel, Field


class FrequenciesResponse(BaseModel):
    """Respuesta de /filters/frequencies: lista de frecuencias centrales disponibles."""

    bandwidth: str = Field(..., description="Tipo de banda: 'octave' (único soportado por ahora)")
    frequencies: list[float] = Field(..., description="Frecuencias centrales en Hz")
    num_bands: int = Field(..., description="Cantidad de bandas")


class BandFilterHeaders(BaseModel):
    """Metadata del filtrado por bandas, expuesta en los headers de la respuesta.

    No se usa como response_model (la respuesta es un ZIP binario), sino
    como fuente única de verdad para construir el dict de headers HTTP
    y para documentar el endpoint en /docs.
    """

    sample_rate: int = Field(..., description="Frecuencia de muestreo en Hz")
    num_samples: int = Field(..., description="Número de muestras del archivo original")
    bandwidth: str = Field(default="octave", description="Tipo de banda: 'octave' o 'third'")
    center_frequencies: list[float] = Field(
        ..., description="Frecuencias centrales de las bandas incluidas en el ZIP"
    )

    def to_headers(self) -> dict[str, str]:
        """Convierte el modelo a un dict de headers HTTP (todo como string)."""
        return {
            "X-Sample-Rate": str(self.sample_rate),
            "X-Num-Samples": str(self.num_samples),
            "X-Bandwidth": self.bandwidth,
            "X-Center-Frequencies": ",".join(f"{fc:g}" for fc in self.center_frequencies),
        }


# Documentación de los headers
BAND_FILTER_RESPONSE_HEADERS = {
    "X-Sample-Rate": {"schema": {"type": "integer"}, "description": "Frecuencia de muestreo en Hz"},
    "X-Num-Samples": {
        "schema": {"type": "integer"},
        "description": "Número de muestras del archivo original",
    },
    "X-Bandwidth": {
        "schema": {"type": "string"},
        "description": "Tipo de banda: 'octave' o 'third'",
    },
    "X-Center-Frequencies": {
        "schema": {"type": "string"},
        "description": "Frecuencias centrales incluidas en el ZIP, separadas por coma",
    },
}


class SingleBandFilterHeaders(BaseModel):
    """Metadata del filtrado de banda única, expuesta en los headers de la respuesta.

    Igual que BandFilterHeaders: no es un response_model (el body es un WAV
    binario), sino la fuente de verdad para construir los headers HTTP.
    """

    sample_rate: int = Field(..., description="Frecuencia de muestreo en Hz")
    num_samples: int = Field(..., description="Número de muestras del archivo original")
    center_freq: float = Field(..., description="Frecuencia central de la banda filtrada, en Hz")
    bandwidth: str = Field(default="octave", description="Tipo de banda: 'octave'")

    def to_headers(self) -> dict[str, str]:
        return {
            "X-Sample-Rate": str(self.sample_rate),
            "X-Num-Samples": str(self.num_samples),
            "X-Center-Freq": f"{self.center_freq:g}",
            "X-Bandwidth": self.bandwidth,
        }


SINGLE_BAND_RESPONSE_HEADERS = {
    "X-Sample-Rate": {"schema": {"type": "integer"}, "description": "Frecuencia de muestreo en Hz"},
    "X-Num-Samples": {
        "schema": {"type": "integer"},
        "description": "Número de muestras del archivo original",
    },
    "X-Center-Freq": {
        "schema": {"type": "string"},
        "description": "Frecuencia central filtrada, en Hz",
    },
    "X-Bandwidth": {"schema": {"type": "string"}, "description": "Tipo de banda: 'octave'"},
}
