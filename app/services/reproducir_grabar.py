"""Grabacion y Reproduccion en simultaneo.

Milestone 1: Generacion de senales.
"""

import numpy as np
import sounddevice as sd

PRE_ROLL = 0.5  # segundos


def reproducir_y_grabar(
    signal: np.ndarray,
    fs: int,
    duracion_grabacion: float,
) -> np.ndarray:
    """
    Reproduce una señal y graba simultáneamente.

    Se agrega automáticamente un silencio inicial (pre-roll) de 0.5 s y,
    si es necesario, un silencio final (post-roll) para completar la
    duración solicitada de la grabación y permitir capturar la cola de
    reverberación.

    Parameters
    ----------
    signal : np.ndarray
        Señal a reproducir.
    fs : int
        Frecuencia de muestreo en Hz.
    duracion_grabacion : float
        Duración total de la grabación en segundos.
        Debe ser mayor o igual que la duración de la señal reproducida.

    Returns
    -------
    np.ndarray
        Array con la señal grabada.

    Raises
    ------
    ValueError
        Si fs, duracion_grabacion o signal son inválidos (no positivos,
    señal vacía, o con más de 2 dimensiones).
    RuntimeError
        Si el dispositivo de audio no soporta la configuración solicitada,
    o si la duración grabada difiere en más de un 1% de la solicitada.
    """
    
    if fs <= 0:
        raise ValueError("la frecuencia de muestreo debe ser positiva")

    if duracion_grabacion <= 0:
        raise ValueError("la duración de grabación debe ser positiva")

    if signal.size == 0:
        raise ValueError("la señal no puede estar vacía")

    # acepta señal mono (1D) o estéreo/multicanal (2D)
    if signal.ndim == 1:
        channels = 1
    elif signal.ndim == 2:
        channels = signal.shape[1]
    else:
        raise ValueError("`signal` debe ser mono o estéreo (1D o 2D)")

    # ---------- Pre-roll ----------
    pre_roll = np.zeros(
        int(PRE_ROLL * fs),
        dtype=signal.dtype,
    )

    # duración de pre-roll + señal (sin contar el post-roll)
    playback_length = PRE_ROLL + signal.shape[0] / fs

    if duracion_grabacion < playback_length:
        raise ValueError(f"La duración de grabación debe ser al menos de {playback_length:.3f} s.")

    # ---------- Post-roll ----------
    extra_time = duracion_grabacion - playback_length
    post_roll_samples = int(round(extra_time * fs))

    if signal.ndim == 1:
        post_roll = np.zeros(
            post_roll_samples,
            dtype=signal.dtype,
        )

        senal_final = np.concatenate(
            (
                pre_roll,
                signal,
                post_roll,
            )
        )

    else:
        pre_roll_multi = np.tile(
            pre_roll.reshape(-1, 1),
            (1, channels),
        )

        post_roll = np.zeros(
            (post_roll_samples, channels),
            dtype=signal.dtype,
        )

        senal_final = np.concatenate(
            (
                pre_roll_multi,
                signal,
                post_roll,
            ),
            axis=0,
        )

    # verifica dispositivos de entrada y salida
    try:
        sd.check_input_settings(
            samplerate=int(fs),
            channels=channels,
        )

        sd.check_output_settings(
            samplerate=int(fs),
            channels=channels,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Problema con la configuración del dispositivo de audio: {exc}"
        ) from exc

    # normaliza la señal antes de reproducir
    max_abso = np.nanmax(np.abs(senal_final))

    if np.isfinite(max_abso) and max_abso > 0:
        senal_final = 0.9 * senal_final.astype(np.float32) / max_abso
    else:
        senal_final = senal_final.astype(np.float32)

    # reproducción y grabación simultáneas
    recording = sd.playrec(
        senal_final,
        samplerate=int(fs),
        channels=channels,
        dtype="float32",
    )

    sd.wait()

    # verifica que la duración grabada coincida con la solicitada (±1%)
    recorded_seconds = recording.shape[0] / float(fs)
    rel_diff = abs(recorded_seconds - duracion_grabacion) / duracion_grabacion
    if rel_diff > 0.01:
        raise RuntimeError(
            f"Duración de grabación inesperada: solicitada {duracion_grabacion:.6f}s, "
            f"registrada {recorded_seconds:.6f}s dando una diferencia del "
            f"({rel_diff * 100:.2f}%)")

    return recording
