"""Servicio de calculo de parametros acusticos segun ISO 3382.

Milestone 3: Analisis de parametros acusticos.
"""

import numpy as np
from scipy.signal import hilbert

from app.services.filter import filtro_octava

BANDAS_VALIDACION_IEC61260: list[float] = [125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0]

# tramo (dB inicio, dB fin) sobre la curva de Schroeder para cada parametro de TR
_TRAMOS_TR = {
    "EDT": (0.0, -10.0),
    "T10": (-5.0, -15.0),
    "T20": (-5.0, -25.0),
    "T30": (-5.0, -35.0),
}


def suavizar_signal(signal: np.ndarray, ventana: int | str = "hilbert") -> np.ndarray:
    """
    Suaviza una senal para reducir fluctuaciones del ruido.

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (array 1D).
    ventana : int
        Tamano de la ventana de suavizado en muestras.

    Returns
    -------
    np.ndarray
        Senal suavizada (envolvente de energia).
    """
    signal = np.asarray(signal, dtype=float)

    if isinstance(ventana, str):
        if ventana != "hilbert":
            raise ValueError(
                f"Valor de 'ventana' no reconocido: {ventana!r}. Debe ser 'hilbert' o un entero."
            )
        analitica = hilbert(signal)
        return np.abs(analitica)  # type: ignore

    if isinstance(ventana, int):
        if ventana < 1:
            raise ValueError("El tamano de ventana debe ser un entero positivo.")

        energia = signal**2
        kernel = np.ones(ventana) / ventana
        # 'same' preserva la longitud de la senal de entrada
        return np.convolve(energia, kernel, mode="same")

    raise TypeError(f"'ventana' debe ser int o str, no {type(ventana).__name__}.")


def integral_schroeder(ri: np.ndarray) -> np.ndarray:
    """
    Calcula la integral de Schroeder (integracion inversa).

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (o RI filtrada por banda).

    Returns
    -------
    np.ndarray
        Curva de decaimiento de Schroeder en dB, normalizada a 0 dB.
    """
    ri = np.asarray(ri, dtype=float)

    if ri.size == 0:
        raise ValueError("La RI no puede estar vacia.")

    eps = np.finfo(float).eps

    energia = ri**2
    integral_inversa = np.cumsum(energia[::-1])[::-1]

    # normalizacion respecto a la energia total
    curva_db = 10 * np.log10(integral_inversa / integral_inversa[0] + eps)

    return curva_db


def regresion_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Calcula la regresion lineal por minimos cuadrados.

    Parameters
    ----------
    x : np.ndarray
        Variable independiente (tipicamente tiempo en segundos).
    y : np.ndarray
        Variable dependiente (tipicamente curva de Schroeder en dB).

    Returns
    -------
    tuple[float, float, float]
        (pendiente, ordenada_al_origen, r_cuadrado)
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.shape != y.shape:
        raise ValueError("x e y deben tener la misma longitud.")
    if x.size < 2:
        raise ValueError("Se requieren al menos 2 puntos para la regresion.")

    n = x.size
    suma_x = np.sum(x)
    suma_y = np.sum(y)
    suma_xy = np.sum(x * y)
    suma_x2 = np.sum(x**2)

    denominador = n * suma_x2 - suma_x**2
    if denominador == 0:
        raise ValueError("No se puede ajustar: los valores de x son constantes.")

    pendiente = (n * suma_xy - suma_x * suma_y) / denominador
    ordenada = (suma_y - pendiente * suma_x) / n

    y_pred = pendiente * x + ordenada  # y_pred es la recta ajustada a
    # los puntos de la curva de Schroeder
    ss_res = np.sum((y - y_pred) ** 2)  # ss_res es la suma de los residuos al cuadrado
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # ss_tot es la suma de las diferencias al cuadrado
    # respecto a la media

    # y es constante: si el ajuste es exacto, r^2 = 1; si no, 0
    r2 = (1.0 if ss_res < 1e-12 else 0.0) if ss_tot == 0 else 1 - ss_res / ss_tot

    return float(pendiente), float(ordenada), float(r2)


# se definen funciones de TR, C80 y D50 para utilizar en calcular_parametros_acusticos


def _tiempo_reverberacion(
    t: np.ndarray, curva_db: np.ndarray, db_inicio: float, db_fin: float
) -> tuple[float, float]:
    """Ajusta una recta sobre [db_inicio, db_fin] y extrapola a -60 dB.

    Returns
    -------
    tuple[float, float]
        (tiempo_reverberacion, r_cuadrado)
    """
    mask = (curva_db <= db_inicio) & (curva_db >= db_fin)

    if np.sum(mask) < 2:
        raise ValueError(
            f"No hay suficientes puntos en el tramo [{db_inicio}, {db_fin}] dB "
            "para ajustar la regresion"
        )

    pendiente, _, r2 = regresion_lineal(t[mask], curva_db[mask])

    if pendiente >= 0:
        raise ValueError(
            "La pendiente estimada no es negativa; la curva de Schroeder "
            "no decae en el tramo solicitado."
        )

    return -60.0 / pendiente, r2


