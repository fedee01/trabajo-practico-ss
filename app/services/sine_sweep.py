"""Servicio de generacion de sine sweep logaritmico.

Milestone 1: Generacion de senales.
"""

import math as ma

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


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
    """

    if (f1 == 0):  # si la fcia pedida es 0, usa un numero muy chico para no dividir por 0
        f1 += 1e-10

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
        dtype=float,)
    
    R = (f2 / f1) #rel. entre la fcia final e inicial

    envolvente = np.exp(-t * np.log(R) / duracion)

    filt_inv = sine_sweep[::-1] * envolvente  #esto es el metodo de farina

    # normalizacion
    if np.max(sine_sweep) > 0:
        ratio = 2 / (np.max(sine_sweep) - np.min(sine_sweep)) #escalado a 2 -1 y 1
        shift = (np.max(sine_sweep) + np.min(sine_sweep)) / 2
        # now you need to shift the center to the middle, this is not the average of the values.
        sine_sweep_normalizada = (sine_sweep - shift) * ratio

    if np.max(filt_inv) > 0:
        ratio = 2 / (np.max(filt_inv) - np.min(filt_inv))
        shift = (np.max(filt_inv) + np.min(filt_inv)) / 2
        filt_inv_normalizado = (filt_inv - shift) * ratio

    return sine_sweep_normalizada, filt_inv_normalizado


# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)

# normalizacion de la convolucion
convolucion = signal.fftconvolve(sweep, inverso, mode="full")

# plot 1
plt.figure(figsize=(10, 4))
plt.specgram(sweep, Fs=fs)
plt.yscale("log")
plt.ylim([20, 20000])
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.title("Sine Sweep Logaritmico")
plt.show()

# plot 2: convolucion sweep x filtro inverso
convolucion_normalizada = convolucion / np.max(np.abs(convolucion)) #normalizo tq que el pico sea 1
indice_pico = np.argmax(np.abs(convolucion))  # busco el pico
pico = np.max(np.abs(convolucion))
ventana = 1000  # calculo el piso excluyendo una ventana alrededor del pico
sin_pico = np.concatenate(
    (np.abs(convolucion[: indice_pico - ventana]), np.abs(convolucion[indice_pico + ventana :]))
)
piso = np.mean(sin_pico)
relacion_db = 20 * np.log10(pico / piso)  # relacion pico/piso en dB
ancho = 1000  # muestro solo alrededor del impulso
inicio = indice_pico - ancho
fin = indice_pico + ancho
tiempo = np.arange(len(convolucion)) / fs
tiempo_relativo = tiempo[inicio:fin] - tiempo[indice_pico]

plt.figure(figsize=(10, 4))
plt.plot(tiempo_relativo, convolucion_normalizada[inicio:fin])
plt.xlabel("Tiempo respecto al pico [s]")
plt.ylabel("Amplitud normalizada")
plt.title(f"Convolucion Sweep x Filtro Inverso - SNR pico/piso = {relacion_db:.1f} dB")
plt.ylim([-1.1, 1.1])
plt.grid()
plt.show()
