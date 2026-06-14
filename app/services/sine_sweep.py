"""Servicio de generacion de sine sweep logaritmico.


Milestone 1: Generacion de senales.
"""
import math as ma
import numpy as np
from scipy import signal
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

    if f1 == 0:  # si la frecuencia pedida es 0, se usa un numero muy pequeño en su lugar para no dividir por cero
        f1 += 1e-10

    t = np.linspace(0, duracion, int(duracion * fs)) 
    # crea un array de muestras de la duracion que se haya pedido, ubicando cada muestra a una distancia de igual tamano entre ellas. (eso hace el linspace)

    sine_sweep = [ma.sin
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp(n * (ma.log(f2 / f1) / duracion) - 1))
                    / ma.log(f2 / f1)) 
                for n in t] 
    # aca hago la formula esa que esta en el apunte por cada muestra que necesito y lo meto todo en un array

    filt_inv = [ma.sin(
                    (2 * ma.pi * f1 * duracion * 
                        (ma.exp((duracion - n) * ma.log(f2 / f1) / duracion) - 1))
                            / ma.log(f2 / f1)) 
                / ma.exp(-n * ma.log(f2 / f1) / duracion) for n in t] 
    # lo mismo con el filtro, aplico la formula del apunte asignandole un seno a cada muestra

    if np.max(sine_sweep) > 0:
        ratio = 2/(np.max(sine_sweep) - np.min(sine_sweep)) 
        #as you want your data to be between -1 and 1, everything should be scaled to 2, 
        #if your desired min and max are other values, replace 2 with your_max - your_min
        shift = (np.max(sine_sweep) + np.min(sine_sweep))/2 
        #now you need to shift the center to the middle, this is not the average of the values.
        sine_sweep_normalizada = (sine_sweep - shift)*ratio

    if np.max(filt_inv) > 0:
        ratio = 2/(np.max(filt_inv)-np.min(filt_inv)) 
        shift = (np.max(filt_inv)+np.min(filt_inv))/2 
        filt_inv_normalizado = (filt_inv - shift)*ratio

    return sine_sweep_normalizada, filt_inv_normalizado

# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)

#codigo para normalizar la convolucion
convolucion = signal.fftconvolve(sweep, inverso)

ratio = 2/(np.max(convolucion)-np.min(convolucion)) 
shift = (np.max(convolucion)+np.min(convolucion))/2 
convolucion_normalizada = (convolucion - shift)*ratio

# fuente https://stackoverflow.com/questions/10812189/creating-a-log-frequency-axis-spectrogram-using-specgram-in-matplotlib
# escalas logaritmicas: https://matplotlib.org/stable/gallery/scales/log_demo.html

# plot 1: sine sweep en escala logaritmica
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

# plot 2: convolucion con el filtro inverso (este no anda lol)
tiempo = np.linspace(0, duracion, num=len(convolucion))
plt2.ylabel('Amplitud normalizada')
plt2.xlabel('Tiempo respecto al pico (segundos)')
plt2.title("convolucion")
plt2.plot(tiempo, convolucion_normalizada)
# plt2.xlim([-5,5])
plt2.ylim([-1,1]) 
plt2.show()
