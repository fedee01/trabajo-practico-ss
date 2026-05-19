"""Servicio de generacion de sine sweep logaritmico.

Milestone 1: Generacion de senales.
"""
import numpy as np
import math as ma
import sounddevice as sd

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
    
    t = np.linspace(0, duracion, int(duracion * fs)) # crea un array de muestras de la duracion que se haya pedido, ubicando cada muestra a una distancia de igual tamano entre ellas. (eso hace el linspace)
    
    sine_sweep = [ma.sin(2 * ma.pi * f1 * duracion * (ma.exp(n * (ma.log(f2 / f1) / duracion) - 1)) / ma.log(f2 / f1)) for n in t] # aca hago la formula esa que esta en el apunte por cada muestra que necesito y lo meto todo en un array

    filt_inv = [ma.sin(
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp((duracion - n) * ma.log(f2 / f1) / duracion) - 1))
                            / ma.log(f2 / f1)) 
                / ma.exp(-n * ma.log(f2 / f1) / duracion) for n in t] 
    # lo mismo con el filtro, aplico la formula del apunte asignandole un seno a cada muestra

    return tuple[sine_sweep, filt_inv] # devuelve en una tupla ambas senales

# para escuchar como suena descomenten este codigo y reemplacen el return de aca arriba por return sine_sweep 
# sd.play(generar_sine_sweep(400,4000,1,44100))
# sd.wait()

