"""Grabacion y Reproduccion en simultaneo.

Milestone 1: Generacion de senales.
"""

import sounddevice as sd 
import numpy as np 

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

    pre_roll = np.zeros(int(0.5 * fs)) # Crea un array de silencio para el pre-roll
    senal_final = np.concatenate((pre_roll, signal)) # Concatena el pre-roll con la señal original
    
    if not sd.query_devices():
        raise RuntimeError("No se encontraron dispositivos de audio disponibles.") 
    
    grabacion = sd.playrec(senal_final, samplerate=fs, channels=signal.shape[1] if signal.ndim > 1 else 1, dtype='float32') # Reproducir y grabar simultáneamente
    sd.wait()  # Esperar a que la reproducción y grabación terminen

    return grabacion


