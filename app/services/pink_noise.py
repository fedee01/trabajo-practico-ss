import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch
from scipy.stats import linregress


def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
    """
    Genera ruido rosa usando el algoritmo de Voss-McCartney.

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
    n_bits = 20  # numero de bits, es decir numero de generadores. acá cambié a 20 para que el ruido sea más suave.
    n_muestras = int(duracion * fs)  # numero de muestras

    generadores = np.random.randn(
        n_bits
    )  # array de la profundidad de bits elegida con los generadores de ruido.
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
duracion = 10.0
fs = 44100
r_rosa = generar_ruido_rosa(duracion, fs)

#acá empieza el calculo de la pendiente con welch
f, Pxx = welch(r_rosa, fs=fs, nperseg=8192) #pxx es el psd

mask = (f >= 100) & (f <= 10000) #acá tomo las frecuencias entre 100 y 1000 hz

x = np.log2(f[mask]) #acá expreso al eje x en escala logarítmica para que al hacer el primedio de la pendiente sea en db/octava
y = 10 * np.log10(Pxx[mask]) #esto me hace la escala y en db

pendiente, _, _, _, _ = linregress(x, y) #lineregress toma todos los puntos de la respuesta espectral y hace un ajuste lineal

#esta parte es la del gráfico
plt.figure()

plt.psd(r_rosa, Fs=fs, color="red", linewidth=1)

plt.xlabel("Frecuencia [Hz]")
plt.ylabel("PSD [dB/Hz]")
plt.xscale("log")

plt.xlim([20, 24000])
plt.ylim([-85, -35])

plt.title("Ruido rosa")

plt.text(
    0.6,
    0.95,
    f"Pendiente = {pendiente:.2f} dB/oct",
    transform=plt.gca().transAxes,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white"),
)
#plt.text es para poner la cajita con el valor de la pendiente

plt.show()
