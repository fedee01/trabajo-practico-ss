"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
<<<<<<< HEAD
from scipy.signal import butter, sosfilt, sosfiltfilt
=======
>>>>>>> dev


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
    if not isinstance(signal, np.ndarray):
        raise TypeError("signal debe ser un np.ndarray")

    if fc <= 0:
        raise ValueError("fc debe ser positiva")

<<<<<<< HEAD
    # Manejar entradas multi-canal: convertir a mono tomando la media por canales
    sig = x.mean(axis=1) if x.ndim > 1 else x

    # Usar formato SOS para mayor estabilidad numérica en órdenes altos
    sos = butter(orden, [wn0, wn1], btype="band", output="sos")

    # Filtrado cero-fase: forward + backward con sosfiltfilt
    try:
        y = sosfiltfilt(sos, sig)
    except AttributeError:
        # Compatibilidad con versiones antiguas de scipy
        # Aplicar sosfilt forward y backward manualmente
        y_fwd = sosfilt(sos, sig)
        y = sosfilt(sos, y_fwd[::-1])[::-1]

    return np.asarray(y)
=======
    if fs <= 0:
        raise ValueError("fs debe ser positivo")

    if orden <= 0:
        raise ValueError("orden debe ser positivo")

    if signal.ndim > 1:
        signal = signal.mean(axis=1)

    f_inf = fc / np.sqrt(2)
    f_sup = fc * np.sqrt(2)

    nyquist = fs / 2

    if f_sup >= nyquist:
        raise ValueError("La frecuencia superior excede Nyquist")

    W_inf = 2 * f_inf / fs
    W_sup = 2 * f_sup / fs

    sos = scipy.signal.butter(orden, [W_inf, W_sup], btype="bandpass", output="sos")

    senal_filtrada = scipy.signal.sosfiltfilt(sos, signal)

    return senal_filtrada
>>>>>>> dev
