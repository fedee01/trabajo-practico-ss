import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
    """
    Genera ruido rosa usando el algoritmo de Voss-McCartney.
import numpy as np


    Parámetros
    ----------
    duracion : float
        Duración de la señal en segundos.
    fs : int
        Frecuencia de muestreo en Hz.


    Returns
    -------
    np.ndarray
        Array con la señal de ruido rosa normalizada entre -1 y 1 (dtype float32).
    """
    n_bits = 16  # numero de bits, es decir numero de generadores
    n_muestras = int(duracion * fs)  # numero de muestras

    generadores = np.random.randn(n_bits)  # array de la profundidad de bits elegida con los generadores de ruido.
    r_rosa = np.empty(n_muestras, dtype=np.float32)

    for i in range(n_muestras):
        r_rosa[i] = float(np.sum(generadores))  # va sumando
        for n in range(n_bits):  # Voss-McCartney
            if (i + 1) % (2**n) == 0:
                generadores[n] = np.random.randn()


    max_val = float(np.max(np.abs(r_rosa)))  # normaliza
    if max_val > 0:
        r_rosa /= max_val

    return r_rosa


# parametros de ejemplo:

duracion = 3.0
fs = 44100
r_rosa = generar_ruido_rosa(duracion, fs)

# aca encontre la funcion magnitude spectrum: https://www.geeksforgeeks.org/python/plot-the-magnitude-spectrum-in-python-using-matplotlib/
# en la documentacion me fije como se usaba y que parametros pasarle https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.magnitude_spectrum.html
# me di cuenta que habia que usar la funcion psd, que relaciona los dB con los Hz, me fije en la documentacion aca https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.psd.html#matplotlib.pyplot.psd

plt.ylabel('PSD (dB/Hz)')
plt.xlabel('Frecuencia en Hz')
plt.title("Ruido rosa")

plt.psd(r_rosa, Fs=fs, color ='red', linewidth=1)
plt.xscale('log') 
plt.ylim([-85,-35]) 
plt.xlim([20,24000]) 
plt.show()

