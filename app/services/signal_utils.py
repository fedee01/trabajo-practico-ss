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
        raise TypeError("'ruta' debe ser una cadena con la ruta al archivo de audio")

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    try:
        data, fs = sf.read(ruta, dtype="float64")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de audio: {e}")

    # asegura dtype float64
    data = np.asarray(data, dtype=np.float64)

    # se fija si la frecuencia viene del header del archivo
    try:
        info = sf.info(ruta)
        fs = int(info.samplerate)
    except Exception:
        fs = int(fs)

    # normaliza
    max_abs = np.max(np.abs(data)) if data.size > 0 else 0.0
    if max_abs > 0:
        data = data / float(max_abs)

    # mantiene la forma que devuelve soundfile: (n_samples,) o (n_samples, n_channels)
    return data, int(fs)


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
        raise TypeError("t60_por_banda debe ser un diccionario {f_central: T60_seg}")

    n_samples = int(np.ceil(duracion * fs))
    t = np.arange(n_samples) / float(fs)

    out = np.zeros(n_samples, dtype=np.float64)

    # si no se pasan bandas, usar las centradas en octave bands típicas
    if not t60_por_banda:
        centers = [31.5, 63.0, 125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0]
        # asignar un T60 por defecto si faltan
        t60_por_banda = {f: 1.0 for f in centers}

    # procesa cada banda: genera ruido, filtra, normaliza por RMS y aplica envolvente
    for f0, t60 in t60_por_banda.items():
        f0 = float(f0)
        t60 = float(t60)
        if f0 <= 0:
            raise ValueError(f"Frecuencia central inválida: {f0}")
        if t60 <= 0:
            raise ValueError(f"T60 inválido para banda {f0} Hz: {t60}")

        # generar ruido blanco
        noise = np.random.normal(scale=1.0, size=n_samples).astype(np.float64)

        # diseño de filtro pasa-banda (ancho aproximado de banda de octava)
        low = f0 / np.sqrt(2.0)
        high = f0 * np.sqrt(2.0)

        nyq = fs / 2.0
        if high >= nyq:
            high = nyq * 0.999
        if low <= 0:
            low = 1.0

        wp = [low / nyq, high / nyq]
        sos = butter(N=4, Wn=wp, btype="band", output="sos")

        # filtrado cero-fase con sosfiltfilt; fallback a sosfilt si falla
        try:
            filtered = sosfiltfilt(sos, noise)
        except Exception:
            try:
                # aplicar forward+backward manualmente con sosfilt
                forward = sosfilt(sos, noise)
                filtered = forward[::-1].copy()
                filtered = sosfilt(sos, filtered)[::-1]
            except Exception:
                # último recurso: usar filtfilt con coeficientes b,a
                b, a = butter(N=4, Wn=wp, btype="band")
                try:
                    filtered = filtfilt(b, a, noise)
                except Exception:
                    filtered = noise

        # normalizar cada banda por su RMS antes de aplicar la envolvente
        rms = np.sqrt(np.mean(filtered**2))
        if rms > 0:
            filtered = filtered / float(rms)

        # envolvente exponencial a partir de T60: exp(-alpha * t)
        alpha = np.log(1000.0) / t60  # ln(1000) para -60 dB en T60
        envelope = np.exp(-alpha * t)

        band = filtered * envelope
        out += band

    # normalizar respecto al pico
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
