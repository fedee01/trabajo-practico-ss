"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
from scipy.signal import butter, filtfilt, lfilter

def filtro_octava(signal: np.ndarray, fc: float, fs: int, orden: int = 4) -> np.ndarray:
    """Aplica un filtro pasabanda de una octava centrado en ``fc``.

    Implementa un filtro Butterworth pasabanda cuyas frecuencias de corte
    corresponden a los limites de una banda de octava segun IEC 61260:
    - Frecuencia inferior: ``fc / sqrt(2)``
    - Frecuencia superior: ``fc * sqrt(2)``

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (array 1D).
    fc : float
        Frecuencia central de la banda de octava en Hz.
    fs : int
        Frecuencia de muestreo en Hz.
    orden : int, optional
        Orden del filtro Butterworth (por defecto 4).

    Returns
    -------
    np.ndarray
        Senal filtrada (array 1D).
    """
    nyq = float(fs) / 2.0
    low = float(fc) / np.sqrt(2.0)
    high = float(fc) * np.sqrt(2.0)

    if low <= 0:
        low = 1.0
    if high >= nyq:
        high = nyq * 0.999

    wn0 = low / nyq
    wn1 = high / nyq

    # evitar valores en los limites y asegurar wn0 < wn1
    eps = 1e-6
    wn0 = max(wn0, eps)
    wn1 = min(wn1, 1.0 - eps)

    # intenta filtfilt (cero-fase)
    # si es muy corta capturamos la excepción y usamos lfilter como respaldo.
    try:
        filtered = filtfilt(b, a, x)
    except Exception:
        filtered = lfilter(b, a, x)

    # Asegurar 1D y tipo float64
    filtered = np.asarray(filtered, dtype=np.float64).flatten()

    return filtered
