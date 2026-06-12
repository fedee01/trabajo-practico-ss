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

# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)
convolucion = np.convolve(sweep, inverso, mode="full")

# fuente https://stackoverflow.com/questions/10812189/creating-a-log-frequency-axis-spectrogram-using-specgram-in-matplotlib
# escalas logaritmicas: https://matplotlib.org/stable/gallery/scales/log_demo.html

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

tiempo = np.linspace(0, len(convolucion) / fs, num=len(convolucion))
plt2.ylabel('Amplitud normalizada')
plt2.xlabel('Tiempo respecto al pico (segundos)')
plt2.title("sweep")
plt2.plot(tiempo, convolucion)
# plt2.xlim([-5,5])
plt2.ylim([-1,1]) 
plt2.show()