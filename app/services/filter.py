"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt


def filtro_octava(x: np.ndarray, fc: float, fs: int, orden: int = 8) -> np.ndarray:
    """Aplica un filtro pasabanda de una octava centrado en ``fc``.

    Implementa un filtro Butterworth pasabanda cuyas frecuencias de corte
    corresponden a los limites de una banda de octava segun IEC 61260:
    - Frecuencia inferior: ``fc / sqrt(2)``
    - Frecuencia superior: ``fc * sqrt(2)``

    El filtrado es de fase cero (forward + backward) para no introducir
    retardo de grupo, lo cual es crítico para no inflar T60 en graves.

    Parameters
    ----------
    x : np.ndarray
        Senal de entrada (array 1D o 2D). Si es 2D, se asume multicanal
        (muestras, canales) y se promedia a mono antes de filtrar.
    fc : float
        Frecuencia central de la banda de octava en Hz.
    fs : int
        Frecuencia de muestreo en Hz.
    orden : int, optional
        Orden del filtro Butterworth (por defecto 8).

    Returns
    -------
    np.ndarray
        Senal filtrada (array 1D).

    Raises
    ------
    ValueError
        Si fc o fs no son positivos, o si la banda resultante es inválida
        (p. ej. f_sup >= nyquist sin margen para clipear).
    """
    if fc <= 0:
        raise ValueError(f"Frecuencia central inválida: {fc}")
    if fs <= 0:
        raise ValueError("fs debe ser positivo")

    f_inf = float(fc) / np.sqrt(2.0)
    f_sup = float(fc) * np.sqrt(2.0)

    # normalizar a Nyquist (Wn en [0, 1], donde 1 corresponde a Nyquist)
    nyq = float(fs) / 2.0
    wn0 = max(f_inf / nyq, 1e-12)
    wn1 = min(f_sup / nyq, 1.0 - 1e-12)

    if wn0 >= wn1:
        raise ValueError(f"Banda inválida para fc={fc} con fs={fs}")

    # Manejar entradas multi-canal: convertir a mono tomando la media por canales
    sig = x.mean(axis=1) if x.ndim > 1 else x

    # Usar formato SOS para mayor estabilidad numérica en órdenes altos
    sos = butter(orden, [wn0, wn1], btype="band", output="sos")

    # Filtrado cero-fase: forward + backward con sosfiltfilt
    try:
        y = sosfiltfilt(sos, sig)
    except AttributeError:
        # Compatibilidad con versiones antiguas de scipy sin sosfiltfilt
        y_fwd = sosfilt(sos, sig)
        y = sosfilt(sos, y_fwd[::-1])[::-1]

    return np.asarray(y)
