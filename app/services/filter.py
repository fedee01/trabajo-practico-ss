"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
import scipy.signal 


def filtro_octava(x: np.ndarray, fc: float, fs: int, orden: int = 4) -> np.ndarray:
    """Aplica un filtro pasabanda de una octava centrado en ``fc``.

    Implementa un filtro Butterworth pasabanda cuyas frecuencias de corte
    corresponden a los limites de una banda de octava segun IEC 61260:
    - Frecuencia inferior: ``fc / sqrt(2)``
    - Frecuencia superior: ``fc * sqrt(2)``

    Parameters
    ----------
    x : np.ndarray
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
    f_inf = float(fc) / np.sqrt(2.0)
    f_sup = float(fc) * np.sqrt(2.0)

    # normalizar a Nyquist (Wn en [0, 1], donde 1 corresponde a Nyquist)
    nyq = float(fs) / 2.0
    wn0 = max(f_inf / nyq, 1e-12)
    wn1 = min(f_sup / nyq, 1.0 - 1e-12)

    # Manejar entradas multi-canal: convertir a mono tomando la media por canales
    if x.ndim > 1:
        sig = x.mean(axis=1)
    else:
        sig = x

    # Usar formato SOS para mayor estabilidad numérica en órdenes altos
    sos = scipy.signal.butter(orden, [wn0, wn1], btype='band', output='sos')

    # Filtrado cero-fase: forward + backward con sosfiltfilt
    try:
        y = scipy.signal.sosfiltfilt(sos, sig)
    except AttributeError:
        # Compatibilidad con versiones antiguas de scipy
        # Aplicar sosfilt forward y backward manualmente
        y_fwd = scipy.signal.sosfilt(sos, sig)
        y = scipy.signal.sosfilt(sos, y_fwd[::-1])[::-1]

    return y

    # return scipy.signal.filtfilt(b, a, signal)
