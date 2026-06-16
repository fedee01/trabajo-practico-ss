"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
import scipy.signal


def filtro_octava(signal: np.ndarray, fc: float, fs: int, orden: int = 4) -> np.ndarray:
    """Aplica un filtro pasabanda de una octava centrado en ``fc``.

    Implementa un filtro Butterworth pasabanda cuyas frecuencias
    de corte siguen la norma IEC 61260:

    - Frecuencia inferior: fc / sqrt(2)
    - Frecuencia superior: fc * sqrt(2)

    Parameters
    ----------
    signal : np.ndarray
        Señal de entrada.
    fc : float
        Frecuencia central de la banda de octava en Hz.
    fs : int
        Frecuencia de muestreo en Hz.
    orden : int, optional
        Orden del filtro Butterworth, por defecto 4.

    Returns
    -------
    np.ndarray
        Señal filtrada.
    """
    # validaciones
    if not isinstance(signal, np.ndarray):
        raise TypeError("signal debe ser un np.ndarray")

    if fc <= 0:
        raise ValueError("fc debe ser positiva")

    if fs <= 0:
        raise ValueError("fs debe ser positivo")

    if orden <= 0:
        raise ValueError("orden debe ser positivo")

    # convertir a mono si es multicanal
    if signal.ndim > 1:
        signal = signal.mean(axis=1)

    # límites de la banda IEC 61260
    f_inf = fc / np.sqrt(2)
    f_sup = fc * np.sqrt(2)

    nyquist = fs / 2

    if f_sup >= nyquist:
        raise ValueError("La frecuencia superior excede Nyquist")

    # frecuencias normalizadas
    W_inf = 2 * f_inf / fs
    W_sup = 2 * f_sup / fs

    # Butterworth en formato SOS
    sos = scipy.signal.butter(orden, [W_inf, W_sup], btype="bandpass", output="sos")

    # filtrado de fase cero
    senal_filtrada = scipy.signal.sosfiltfilt(sos, signal) 
    # sos es una lista de matrices de coef del filtro
    # sosfiltfilt aplica el filtro en ambas direcciones para evitar distorsión de fase

    return senal_filtrada
