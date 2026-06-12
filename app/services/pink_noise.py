import numpy as np
import sounddevice as sd

def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
    """
    Genera ruido rosa usando el algoritmo de Voss-McCartney.

    Parameters
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
    
    n_bits = 16
    n_muestras = int(duracion * fs)

    # array de la profundidad de bits elegida con los generadores de ruido
    generadores = np.random.randn(n_bits)  
    r_rosa = np.empty(n_muestras, dtype=np.float32)

    # Voss-McCartney, va sumando ruidos blancos que cambian cada 2**n
    for i in range(n_muestras):
        r_rosa[i] = float(np.sum(generadores))
        for n in range(n_bits):    
            if (i + 1) % (2**n) == 0:
                generadores[n] = np.random.randn()

    # normaliza
    max_val = float(np.max(np.abs(r_rosa)))
    if max_val > 0:
        r_rosa *= 0.9 / max_val

    # corre la funcion y espera a que termine
    sd.play(r_rosa, samplerate=fs)
    sd.wait()
    
    return r_rosa

# comprobacion (borrar al subir a main)
"""
if __name__ == "__main__":
    duracion = 3.0
    fs = 44100
    r_rosa = generar_ruido_rosa(duracion, fs)
    print(f"Reproduciendo ruido rosa de {duracion} s a {fs} Hz...")
"""
