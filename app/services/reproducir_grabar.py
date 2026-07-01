"""Grabacion y Reproduccion en simultaneo.

Milestone 1: Generacion de senales.
"""

import numpy as np
import sounddevice as sd


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

    # acepta señal mono (1D) o multicanal (2D)
    if signal.ndim == 1:
        channels = 1
    elif signal.ndim == 2:  # verifica mono/stereo
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

    # duración mínima requerida (preroll + señal reproducida)
    playback_length = senal_final.shape[0] / float(fs)
    if duracion_grabacion < playback_length:
        raise ValueError(f"La duración de grabación debe ser al menos de ({playback_length:.3f}s)")

    n_samples_rec = int(round(duracion_grabacion * fs))

    # verifica dispositivos de entrada y salida
    try:
        sd.check_input_settings(samplerate=int(fs), channels=channels)
        sd.check_output_settings(samplerate=int(fs), channels=channels)
    except Exception as e:
        raise RuntimeError(f"Problema con la configuración del dispositivo de audio: {e}") from e

    # normaliza
    max_abso = np.nanmax(np.abs(senal_final))
    if np.isfinite(max_abso) and max_abso > 0:
        senal_final = 0.9 * senal_final.astype(np.float32) / max_abso
    else:
        senal_final = senal_final.astype(np.float32)

    recording = sd.rec(frames=n_samples_rec, samplerate=int(fs), channels=channels, dtype="float32")
    sd.play(senal_final, samplerate=int(fs))
    sd.wait()

    # verifica que la duración grabada coincida con la solicitada (± 1%)
    recorded_seconds = recording.shape[0] / float(fs)
    if duracion_grabacion > 0:
        rel_diff = abs(recorded_seconds - duracion_grabacion) / duracion_grabacion
        if rel_diff > 0.01:
            raise RuntimeError(
                f"Duración de grabación inesperada: solicitada {duracion_grabacion:.6f}s, "
                f"registrada {recorded_seconds:.6f}s dando una diferencia del "
                f"({rel_diff * 100:.2f}%)"
            )

    return recording
