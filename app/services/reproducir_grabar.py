"""Grabacion y Reproduccion en simultaneo.

Milestone 1: Generacion de senales.
"""

import sounddevice as sd
import numpy as np


def reproducir_y_grabar(
    signal: np.ndarray,
    fs: int,
    duracion_grabacion: float
) -> np.ndarray:
    """
    Reproduce una señal y graba simultáneamente.

    Parameters
    ----------
    signal : np.ndarray
        Señal a reproducir.
    fs : int
        Frecuencia de muestreo en Hz.
    duracion_grabacion : float
        Duración total de la grabación en segundos.
        Debe ser >= duración de la señal para capturar la reverberación.

    Returns
    -------
    np.ndarray
        Array con la señal grabada.
    """

    if duracion_grabacion < len(signal) / fs:
        raise ValueError("La duración de grabación debe ser mayor o igual a la duración de la señal.")

    if not sd.query_devices():
        raise RuntimeError("No se encontraron dispositivos de audio disponibles.")

    muestras_grabacion = int(duracion_grabacion * fs)

    # Pre-roll recomendado
    if signal.ndim == 1:
        pre_roll = np.zeros(int(0.5 * fs))
    else:
        pre_roll = np.zeros((int(0.5 * fs), signal.shape[1]))

    senal_final = np.concatenate((pre_roll, signal))

    # Ajustar exactamente a la duración pedida
    if len(senal_final) < muestras_grabacion:

        if signal.ndim == 1:
            padding = np.zeros(muestras_grabacion - len(senal_final), dtype=senal_final.dtype)
        else:
            padding = np.zeros(
                (muestras_grabacion - len(senal_final), signal.shape[1]), dtype=senal_final.dtype)

        senal_final = np.concatenate((senal_final, padding))

    else:
        senal_final = senal_final[:muestras_grabacion]

    # Normalización al 90 %
    max_abso = np.nanmax(np.abs(senal_final))

    if np.isfinite(max_abso) and max_abso > 0:
        senal_final = ( 0.9 * senal_final.astype(np.float32)) / max_abso
    else:
        senal_final = senal_final.astype(np.float32)

    grabacion = sd.playrec(senal_final, samplerate=fs, channels=signal.shape[1] if signal.ndim > 1 else 1, dtype="float32")

    sd.wait()

    return grabacion
