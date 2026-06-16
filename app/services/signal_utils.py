"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import os
import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfiltfilt

def cargar_audio(ruta: str) -> tuple[np.ndarray, int]:
    """Carga un archivo de audio y retorna la senal y la frecuencia de muestreo.

    Parameters
    ----------
    ruta : str
        Ruta al archivo de audio a cargar.

    Returns
    -------
    signal : np.ndarray
        Senal de audio como array 1D (mono).
    fs : int
        Frecuencia de muestreo del archivo en Hz.

    Raises
    ------
    FileNotFoundError
        Si el archivo especificado no existe.
    """
    # validacion
    if not isinstance(ruta, str):
        raise TypeError("'ruta' debe ser una cadena de texto")
    #si no es un string, no tiene sentido intentar cargar un archivo, así que lanzo un error de tipo

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    ext = os.path.splitext(ruta)[1].lower()

    if ext not in (".wav", ".flac"):
        raise ValueError(f"Formato '{ext}' no soportado. Sólo se aceptan archivos WAV o FLAC.")

    try:
        signal, fs = sf.read(ruta, dtype="float64")

    # cualquier error de lectura se captura y se lanza como RuntimeError con mensaje claro
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo: {e}") from e

    signal = np.asarray(signal,dtype=np.float64)

    if signal.ndim == 2:
        n_channels = signal.shape[1] #[1] es el numero de canales, [0] es el numero de muestras

        if n_channels not in (1, 2):
            raise ValueError(
                f"Número de canales inválido: "
                f"{n_channels}. "
                "Debe ser mono o estéreo.")
            
        signal = signal.mean(axis=1) # si es estéreo, promedia ambos canales para obtener mono

    elif signal.ndim != 1:
        raise ValueError("Formato de audio inválido.")

    if signal.size == 0:
        raise ValueError("El archivo de audio está vacío.")

    # normalizado
    max_abs = np.max(np.abs(signal))
    if max_abs > 0:
        signal = signal / max_abs

    return signal, int(fs)

def sintetizar_ri(t60_por_banda: dict[float, float], fs: int, duracion: float) -> np.ndarray:
    """Sintetiza una respuesta al impulso artificial a partir de valores T60 por banda.

    Parameters
    ----------
    t60_por_banda : dict[float, float]
        Diccionario {frecuencia_central_Hz: T60_segundos}.
    fs : int
        Frecuencia de muestreo en Hz.
    duracion : float
        Duracion de la respuesta al impulso en segundos.

    Returns
    -------
    np.ndarray
        Respuesta al impulso sintetizada (array 1D).
    """

    #validaciones
    if not isinstance(t60_por_banda, dict):
        raise TypeError("t60_por_banda debe ser un diccionario {fc:T60}")

    if len(t60_por_banda) == 0:
        raise ValueError("t60_por_banda no puede estar vacío")

    if fs <= 0:
        raise ValueError("fs debe ser positivo")

    n_samples = int(np.ceil(duracion * fs))                 # ceil es para redondear hacia arriba, así me aseguro de tener suficientes muestras para la duración pedida
    t = np.arange(n_samples, dtype=np.float64) / fs         # acomoda las muestras a cada instante correspondiente del tiempo
    ri_sintetizada = np.zeros(n_samples, dtype=np.float64)  # np.zeros crea array de ceros = a la duración pedida, donde voy a ir sumando cada banda filtrada con su envolvente
    nyq = fs / 2

    for fc, t60 in t60_por_banda.items():
        fc = float(fc) #fc es la frecuencia central de la banda
        t60 = float(t60)

        if fc <= 0:
            raise ValueError(f"Frecuencia inválida: {fc}")

        if t60 <= 0:
            raise ValueError(f"T60 inválido: {t60}")

        # ruido blanco
        noise = np.random.normal(loc=0.0, scale=1.0, size=n_samples) # np.random.normal genera ruido blanco gaussiano (media 0, desviación estándar 1) del tamaño de la duración pedida

        # filtro de octava
        f_inf = fc / np.sqrt(2)
        f_sup = fc * np.sqrt(2)

        if f_sup >= nyq:
            f_sup = nyq * 0.999

        if f_inf >= f_sup:
            raise ValueError(f"Banda inválida para fc={fc}")

        w = [f_inf / nyq, f_sup / nyq] # w es la fc normalizada para el filtro bandpass (f_inf y f_sup son frecs de corte inf y sup) normalizadas por la frec de nyquist

        sos = butter( N=4, Wn=w, btype="bandpass", output="sos") # sos es la representación en secciones de 2° orden del filtro Butterworth de orden 4, con las fc definidas por w y tipo "bandpass"
                                                                 # butterworth es un filtro pasabandas

        filtrado = sosfiltfilt(sos, noise) # filtro el ruido blanco con el filtro bandpass definido por sos (filtfilt para evitar desfases)

        # normalización RMS
        rms = np.sqrt(np.mean(filtrado**2)) 
        if rms > 0:
            filtrado /= rms

        # envolvente
        alfa = np.log(1000.0) / t60 # alfa es el coef de atenuación para la envolvente exponencial, calculado a partir del T60 pedido para esa banda
                                     # usando la fórmula que relaciona T60 con el tiempo que tarda la señal en atenuarse 1000 veces (60 dB)

        envolv = np.exp(-alfa * t) # envolvente exponencial que simula la decaimiento de la reverberación, 
                                      # con el alfa calculado a partir del T60 pedido para esa banda

        banda = filtrado * envolv # cada banda de la respuesta al impulso se obtiene multiplicando
                                   # el ruido filtrado por la envolvente exponencial correspondiente a esa banda

        ri_sintetizada += banda #la sumatoria de todas las bandas

    # normalizado
    max_abs = np.max(np.abs(ri_sintetizada)) 
    if max_abs > 0:
        ri_sintetizada /= max_abs

    return ri_sintetizada

