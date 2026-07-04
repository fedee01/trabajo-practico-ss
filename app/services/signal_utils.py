"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import os

import numpy as np


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
<<<<<<< HEAD
    # si no es un string, no tiene sentido intentar cargar un archivo, lanzo un error de tipo

=======
>>>>>>> dev
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    ext = os.path.splitext(ruta)[1].lower()

    if ext not in (".wav", ".flac"):
        raise ValueError(f"Formato '{ext}' no soportado. Sólo se aceptan archivos WAV o FLAC.")

    try:
        signal, fs = sf.read(ruta, dtype="float64")

    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo: {e}") from e

    signal = np.asarray(signal, dtype=np.float64)

    if signal.ndim == 2:
<<<<<<< HEAD
        n_channels = signal.shape[1]  # [1] es el numero de canales, [0] es el numero de muestras
=======
        n_channels = signal.shape[1]
>>>>>>> dev

        if n_channels not in (1, 2):
            raise ValueError(f"Número de canales inválido: {n_channels}. Debe ser mono o estéreo.")

<<<<<<< HEAD
        signal = signal.mean(axis=1)  # si es estéreo, promedia ambos canales para obtener mono
=======
        signal = signal.mean(axis=1)
>>>>>>> dev

    elif signal.ndim != 1:
        raise ValueError("Formato de audio inválido.")

    if signal.size == 0:
        raise ValueError("El archivo de audio está vacío.")

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
    raise NotImplementedError("Implementar en Milestone 2")

<<<<<<< HEAD
    # validaciones
=======
>>>>>>> dev
    if not isinstance(t60_por_banda, dict):
        raise TypeError("t60_por_banda debe ser un diccionario {fc:T60}")

    if len(t60_por_banda) == 0:
        raise ValueError("t60_por_banda no puede estar vacío")

    if fs <= 0:
        raise ValueError("fs debe ser positivo")

    n_samples = int(np.ceil(duracion * fs))
    t = np.arange(n_samples, dtype=np.float64) / fs
    ri_sintetizada = np.zeros(n_samples, dtype=np.float64)
    nyq = fs / 2

    for fc, t60 in t60_por_banda.items():
<<<<<<< HEAD
        fc = float(fc)  # fc es la frecuencia central de la banda
=======
        fc = float(fc)
>>>>>>> dev
        t60 = float(t60)

        if fc <= 0:
            raise ValueError(f"Frecuencia inválida: {fc}")

        if t60 <= 0:
            raise ValueError(f"T60 inválido: {t60}")

<<<<<<< HEAD
        # ruido blanco
=======
>>>>>>> dev
        noise = np.random.normal(loc=0.0, scale=1.0, size=n_samples)

        f_inf = fc / np.sqrt(2)
        f_sup = fc * np.sqrt(2)

        if f_sup >= nyq:
            f_sup = nyq * 0.999

        if f_inf >= f_sup:
            raise ValueError(f"Banda inválida para fc={fc}")

        w = [f_inf / nyq, f_sup / nyq]

<<<<<<< HEAD
        sos = butter(N=4, Wn=w, btype="bandpass", output="sos")

        filtrado = sosfiltfilt(sos, noise)

        # normalización RMS
=======
        sos = butter( N=4, Wn=w, btype="bandpass", output="sos")

        filtrado = sosfiltfilt(sos, noise)

>>>>>>> dev
        rms = np.sqrt(np.mean(filtrado**2))
        if rms > 0:
            filtrado /= rms

<<<<<<< HEAD
        # envolvente
        alfa = np.log(1000.0) / t60
        envolv = np.exp(-alfa * t)
        banda = filtrado * envolv

        ri_sintetizada += banda  # la sumatoria de todas las bandas

    # normalizado
=======
        alfa = np.log(1000.0) / t60

        envolv = np.exp(-alfa * t)
        banda = filtrado * envolv
        ri_sintetizada += banda

>>>>>>> dev
    max_abs = np.max(np.abs(ri_sintetizada))
    if max_abs > 0:
        ri_sintetizada /= max_abs

    return ri_sintetizada


def obtener_ri_desde_sweep(grabacion: np.ndarray, filtro_inverso: np.ndarray) -> np.ndarray:
    """
    Obtiene la respuesta al impulso (RI) mediante la deconvolución de una grabación realizada con
    un sine sweep.

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
    if not isinstance(grabacion, np.ndarray):
        raise TypeError("grabacion debe ser un array numpy")

    if not isinstance(filtro_inverso, np.ndarray):
        raise TypeError("filtro_inverso debe ser un array numpy")

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

    grabacion = np.asarray(grabacion, dtype=np.float64)
    filtro_inverso = np.asarray(filtro_inverso, dtype=np.float64)

    if grabacion.size == 0:
        raise ValueError("grabacion vacía")
    if filtro_inverso.size == 0:
        raise ValueError("filtro_inverso vacío")

<<<<<<< HEAD
    # deconvolución con FFT
=======
>>>>>>> dev
    ri_full = fftconvolve(grabacion, filtro_inverso, mode="full")

    peak_idx = np.argmax(np.abs(ri_full))
<<<<<<< HEAD
    ri = ri_full[peak_idx:]

    # normalizado
=======
    ri= ri_full[peak_idx:]
>>>>>>> dev
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
    if not isinstance(signal, np.ndarray):
        raise TypeError("signal debe ser un np.ndarray")

<<<<<<< HEAD
    # convierte a mono si es multicanal
    sig = signal.mean(axis=1) if signal.ndim > 1 else signal
=======
    if signal.size == 0:
        raise ValueError("signal no puede estar vacía")

    if signal.ndim > 1:
        signal = signal.mean(axis=1)
>>>>>>> dev

    safe = np.where(signal == 0, np.finfo(float).eps, np.abs(signal))

    db = 20 * np.log10(safe / np.max(safe))

    db = np.maximum(db, -120.0)

    return db
