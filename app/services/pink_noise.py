"""Servicio de generacion de ruido rosa.

Milestone 1: Generacion de senales.
"""
import numpy as np
import soundfile as sf
import sounddevice as sd

def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
    """
    Genera ruido rosa creando ruido blanco y aplicando un filtro.

    Parámetros
    ----------
    duracion : float
        Duración de la señal en segundos.
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    np.ndarray
        Array con la senal de ruido rosa normalizada entre -1 y 1.
    """
    
    n_bits = 16;                # numero de bits, es decir numero de generadores
    n_muestras = int(duracion * fs)  # numero de muestras    

    generadores = [np.array(np.random.randn(n_muestras)) for n in range(0, n_bits)] # array de la profundidad de bits elegida con los generadores de ruido.
    r_rosa = np.array(sum(generadores)) # la primera muestra del ruido rosa va a ser la suma de los generadores 
    contador = 0 # contador que voy a usar para controlar cuando actualizar los arrays
    
    # con un for armo mi senal sumando los generadores en cada muestra
    for i in range(0,n_muestras):
        contador += 1 
        np.append(r_rosa,sum(generadores)) # en cada muestra agrego mi suma de generadores

        for n in range(0, n_bits): # en la consigna dice que los generadores i tienen que actualizarse cada 2^i (supongo que muestras), asi que aca itero por mi numero de bits (o sea el numero de generadores) y me fijo si la cantidad de muestras que ya sume coincide con 2^i, si lo hace actualizo los generadores
            if contador == 2 ** n: 
                generadores[n] = np.random.randn(n_muestras)
    return r_rosa

# descomenten esto para escuchar como suena (tarda un rato asi q paciencia)
# sd.play(generar_ruido_rosa(1,44100))
# sd.wait()
