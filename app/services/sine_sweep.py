"""Servicio de generacion de sine sweep logaritmico.


Milestone 1: Generacion de senales.
"""
import math as ma
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2

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

    if f1 == 0:  # asi no divide por cero
        f1 += 1e-10

    n_muestras = int(duracion * fs)

    t = np.arange(n_muestras) / fs
    k = ma.log(f2 / f1) / duracion
    o = 2 * ma.pi * f1 / k

    fase = o * (np.exp(k * t) - 1)
    sine_sweep = np.sin(fase)
    filt_inv = np.sin(o * (np.exp(k * (duracion - t)) - 1)) * np.exp(-k * t)

    funcion1 = np.asarray(sine_sweep, dtype=np.float64)
    max1 = float(np.max(np.abs(funcion1)))  # normaliza
    if max1 > 0:
        funcion1 /= max1

    funcion2 = np.asarray(filt_inv, dtype=np.float64)
    max2 = float(np.max(np.abs(funcion2)))  # normaliza
    if max2 > 0:
        funcion2 /= max2

    return funcion1, funcion2

#parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 5

sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)
convolucion = np.convolve(sweep, inverso, mode="full")

    # si ponen [0] hace el sweep normal y si ponen [1] hace el inverso
    # y si en vez de lo otro ponen esto las convoluciona y hace cosas raras

    # ej = generar_sine_sweep(400, 4000, 1, 44100)
    # sd.play(np.convolve(ej[0], ej[1], mode="full"), 44100)


# fuente https://stackoverflow.com/questions/10812189/creating-a-log-frequency-axis-spectrogram-using-specgram-in-matplotlib
# escalas logaritmicas: https://matplotlib.org/stable/gallery/scales/log_demo.html

# parece que matplotlib no tiene una forma directa de hacer graficos con escalas logaritmicas por lo que se tiene que usar Axes

plt.xlabel('Tiempo en segundos')
plt.ylabel('Frecuencia en Hz')
plt.title("Sine Sweep")
plt.yscale('symlog') 
    # esto setea la escala logaritmica en y
    # poner la escala en 'log' me estaba generando un grafico demasiado grande 
    # asi que lo cambie por 'symlog' aca se puede leer mas:
    # https://matplotlib.org/stable/gallery/scales/symlog_demo.html
    # symlog es mas util para rangos muy grandes de datos
plt.specgram(sweep, Fs=fs)
plt.ylim([20,20000]) 
plt.show()

# plt2.xlabel('frecuencia en Hz')
# plt2.title("sweep")
# plt2.psd(convolucion, Fs=fs, color ='green')
# plt2.show()