def obtener_ri_desde_sweep(grabacion: np.ndarray, filtro_inverso: np.ndarray) -> np.ndarray:
    """
    Obtiene la respuesta al impulso (RI) mediante la deconvolución de una grabación realizada con un sine sweep.

    Parameters
    ----------
    grabacion : np.ndarray
        Señal grabada que contiene la respuesta de la sala al sine sweep. Puede ser mono o estéreo.

    filtro_inverso : np.ndarray
        Filtro inverso correspondiente al sine sweep utilizado.
        Puede ser mono o estéreo.

    Returns
    -------
    np.ndarray
        Respuesta al impulso estimada y normalizada entre -1 y 1.
    """
    # validación de tipos
    if not isinstance(grabacion, np.ndarray):
        raise TypeError("grabacion debe ser un array numpy")

    if not isinstance(filtro_inverso, np.ndarray):
        raise TypeError("filtro_inverso debe ser un array numpy")

    # conversión estéreo -> mono, se promedian para obtener una única señal mono.
    if grabacion.ndim == 2:
        grabacion = grabacion.mean(axis=1)

    elif grabacion.ndim != 1:
        raise ValueError("grabacion debe ser mono o estéreo")

    if filtro_inverso.ndim == 2:
        n_channels = filtro_inverso.shape[1]
        
        if n_channels not in (1, 2):
             raise ValueError(f"Número de canales inválido:{n_channels}. Debe ser mono o estéreo.")

        filtro_inverso = filtro_inverso.mean(axis=1)

    elif filtro_inverso.ndim != 1:
        raise ValueError("filtro_inverso debe ser mono o estéreo.")

    # conversión a float64
    grabacion = np.asarray(grabacion, dtype=np.float64)
    filtro_inverso = np.asarray(filtro_inverso, dtype=np.float64)

    # validación de arrays vacíos
    if grabacion.size == 0:
        raise ValueError("grabacion vacía")
    if filtro_inverso.size == 0:
        raise ValueError("filtro_inverso vacío")

    # deconvolución con FFT, la RI sale de convolucionar la grabación con el filtro inverso del sweep.
    ri_full = fftconvolve(grabacion, filtro_inverso, mode="full")

    # ubica el pico principal
    peak_idx = np.argmax(np.abs(ri_full))
    ri= ri_full[peak_idx:]
    # o se puede hacer ri= ri_full para no perder las primeras reflexiones
    # pero es más difícil medir el T60 después porque la curva no empieza en 0 dB
    # sino que tiene un pico inicial que puede ser mucho mayor que las reflexiones posteriores
    # lo que hace que la curva de decaimiento sea más difícil de analizar.
    # Al cortar desde el pico principal, me aseguro de que la curva de decaimiento empiece en 0 dB
    # y sea más fácil de medir el T60.

    # normalizado
    max_abs = np.max(np.abs(ri))
    if max_abs > 0:
        ri /= max_abs

    return ri

def a_escala_log(signal: np.ndarray) -> np.ndarray:
    """Convierte una señal a escala logarítmica (dB) normalizada.

    Parameters
    ----------
    signal : np.ndarray
        Señal de entrada.

    Returns
    -------
    np.ndarray
        Señal en escala logarítmica (dB), normalizada a 0 dB.
    """
    # validaciones (no se si son necesarias acá)
    if not isinstance(signal, np.ndarray):
        raise TypeError("signal debe ser un np.ndarray")

    if signal.size == 0:
        raise ValueError("signal no puede estar vacía")

    # pasar a mono si tiene mas canales
    if signal.ndim > 1:
        signal = signal.mean(axis=1)

    # protección contra log(0)
    safe = np.where(signal == 0, np.finfo(float).eps, np.abs(signal))

    # Normalización al máximo y conversión a dB
    db = 20 * np.log10(safe / np.max(safe))

    # piso de ruido opcional
    db = np.maximum(db, -120.0)

    return db
