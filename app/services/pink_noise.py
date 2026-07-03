import numpy as np


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
    if duracion <= 0:
        raise ValueError("la duracion debe ser un numero positivo")
    if fs <= 0:
        raise ValueError("la frecuencia de muestreo debe ser un numero positivo")

    n_bits = 20
    n_muestras = int(duracion * fs)  # numero de muestras

    generadores = np.random.randn(n_bits)
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
