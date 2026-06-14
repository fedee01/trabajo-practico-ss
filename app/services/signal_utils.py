"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import os

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, filtfilt, sosfilt, sosfiltfilt


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

    if duracion <= 0:
        raise ValueError("duracion debe ser positiva")

    n_samples = int(np.ceil(duracion * fs)) #ceil es para redondear hacia arriba, así me aseguro de tener suficientes muestras para la duración pedida
    t = np.arange(n_samples, dtype=np.float64) / fs #acomoda las muestras a cada instante correspondiente del tiempo
    ri = np.zeros(n_samples, dtype=np.float64) #np.zeros para crear un array de ceros del tamaño necesario para la duración pedida, que es donde voy a ir sumando cada banda filtrada con su envolvente correspondiente
    nyq = fs / 2
    nyq = fs / 2

    for fc, t60 in t60_por_banda.items():
        fc = float(fc) #fc es la frecuencia central de la banda
        t60 = float(t60)

        if fc <= 0:
            raise ValueError(f"Frecuencia inválida: {fc}")

        if t60 <= 0:
            raise ValueError(f"T60 inválido: {t60}")

        noise = np.random.normal(loc=0.0, scale=1.0, size=n_samples) #np.random.normal para generar ruido blanco gaussiano, con media 0 y desviación estándar 1, del tamaño necesario para la duración pedida

        f_inf = fc / np.sqrt(2)

        f_sup = fc * np.sqrt(2)

        if f_sup >= nyq:

            f_sup = nyq * 0.999

        w = [f_inf / nyq, f_sup / nyq] # w es la frecuencia de corte normalizada para el filtro bandpass, con f_inf y f_sup como frecuencias de corte inferior y superior respectivamente, normalizadas por la frecuencia de nyquist

        sos = butter( N=4, Wn=w, btype="bandpass", output="sos") # sos es la representación en secciones de segundo orden del filtro Butterworth de orden 4, con las frecuencias de corte definidas por w, y tipo "bandpass"
                                                                 # butterworth es un filtro pasabandas

        filtered = sosfiltfilt(sos, noise) # filtro el ruido blanco con el filtro bandpass definido por sos, usando filtfilt para evitar desfases

        rms = np.sqrt(np.mean(filtered**2)) 

        if rms > 0:

            filtered /= rms

        alpha = np.log(1000.0) / t60 # alfa es el coeficiente de atenuación para la envolvente exponencial, calculado a partir del T60 pedido para esa banda
                                     # usando la fórmula que relaciona T60 con el tiempo que tarda la señal en atenuarse 1000 veces (60 dB)

        envelope = np.exp(-alpha * t) # envolvente exponencial que simula la decaimiento de la reverberación, 
                                      # con el coeficiente de atenuación alpha calculado a partir del T60 pedido para esa banda

        band = filtered * envelope # cada banda de la respuesta al impulso se obtiene multiplicando
                                   # el ruido filtrado por la envolvente exponencial correspondiente a esa banda

        ri += band #la sumatoria de todas las bandas

    # normalizado
    max_abs = np.max(np.abs(ri)) 
    if max_abs > 0:
        ri /= max_abs

    return ri


```python
import numpy as np
from scipy.signal import fftconvolve


def obtener_ri_desde_sweep(
    grabacion: np.ndarray,
    filtro_inverso: np.ndarray
) -> np.ndarray:
    """
    Obtiene la respuesta al impulso mediante
    deconvolución de un sine sweep.

    Parameters
    ----------
    grabacion : np.ndarray
        Señal grabada que contiene la respuesta de la sala.

    filtro_inverso : np.ndarray
        Filtro inverso del sweep utilizado.

    Returns
    -------
    np.ndarray
        Respuesta al impulso estimada, normalizada.
    """

    if not isinstance(grabacion, np.ndarray):
        raise TypeError(
            "grabacion debe ser un array numpy")

    if not isinstance(filtro_inverso, np.ndarray):
        raise TypeError(
            "filtro_inverso debe ser un array numpy")

    if grabacion.ndim > 1:
        grab = grabacion.mean(axis=1)
    else:
        grab = grabacion

    if filtro_inverso.ndim > 1:
        filt_inv = filtro_inverso.mean(axis=1)

    else:
        filt_inv = filtro_inverso
    grab = np.asarray(grab, dtype=np.float64)

    filt_inv = np.asarray(filt_inv, dtype=np.float64)

    if grab.size == 0:
        raise ValueError("grabacion vacía")

    if filt_inv.size == 0:
        raise ValueError("filtro_inverso vacío")

    ri_full = fftconvolve(grab, filt_inv, mode="full")

    peak_idx = np.argmax(np.abs(ri_full))

    ri = ri_full[peak_idx:]

    peak = np.max(np.abs(ri))

    if peak == 0:
        return ri

    threshold = 1e-6 * peak
    indices = np.where(np.abs(ri) >= threshold)[0]

    if indices.size > 0:
        ri = ri[:indices[-1] + 1]

    ri /= np.max(np.abs(ri))

    return ri

def a_escala_log(signal: np.ndarray) -> np.ndarray:
    """Convierte una senal a escala logaritmica (dB) normalizada.

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (array 1D).

    Returns
    -------
    np.ndarray
        Senal en escala logaritmica (dB), normalizada a 0 dB en el maximo.
    """
    if not isinstance(signal, np.ndarray):
        raise TypeError("signal debe ser un np.ndarray")

    # convierte a mono si es multicanal
    if signal.ndim > 1:
        sig = signal.mean(axis=1)
    else:
        sig = signal

    # evita negativos por si la señal es compleja
    mag = np.abs(sig.astype(np.float64))

    # evitar log(0): usar clip
    mag_safe = np.clip(mag, 1e-10, None)

    db = 20.0 * np.log10(mag_safe)

    # normalizar para que el maximo sea 0 dB
    db = db - np.max(db)

    piso_ruido = -120.0
    db = np.maximum(db, piso_ruido)

    return db
