from sine_sweep import generar_sine_sweep
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

# para que les muestre los diferentes plots pongan:
# ploteo('sinesweep') - grafico espectral del sine sweep
# ploteo('convolucion') - convolucion del sine sweep y filtro inverso

def ploteo(plot):

    if plot == 'plotsinesweep' or plot == 'plotconvolucion':
        sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)

        # normalizacion de la convolucion
        convolucion = signal.fftconvolve(sweep, inverso, mode="full")

        if plot == 'plotsinesweep':

            # plot 1
            plt.figure(figsize=(10, 4))
            plt.specgram(sweep, Fs=fs)
            plt.yscale("log")
            plt.ylim([20, 20000])
            plt.xlabel("Tiempo [s]")
            plt.ylabel("Frecuencia [Hz]")
            plt.title("Sine Sweep Logaritmico")
            plt.show()

        elif plot == 'plotconvolucion':
            # plot 2: convolucion sweep x filtro inverso
            convolucion_normalizada = convolucion / np.max(np.abs(convolucion)) # normalizo tq pico sea 1
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

ploteo('plotconvolucion')