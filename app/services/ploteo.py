import matplotlib.pyplot as plt
import numpy as np
from pink_noise import generar_ruido_rosa
from scipy import signal
from scipy.signal import welch
from scipy.stats import linregress
from sine_sweep import generar_sine_sweep

# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

# hice una funcion que dependiendo que le pidan al llamarla devuelve uno de los plots:
# ploteo('plotsinesweep')       devuelve grafico espectral del sine sweep
# ploteo('plotconvolucion')     devuelve convolucion del sine sweep y filtro inverso
# ploteo('plotruidorosa')       devuelve grafico de ruido rosa


def ploteo(plot):

    if plot == "plotsinesweep" or plot == "plotconvolucion":
        sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)

        # normalizacion de la convolucion
        convolucion = signal.fftconvolve(sweep, inverso, mode="full")

        if plot == "plotsinesweep":
            # plot 1
            plt.figure(figsize=(10, 4))
            plt.specgram(sweep, Fs=fs)
            plt.yscale("log")
            plt.ylim([20, 20000])
            plt.xlabel("Tiempo [s]")
            plt.ylabel("Frecuencia [Hz]")
            plt.title("Sine Sweep Logaritmico")
            plt.show()

        elif plot == "plotconvolucion":
            # plot 2: convolucion sweep x filtro inverso
            convolucion_normalizada = convolucion / np.max(np.abs(convolucion))
            indice_pico = np.argmax(np.abs(convolucion))  # busco el pico
            pico = np.max(np.abs(convolucion))
            ventana = 1000  # calculo el piso excluyendo una ventana alrededor del pico
            sin_pico = np.concatenate(
                (
                    np.abs(convolucion[: indice_pico - ventana]),
                    np.abs(convolucion[indice_pico + ventana :]),
                )
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

    if plot == "plotruidorosa":
        r_rosa = generar_ruido_rosa(duracion, fs)

        # acá empieza el calculo de la pendiente con welch
        f, pxx = welch(r_rosa, fs=fs, nperseg=8192)  # pxx es el psd

        mask = (f >= 100) & (f <= 10000)  # acá tomo las frecuencias entre 100 y 1000 hz

        x = np.log2(f[mask])
        y = 10 * np.log10(pxx[mask])

        pendiente, _, _, _, _ = linregress(x, y)

        # esta parte es la del gráfico
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
        # plt.text es para poner la cajita con el valor de la pendiente

        plt.show()


ploteo("plotruidorosa")
