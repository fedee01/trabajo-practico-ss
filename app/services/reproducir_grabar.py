"""Grabacion y Reproduccion en simultaneo.

Milestone 1: Generacion de senales.
"""

from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


def reproducir_y_grabar(signal: np.ndarray, fs: int, duracion_grabacion: float) -> np.ndarray:
    """
    Reproduce una senal y graba simultaneamente.

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
    if fs <= 0:
        raise ValueError("la frecuencia de muestreo debe ser positiva")

    if signal.ndim == 1:
        channels = 1
    elif signal.ndim == 2:
        channels = signal.shape[1]
    else:
        raise ValueError("`signal` debe ser mono o stereo (1D o 2D)")

    if duracion_grabacion < len(signal) / fs:
        raise ValueError("La duración de grabación debe ser mayor o igual a la de la señal")

    pre_roll = np.zeros(int(0.5 * fs), dtype=signal.dtype)

    if signal.ndim == 1:
        senal_final = np.concatenate((pre_roll, signal))
    else:
        pre_roll_multi = np.tile(pre_roll.reshape(-1, 1), (1, channels))
        senal_final = np.concatenate((pre_roll_multi, signal), axis=0)

    playback_length = senal_final.shape[0] / float(fs)
    if duracion_grabacion < playback_length:
        raise ValueError(f"La duración de grabación debe ser al menos de ({playback_length:.3f}s)")

    try:
        sd.check_input_settings(samplerate=int(fs), channels=channels)
        sd.check_output_settings(samplerate=int(fs), channels=channels)
    except Exception as e:
        raise RuntimeError(f"Problema con la configuración del dispositivo de audio: {e}") from e

    pre_roll = np.zeros(int(0.5 * fs))  # Crea un array de silencio para el pre-roll
    senal_final = np.concatenate((pre_roll, signal))  # Concatena el pre-roll con la señal original

    if not sd.query_devices():
        raise RuntimeError("No se encontraron dispositivos de audio disponibles.")

    sd.wait()

    recording = sd.playrec(senal_final, samplerate=int(fs), channels=channels, dtype="float32")
    sd.wait()

    app_dir = Path(__file__).resolve().parent.parent.parent / "grabaciones"

    graba_num = 1
    filename = f"grabacion_{graba_num}.wav"
    while (app_dir / filename).exists():
        graba_num += 1
        filename = f"grabacion_{graba_num}.wav"

    out_path = app_dir / filename
    sf.write(str(out_path), recording, int(fs))

    return recording
