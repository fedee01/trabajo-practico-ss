import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate, fftconvolve

from app.services.signal_utils import (
    obtener_ri_desde_sweep,
    sintetizar_ri,
)
from app.services.sine_sweep import generar_sine_sweep


def validar_obtener_ri_desde_sweep() -> float:
    """
    Valida la recuperación de una RI a partir de un sweep.

    Returns
    -------
    float
        Correlación cruzada normalizada.
    """

    fs = 44100

    # parametros del sweep + filtro inverso
    sweep, filtro_inverso = generar_sine_sweep(f1=20, f2=20000, duracion=5, fs=fs)

    # RI conocida (sintetizada)
    ri_original = sintetizar_ri(
        t60_por_banda={1000.0: 2.0},
        fs=fs,
        duracion=4.0,
    )

    # grabación simulada
    grabacion = fftconvolve(sweep, ri_original, mode="full")

    # recuperar RI
    ri_recuperada = obtener_ri_desde_sweep(grabacion, filtro_inverso)

    print("Longitud RI original:", len(ri_original))
    print("Longitud RI recuperada:", len(ri_recuperada))
    print("Pico original:", np.argmax(np.abs(ri_original)))
    print("Pico recuperada:", np.argmax(np.abs(ri_recuperada)))

    # alineo la RI original
    i_orig = np.argmax(np.abs(ri_original))  # índice del pico de la RI original
    ri_original = ri_original[
        i_orig : i_orig + len(ri_recuperada)
    ]  # recorto la RI original desde el pico hasta el final

    # igualo longitudes
    n = min(len(ri_original), len(ri_recuperada))
    ri_original = ri_original[:n]
    ri_recuperada = ri_recuperada[:n]

    # correlación normalizada
    corr = correlate(ri_recuperada, ri_original, mode="full")

    correlacion = np.max(np.abs(corr)) / (
        np.linalg.norm(ri_recuperada) * np.linalg.norm(ri_original)
    )  # normalización para obtener un valor entre 0 y 1

    # Plot: RI original vs recuperada
    t = np.arange(n) / fs
    plt.figure(figsize=(12, 5))
    plt.plot(t, ri_original, label="RI original")
    plt.plot(t, ri_recuperada, label="RI recuperada")
    plt.grid()
    plt.legend()
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title(f"RI original vs RI recuperada - Correlación = {correlacion:.4f}")
    plt.show()

    # Plot:Zoom primeros 100 ms
    muestras_zoom = min(int(0.1 * fs), n)
    plt.figure(figsize=(12, 5))
    plt.plot(t[:muestras_zoom], ri_original[:muestras_zoom], label="RI original")
    plt.plot(t[:muestras_zoom], ri_recuperada[:muestras_zoom], label="RI recuperada")
    plt.grid()
    plt.legend()
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title("Zoom primeros 100 ms")
    plt.show()

    return correlacion


if __name__ == "__main__":
    correlacion = validar_obtener_ri_desde_sweep()

    print()
    print(f"Correlación final = {correlacion:.4f}")
