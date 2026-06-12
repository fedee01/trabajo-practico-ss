"""Servicio de generacion de sine sweep logaritmico.


Milestone 1: Generacion de senales.
"""
import math as ma
import numpy as np
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
    # para no dividir por cero
    if f1 == 0:  
        f1 += 1e-10

    # crea un array de muestras de la duracion que se haya pedido, ubicando cada muestra a una distancia de igual tamano entre ellas
    t = np.linspace(0, duracion, int(duracion * fs)) 
    
# t = np.arange(n_muestras) / fs 

    # hago la formula del apunte por cada muestra que necesito y lo meto en un array
    sine_sweep = [ma.sin
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp(n * (ma.log(f2 / f1) / duracion) - 1))
                    / ma.log(f2 / f1)) 
                for n in t] 
    

# k = ma.log(f2 / f1) / duracion
# o = 2 * ma.pi * f1 / k
# fase = o * (np.exp(k * t) - 1)
# sine_sweep = np.sin(fase)
# filt_inv = np.sin(o * (np.exp(k * (duracion - t)) - 1)) * np.exp(-k * t)

    # lo mismo con el filtro, aplico la formula del apunte asignandole un seno a cada muestra
    filt_inv = [ma.sin(
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp((duracion - n) * ma.log(f2 / f1) / duracion) - 1))
                            / ma.log(f2 / f1)) 
                / ma.exp(-n * ma.log(f2 / f1) / duracion) for n in t] 
    

    funcion1 = np.asarray(sine_sweep, dtype=np.float64)
    max1 = float(np.max(np.abs(funcion1))) 
    if max1 > 0:
        funcion1 *= 0.9 / max1    # normaliza

    funcion2 = np.asarray(filt_inv, dtype=np.float64)
    max2 = float(np.max(np.abs(funcion2)))  
    if max2 > 0:
        funcion2 *= 0.9 / max2    # normaliza

    sd.wait()
    return funcion1, funcion2