def _definicion_d50(ri_filtrada: np.ndarray, fs: int) -> float:
    """Calcula D50: porcentaje de energia en los primeros 50 ms."""
    energia = ri_filtrada**2
    n50 = int(0.050 * fs)
    n50 = min(n50, len(energia))

    energia_total = np.sum(energia)
    if energia_total <= 0:
        return 0.0

    return float(np.sum(energia[:n50]) / energia_total * 100.0)


def _claridad_c80(ri_filtrada: np.ndarray, fs: int) -> float:
    """Calcula C80: relacion en dB entre energia temprana y tardia (80 ms)."""
    energia = ri_filtrada**2
    n80 = int(0.080 * fs)
    n80 = min(n80, len(energia))

    energia_temprana = np.sum(energia[:n80])
    energia_tardia = np.sum(energia[n80:])

    eps = np.finfo(float).eps
    return float(10 * np.log10((energia_temprana + eps) / (energia_tardia + eps)))


def calcular_parametros_acusticos(
    ri: np.ndarray,
    fs: int,
    bandas: list[float] | None = None,
    orden_filtro: int = 8,
    sin_filtrar: bool = False,
) -> dict[str, dict[float, float]]:
    """
    Calcula los parametros acusticos ISO 3382, por banda de octava o en banda ancha.

    Implementa el pipeline suavizado -> integral de Schroeder -> regresion lineal
    para cada banda solicitada (o para la señal completa si sin_filtrar=True),
    extrapolando a -60 dB para obtener EDT, T10, T20 y T30. Reporta T60
    (T30 o T20 segun el ajuste de r^2), y los parametros D50 y C80.

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso a analizar (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.
    bandas : list[float], optional
        Frecuencias centrales de las bandas de octava a analizar (Hz).
        Si es None, se usan las bandas de la tabla de validacion IEC 61260
        (BANDAS_VALIDACION_IEC61260: 125 Hz a 4 kHz). Se ignora por completo
        si sin_filtrar=True.
    orden_filtro : int, optional
        Orden del filtro Butterworth de banda usado por filtro_octava
        (default 8). Sin efecto si sin_filtrar=True.
    sin_filtrar : bool, optional
        Si True, calcula sobre la RI completa sin filtrar. Los resultados quedan
        bajo la clave de banda 0.0 (banda ancha, no hay frecuencia central real).

    Returns
    -------
    dict[str, dict[float, float]]
        Diccionario {parametro: {frecuencia_central: valor}}, donde parametro
        es una de: 'EDT', 'T10', 'T20', 'T30', 'T60', 'D50', 'C80'. Si
        sin_filtrar=True, la unica clave de frecuencia presente es 0.0.

    Raises
    ------
    ValueError
        Si algun tramo de la curva de Schroeder no tiene suficientes puntos
        para ajustar la regresion (_tiempo_reverberacion), o si fc/fs
        son invalidos para filtro_octava.
    """
    claves = (*_TRAMOS_TR.keys(), "T60", "D50", "C80")
    resultado: dict[str, dict[float, float]] = {clave: {} for clave in claves}

    bandas_a_iterar = [0.0] if sin_filtrar else (bandas or BANDAS_VALIDACION_IEC61260)

    for fc in bandas_a_iterar:
        ri_filtrada = ri if sin_filtrar else filtro_octava(ri, fc=fc, fs=fs, orden=orden_filtro)
        curva_db = integral_schroeder(ri_filtrada)
        t = np.arange(len(curva_db)) / fs

        r2_por_tramo: dict[str, float] = {}
        for parametro, (db_inicio, db_fin) in _TRAMOS_TR.items():
            valor, r2 = _tiempo_reverberacion(t, curva_db, db_inicio, db_fin)
            resultado[parametro][fc] = valor
            r2_por_tramo[parametro] = r2

        if r2_por_tramo["T30"] >= 0.95:
            resultado["T60"][fc] = resultado["T30"][fc]
        else:
            resultado["T60"][fc] = resultado["T20"][fc]

        resultado["D50"][fc] = _definicion_d50(ri_filtrada, fs)
        resultado["C80"][fc] = _claridad_c80(ri_filtrada, fs)

    return resultado


# se define una funcion que estima SNR


def estimar_ruido_de_fondo(ri: np.ndarray, fraccion_cola: float = 0.1) -> tuple[float, float]:
    """
    Estima el nivel de ruido de fondo y el SNR de una RI.

    Nota: esta es una estimacion simplificada (promedio de energia en la cola
    de la señal), da un valor aproximado de piso de ruido y SNR para fines informativos
    (no es Lundeby)

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (banda ancha o filtrada).
    fraccion_cola : float, optional
        Fraccion final de la señal considerada "solo ruido" (default 10%).

    Returns
    -------
    tuple[float, float]
        (nivel_de_ruido_estimado, snr_estimado_db)
    """
    ri = np.asarray(ri, dtype=float)
    energia = ri**2
    n = len(energia)
    n_cola = max(int(n * fraccion_cola), 1)

    eps = np.finfo(float).eps
    energia_ruido = float(np.mean(energia[-n_cola:]))
    energia_pico = float(np.max(energia))

    snr_db = 10 * np.log10((energia_pico + eps) / (energia_ruido + eps))

    return energia_ruido, snr_db
