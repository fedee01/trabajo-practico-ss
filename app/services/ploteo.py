import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import envelope, welch
from scipy.stats import linregress

from .pink_noise import generar_ruido_rosa
from .reproducir_grabar import reproducir_y_grabar
from .signal_utils import obtener_ri_desde_sweep, sintetizar_ri
from .sine_sweep import generar_sine_sweep

# parametros de ejemplo
fs = 44100
f1 = 20
f2 = 20000
duracion = 10

# hice una funcion que dependiendo que le pidan al llamarla devuelve uno de los plots:
# ploteo('plotsinesweep')       devuelve grafico espectral del sine sweep
# ploteo('plotconvolucion')     devuelve convolucion del sine sweep y filtro inverso
# ploteo('plotruidorosa')       devuelve grafico de ruido rosa
# ploteo('plotriAMP')           devuelve grafico de amplitud de nuestro RI sintetizado

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
            convolucion_normalizada = convolucion / np.max(np.abs(convolucion)) # normalizo tq
                                                                                #el pico sea 1
            indice_pico = np.argmax(np.abs(convolucion))  # busco el pico
            pico = np.max(np.abs(convolucion))
            ventana = 1000  # calculo el piso excluyendo una ventana alrededor del pico
            sin_pico = np.concatenate(
                (np.abs(convolucion[: indice_pico - ventana]),
                 np.abs(convolucion[indice_pico + ventana :]))
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
        duracion = 10
        fs = 44100
        r_rosa = generar_ruido_rosa(duracion, fs)

        # acá empieza el calculo de la pendiente con welch
        f, pxx = welch(r_rosa, fs=fs, nperseg=8192)  # pxx es el psd

        mask = (f >= 20) & (f <= 24000)  # tomo de 20 a 24000 hz

        x = np.log2(f[mask])  # eje x en escala logarítmica para  el promedio de la pendiente
        y = 10 * np.log10(pxx[mask]) 

        pendiente, _, _, _, _ = linregress(x, y)  # lineregress toma los puntos de la rta espectral y hace un ajuste lineal

        plt.figure(figsize=(10, 5))
        plt.psd(r_rosa, Fs=fs, color="pink", linewidth=2, label="ruido rosa")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("PSD [dB/Hz]")

        plt.xscale("symlog")
        plt.semilogx(range(20000))
        ax = plt.gca()
        ax.set_xscale("log")
        ax.xaxis.set_major_formatter(mt.ScalarFormatter())
        ax.xaxis.set_minor_formatter(mt.NullFormatter())

        plt.xticks([20,50,100,200,300,500,700,1000,2000,3000,5000,20000,10000,14000,7000,1400])
        
        # recta en escala logaritmica
        x = np.array([20, 20000])
        y = -3 * np.log2(x / 20) + 10 * np.log10(pxx[mask][0])

        plt.plot(x, y, "g--", label="Pendiente -3 dB/oct", linewidth=0.75)
        plt.xlim([100, 20000])
        plt.ylim([-85, -35])
        plt.title("Ruido rosa")

        plt.text(0.6,0.95,f"Pendiente = {pendiente:.2f} dB/oct",transform=plt.gca().transAxes,verticalalignment="top",bbox=dict(boxstyle="round", facecolor="white"),)
        plt.legend()
        plt.show()
        
    if plot == 'plotriAMP' or plot == 'plotriRMS':

        # parametros de ejemplo
        fs = 44100
        duracion = 4
        t60_segundos = 1.2

        biblioteca = {31.5: 1.5,63: 1.4,125: 1.3,250: 1.2,500: 1.1,1000: 1.0,2000: 0.9,4000: 0.8,8000: 0.7,16000: 0.6}
        ri = sintetizar_ri(biblioteca, fs, duracion)
        time = np.linspace(0, len(ri) / fs, num=len(ri))

        plt.figure(figsize=(12, 6), dpi=80)
        plt.title(f"IR sintética: t60 {t60_segundos:.1f} segundos, duración {duracion:.1f} segundos")
        plt.xlabel("Tiempo [s]")

        if plot == "plotriAMP":
            plt.ylabel("Amplitud normalizada")
            plt.xlim([-0.002, 0.8])
            plt.ylim([-1.02, 1.02])
            plt.plot(time, ri, linewidth=0.5)
            plt.grid()
            plt.show()

        elif plot == 'plotriRMS':
            # no se como hacer este
            envolvente = envelope(ri, residual=None)
            plt.ylabel("Envolvente RMS (dB)")
            plt.xlim([0, 4])
            plt.ylim([-80, 0])
            plt.plot(time, envolvente)
            plt.grid()
            plt.show()

    if plot == 'plotridesdesweep':
        fs = 44100
        duracion = 10

        sweep, inverso = generar_sine_sweep(f1, f2, duracion, fs)

        grabacion = reproducir_y_grabar(sweep, fs, duracion)
        ridesdesweep = obtener_ri_desde_sweep(grabacion, inverso)

        plt.ylabel("Amplitud dB")
        plt.xlabel("Amplitud dB")
        plt.xlim([0, 1.5])
        plt.ylim([-100, 0])
        plt.plot(ridesdesweep)
        plt.grid()
        plt.show()

ploteo('plotridesdesweep')
