def obtener_ri_desde_sweep(grabacion: np.ndarray, filtro_inverso: np.ndarray) -> np.ndarray:
    """
    Obtiene la respuesta al impulso (RI) mediante la deconvolución de una grabación realizada con
    un sine sweep.

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

    # deconvolución con FFT
    ri_full = fftconvolve(grabacion, filtro_inverso, mode="full")

    # ubica el pico principal
    peak_idx = np.argmax(np.abs(ri_full))
    ri = ri_full[peak_idx:]

    # normalizado
    max_abs = np.max(np.abs(ri))
    if max_abs > 0:
        ri /= max_abs

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
    sig = signal.mean(axis=1) if signal.ndim > 1 else signal

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
