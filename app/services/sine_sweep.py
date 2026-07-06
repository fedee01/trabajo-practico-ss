"""Servicio de generacion de sine sweep logaritmico.

Milestone 1: Generacion de senales.
"""

import math as ma

import numpy as np


def generar_sine_sweep(
    f1: float, f2: float, duracion: float, fs: int
) -> tuple[np.ndarray, np.ndarray]:
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
        Raises
    ------
    ValueError
        Si f2 no es mayor que f1, o si duracion o fs no son positivos.
    """

    if f1 == 0:  # si la f pedida es 0, usa un numero muy chico para no dividir por 0
        f1 += 1e-10

    if f2 <= f1:
        raise ValueError("la frecuencia final (f2) debe ser mayor a la inicial (f1)")

    if duracion <= 0:
        raise ValueError("la duracion debe ser un numero positivo")

    if fs <= 0:
        raise ValueError("la frecuencia de muestreo debe ser un numero positivo")

    t = np.linspace(0, duracion, int(duracion * fs), endpoint=False)

    sine_sweep = np.array(
        [
            ma.sin(
                2
                * ma.pi
                * f1
                * duracion
                * (ma.exp(n * (ma.log(f2 / f1) / duracion)) - 1)
                / ma.log(f2 / f1)
            )
            for n in t
        ],
        dtype=float,
    )

    # rel entre la f final e inicial
    r = f2 / f1

    envolvente = np.exp(-t * np.log(r) / duracion)

    filt_inv = sine_sweep[::-1] * envolvente  # metodo de farina

    # normalizacion
    if np.max(sine_sweep) > 0:
        ratio = 2 / (np.max(sine_sweep) - np.min(sine_sweep))  # escalado a 2 [-1, 1]
        shift = (np.max(sine_sweep) + np.min(sine_sweep)) / 2
        # corre el centro al costado, no es el valor promedio
        sine_sweep_normalizada = (sine_sweep - shift) * ratio

    if np.max(filt_inv) > 0:
        ratio = 2 / (np.max(filt_inv) - np.min(filt_inv))
        shift = (np.max(filt_inv) + np.min(filt_inv)) / 2
        filt_inv_normalizado = (filt_inv - shift) * ratio

    return sine_sweep_normalizada, filt_inv_normalizado
