"""Utilidades de procesamiento de senales.
Milestone 2: Procesamiento de la respuesta al impulso.
"""
import os
import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, filtfilt

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
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    try:
        data, fs = sf.read(ruta, dtype="float64")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de audio: {e}")

    # devuelve floats normalizados en [-1, 1] 
    data = np.asarray(data, dtype=np.float64)

    # como shape (n_channels, n_samples) — canales en filas, muestras en columnas.
    if data.ndim == 1:
        return data, int(fs)
    # data.ndim == 2: shape (n_samples, n_channels) -> convertir a (n_channels, n_samples)
    transposed = data.T.copy()
    return transposed, int(fs)


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
    n_samples = int(np.ceil(duracion * fs))
    t = np.arange(n_samples) / float(fs)

    out = np.zeros(n_samples, dtype=np.float64)

    for f0, t60 in t60_por_banda.items():
        f0 = float(f0)
        t60 = float(t60)
        if f0 <= 0:
            raise ValueError(f"Frecuencia central inválida: {f0}")
        if t60 <= 0:
            raise ValueError(f"T60 inválido para banda {f0} Hz: {t60}")

        noise = np.random.normal(scale=1.0, size=n_samples).astype(np.float64)

        # Diseño de filtro pasa-banda: usar ancho aproximado de octava (f0/sqrt(2) - f0*sqrt(2))
        low = f0 / np.sqrt(2.0)
        high = f0 * np.sqrt(2.0)

        nyq = fs / 2.0
        if high >= nyq:
            high = nyq * 0.999
        if low <= 0:
            low = 1.0

        wp = [low / nyq, high / nyq]
        # Orden razonable para bandpass
        b, a = butter(N=4, Wn=wp, btype="band")

        # Filtrado cero-fase con filtfilt
        try:
            filtered = filtfilt(b, a, noise)
        except Exception:
            # En caso de fallo del filtfilt (p. ej. bordes cortos), usar lfilter de respaldo
            from scipy.signal import lfilter

            filtered = lfilter(b, a, noise)

        # Envolvente exponencial a partir de T60: exp(-alpha * t)
        alpha = np.log(1000.0) / t60  # ln(1000) para -60 dB en T60
        envelope = np.exp(-alpha * t)

        band = filtered * envelope

        out += band

    # Normalizar respecto al máximo absoluto
    max_abs = np.max(np.abs(out))
    if max_abs == 0:
        return out
    out = out / max_abs
    return out


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
    # Convolucion por FFT (deconvolucion mediante convolucion con filtro inverso)
    try:
        ri_full = fftconvolve(grabacion, filtro_inverso, mode="full")
    except Exception as e:
        raise RuntimeError(f"Error durante la convolucion para obtener RI: {e}")

    ri_full = np.asarray(ri_full, dtype=np.float64)

    # Encontrar pico principal (llegada directa)
    peak_idx = int(np.argmax(np.abs(ri_full)))
    # Recortar para que comience en el pico o ligeramente antes (10 muestras antes si es posible)
    start = max(0, peak_idx - 10)
    ri_trim = ri_full[start:]

    # Normalizar respecto al pico
    peak_val = np.max(np.abs(ri_trim))
    if peak_val == 0:
        return ri_trim
    ri_trim = ri_trim / peak_val
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
    # evitar negativos por si la señal es compleja
    mag = np.abs(signal.astype(np.float64))

    # Evitar log(0): reemplazar por eps
    eps = np.finfo(float).eps
    mag_clipped = np.where(mag <= 0.0, eps, mag)

    db = 20.0 * np.log10(mag_clipped)

    # Normalizar para que el maximo sea 0 dB
    db = db - np.max(db)

    # Piso de ruido para evitar valores extremadamente negativos
    floor_db = -120.0
    db = np.maximum(db, floor_db)

    return db
