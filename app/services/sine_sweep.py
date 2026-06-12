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

    if f1 == 0:  # si la frecuencia pedida es 0, se usa un numero muy pequeño en su lugar para no dividir por cero
        f1 += 1e-10

    t = np.linspace(0, duracion, int(duracion * fs)) 
    # crea un array de muestras de la duracion que se haya pedido, ubicando cada muestra a una distancia de igual tamano entre ellas. (eso hace el linspace)

# t = np.arange(n_muestras) / fs 

    sine_sweep = [ma.sin
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp(n * (ma.log(f2 / f1) / duracion) - 1))
                    / ma.log(f2 / f1)) 
                for n in t] 
    # aca hago la formula esa que esta en el apunte por cada muestra que necesito y lo meto todo en un array

# k = ma.log(f2 / f1) / duracion
# o = 2 * ma.pi * f1 / k
# fase = o * (np.exp(k * t) - 1)
# sine_sweep = np.sin(fase)
# filt_inv = np.sin(o * (np.exp(k * (duracion - t)) - 1)) * np.exp(-k * t)

    filt_inv = [ma.sin(
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp((duracion - n) * ma.log(f2 / f1) / duracion) - 1))
                            / ma.log(f2 / f1)) 
                / ma.exp(-n * ma.log(f2 / f1) / duracion) for n in t] 
    # lo mismo con el filtro, aplico la formula del apunte asignandole un seno a cada muestra


    funcion1 = np.asarray(sine_sweep, dtype=np.float64)
    max1 = float(np.max(np.abs(funcion1)))  # normaliza
    if max1 > 0:
        funcion1 /= max1


    funcion2 = np.asarray(filt_inv, dtype=np.float64)
    max2 = float(np.max(np.abs(funcion2)))  # normaliza
    if max2 > 0:
        funcion2 /= max2


    return funcion1, funcion2


if __name__ == "__main__":
    sweep, inverso = generar_sine_sweep(20, 4000, 1, 44100)
    sd.play(sweep)
    # si ponen [0] hace el sweep normal y si ponen [1] hace el inverso


    # y si en vez de lo otro ponen esto las convoluciona y hace cosas raras
    """
    ej = generar_sine_sweep(400, 4000, 1, 44100)
    sd.play(np.convolve(ej[0], ej[1], mode="full"), 44100)
    """
    sd.wait()
