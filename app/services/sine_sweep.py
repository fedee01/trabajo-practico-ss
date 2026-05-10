"""Servicio de generacion de sine sweep logaritmico.

Milestone 1: Generacion de senales.
"""
import numpy as np
import math as ma

def generar_sine_sweep(f1: float, f2: float, duracion: float, fs: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Genera un sine sweep logaritmico y su filtro inverso.

    Parameters
    ----------
    f1 : float
        Frecuencia inicial en Hz.
    f2 : float
        Frecuencia final en Hz.
    duracion : float
        Duracion del sweep en segundos.
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tupla con (sweep, filtro_inverso), ambos normalizados.
    """
    
    t = np.linspace(0, duracion, int(duracion * fs))
    
    sine_sweep = ma.sin(2 * ma.pi * f1 * duracion * (ma.exp(t * (ma.log(f2 / f1) / duracion) - 1)) / ma.log(f2 / f1))

    filt_inv = (ma.sin(2 * ma.pi * f1 * duracion * (ma.exp((duracion - t) * (ma.log(f2 / f1) / duracion) - 1)) / ma.log(f2 / f1))) / ma.exp(-t * ma.log(f2 / f1) / duracion)

    return sine_sweep * filt_inv
