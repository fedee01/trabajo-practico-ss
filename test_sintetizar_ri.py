import matplotlib.pyplot as plt
import numpy as np

from app.services.filter import filtro_octava
from app.services.signal_utils import sintetizar_ri


def validar_sintetizar_ri():
    """Validación manual de la síntesis de RI."""

    # Parámetros
    fs = 48000
    fc = 1000
    t60_objetivo = 2.0
    duracion = 4.0

    np.random.seed(0)

    # Sintetizar RI
    ri = sintetizar_ri(
        t60_por_banda={fc: t60_objetivo},
        fs=fs,
        duracion=duracion,
    )

    # Filtrar en banda de octava
    ri_filtrada = filtro_octava(x=ri, fc=fc, fs=fs)

    # Curva de Schroeder
    schroeder = np.cumsum((ri_filtrada**2)[::-1])[
        ::-1
    ]  # lo que hace es integrar la energía de la señal al revés, para obtener la curva de
    # decaimiento de la energía
    schroeder /= np.max(
        schroeder
    )  # normaliza la curva de Schroeder dividiéndola por su valor máximo, para que el nivel máximo
    # corresponda a 0 dB
    schroeder_db = 10 * np.log10(schroeder + np.finfo(float).eps)

    print("Mínimo:", np.min(schroeder_db))
    print("Máximo:", np.max(schroeder_db))

    # Tiempo donde cruza -60 dB
    indices = np.where(schroeder_db <= -60)[
        0
    ]  # busca los índices donde la curva de Schroeder cae por debajo de -60 dB, lo que indica el
    # tiempo de reverberación T60

    if len(indices) == 0:
        print("La curva no alcanza -60 dB")
        return "No se pudo medir T60"

    idx_t60 = indices[0]

    t60_medido = (
        idx_t60 / fs
    )  # convierte el índice del cruce a tiempo dividiendo por la frecuencia de muestreo

    error = abs(t60_medido - t60_objetivo) / t60_objetivo * 100

    print(f"T60 objetivo: {t60_objetivo:.2f} s")
    print(f"T60 medido:   {t60_medido:.2f} s")
    print(f"Error:        {error:.2f} %")

    # Plot: curva de decaimiento energético de la respuesta al impulso
    t = np.arange(len(schroeder_db)) / fs

    plt.plot(t, schroeder_db)

    plt.scatter(
        t60_medido,
        -60,
    )
    plt.axhline(
        -60,
        linestyle="--",
    )

    plt.axvline(
        t60_medido,
        linestyle="--",
    )
    texto = (
        f"T60 objetivo: {t60_objetivo:.2f} s\nT60 medido: {t60_medido:.2f} s\nError: {error:.2f} %"
    )

    plt.text(
        0.65,
        0.95,
        texto,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    plt.xlabel("Tiempo [s]")
    plt.ylabel("Nivel [dB]")
    plt.grid(True)
    plt.legend()
    plt.title("Curva de decaimiento energético de la RI sintetizada")
    plt.show()


validar_sintetizar_ri()
