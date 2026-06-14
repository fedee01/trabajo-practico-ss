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
    if not isinstance(t60_por_banda, dict):

        raise TypeError(
            "t60_por_banda debe ser "
            "un diccionario {fc:T60}"
        )

    if len(t60_por_banda) == 0:

        raise ValueError(
            "t60_por_banda no puede estar vacío"
        )

    if fs <= 0:

        raise ValueError(
            "fs debe ser positivo"
        )

    if duracion <= 0:

        raise ValueError(
            "duracion debe ser positiva"
        )

    n_samples = int(
        np.ceil(
            duracion * fs
        )
    )

    t = np.arange(
        n_samples,
        dtype=np.float64
    ) / fs

    ri = np.zeros(
        n_samples,
        dtype=np.float64
    )

    nyq = fs / 2

    for fc, t60 in t60_por_banda.items():

        fc = float(fc)
        t60 = float(t60)

        if fc <= 0:

            raise ValueError(
                f"Frecuencia inválida: {fc}"
            )

        if t60 <= 0:

            raise ValueError(
                f"T60 inválido: {t60}"
            )

        noise = np.random.normal(
            loc=0.0,
            scale=1.0,
            size=n_samples
        )

        f_inf = fc / np.sqrt(2)

        f_sup = fc * np.sqrt(2)

        if f_sup >= nyq:

            f_sup = nyq * 0.999

        w = [
            f_inf / nyq,
            f_sup / nyq
        ]

        sos = butter(
            N=4,
            Wn=w,
            btype="bandpass",
            output="sos"
        )

        filtered = sosfiltfilt(
            sos,
            noise
        )

        rms = np.sqrt(
            np.mean(
                filtered**2
            )
        )

        if rms > 0:

            filtered /= rms

        alpha = np.log(1000.0) / t60

        envelope = np.exp(
            -alpha * t
        )

        band = filtered * envelope

        ri += band

    max_abs = np.max(
        np.abs(ri)
    )

    if max_abs > 0:

        ri /= max_abs

    return ri


def obtener_ri_desde_sweep(grabacion: np.ndarray, filtro_inverso: np.ndarray) -> np.ndarray:
    """Obtiene la respuesta al impulso mediante deconvolucion de un sine sweep.

    Parameters
    ----------
    grabacion : np.ndarray
        Senal grabada que contiene la respuesta de la sala al sweep.
    filtro_inverso : np.ndarray
        Filtro inverso del sweep utilizado.

    Returns
    -------
    np.ndarray
        Respuesta al impulso estimada, normalizada.
    """
    if not isinstance(grabacion, np.ndarray) or not isinstance(filtro_inverso, np.ndarray):
        raise TypeError("grabacion y filtro_inverso deben ser arrays numpy")

    # convierte a mono si es multicanal
    if grabacion.ndim > 1:
        grab = grabacion.mean(axis=1)
    else:
        grab = grabacion
    if filtro_inverso.ndim > 1:
        filt_inv = filtro_inverso.mean(axis=1)
    else:
        filt_inv = filtro_inverso

    # Convolucion por FFT (deconvolucion mediante convolucion con filtro inverso)
    try:
        ri_full = fftconvolve(grab, filt_inv, mode="full")
    except Exception as e:
        raise RuntimeError(f"Error durante la convolucion para obtener RI: {e}")

    ri_full = np.asarray(ri_full, dtype=np.float64)

    # encontrar pico principal (llegada directa)
    peak_idx = int(np.argmax(np.abs(ri_full)))

    # recorta inicio (unos samples antes del pico) y recortar la cola donde la señal es insignificante
    start = max(0, peak_idx - 10)
    trimmed = ri_full[start:]

    peak_val = np.max(np.abs(trimmed))
    if peak_val == 0:
        return trimmed

    # busca último índice significativo (ej > 1e-6 * pico)
    thresh = 1e-6 * peak_val
    above = np.where(np.abs(trimmed) >= thresh)[0]
    if above.size == 0:
        ri_trim = trimmed
    else:
        end = above[-1] + 1
        ri_trim = trimmed[:end]

    # normaliza
    ri_trim = ri_trim / float(np.max(np.abs(ri_trim)))
    
    return ri_trim


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
