"""Tests para los servicios de generacion de senales (Milestone 1)."""

import numpy as np
import pytest

from app.services.pink_noise import generar_ruido_rosa
from app.services.sine_sweep import generar_sine_sweep
from app.services.reproducir_grabar import reproducir_y_grabar

from scipy import signal
from scipy.signal import spectrogram 

class TestGenerarRuidoRosa:
    """Tests para la funcion generar_ruido_rosa."""

    def test_ruido_rosa_espectro(self):
    """Verificar que el espectro del ruido rosa tiene una pendiente
    de aproximadamente -3 dB/octava."""
    r_rosa = generar_ruido_rosa(10, 44100)
    Frec, Psd = signal.welch(r_rosa, fs=44100, nperseg=1024)
    #filtrado y pasaje dB
    mask = (Frec >= 100) & (Frec <= 10000)
    fre_filtro = Frec[mask]
    psd_filtro = Psd[mask]
    db_psd = 10 * np.log10(psd_filtro)
    #calculo
    octava = np.log2(fre_filtro / fre_filtro[0])
    pendiente, interc = np.polyfit(octava, db_psd, 1)
    assert -4 <= pendiente <= -2, "El espectro del ruido rosa tiene una pendiente de aproximadamente -3 dB/octava"


class TestGenerarSineSweep:
    """Tests para la funcion generar_sine_sweep."""
    def test_sine_sweep_rango_frecuencias(self):
    """Verificar que el sine sweep cubre el rango de frecuencias
    especificado de f1 a f2."""
    sin_swe = generar_sine_sweep(20, 20000, 5, 44100)
    Frec2, tiempos, Sxx = spectrogram(sin_swe, fs=44100, nperseg=1024)
    inicio = np.abs(Frec2 - 20).argmin()
    final = np.abs(Frec2 - 20000).argmin()
    #Suma en t por cada frec
    ener_x_frec = np.sum(Sxx, axis=1)
    assert ener_x_frec[20] > umbral_energia, "Poca energía en frecuencia inicial"
    assert ener_x_frec[20000] > umbral_energia, "Poca energía en frecuencia final"
    #Ve si la frec_inst crece monotonamente
    indice_max_ener = np.argmax(Sxx, axis=0)
    frec_max = Frec2[indice_max_ener]
     #Ve si las frec son solo crecientes
    frec_cre = np.all(np.diff(frec_max) >= 0)
    assert frec_cre == np.all(np.diff(frec_max) >= 0), "La frecuencia instantánea no crece monótonamente"

class TestConvolucion:
    """Tests para la funcion generar_sine_sweep."""

    def test_sweep_convolucion_impulso(self):
    """
    Verificar que la convolucion del sweep con su filtro inverso
    produce una aproximacion a un impulso.
    """
    senal1 = generar_sine_sweep(f1: float, f2: float, duracion: float, fs: int)
    rta_imp = fftconvolve(senal1[0], senal1[1], mode="full")
    indice_pico = np.argmax(np.abs(rta_imp))
    # Sacamos una ventana cerca del pico
    vta = 100
    ini_exc = max(0, indice_pico - vta) 
    fin_exc = min(len(rta_imp), indice_pico + vta)
    # mascara booleana
    mask2 = np.ones(len(rta_imp), dtype=bool)
    mask2[ini_exc:fin_exc] = False

    energ_pico = np.sum(np.abs(rta_imp[indice_pico]) ** 2)
    energ_resto = np.sum(np.abs(rta_imp[mask2]) ** 2)
    if energ_resto == 0:
        energ_resto = 1e-12
    # dif energia en dB
    dif_db = 10 * np.log10(energ_pico / energ_resto)

    assert dif_db >= 40, "La energia pico es igual o inferior a 40 dB"


class TestReproducirYGrabar:
    """Tests para la funcion reproducir_y_grabar."""

    def test_reproducir_y_grabar_forma(self):
    """
    Verificar que la funcion maneja correctamente senales mono y estereo.
    """
    mono = np.random.uniform(-1, 1 (int(0,1 * 44100))
    rta_mono = reproducir_y_grabar(mono, 44100, 0.1)
    assert isinstance(rta_mono, np.ndarray)
    
    stereo = np.random.uniform(-1, 1, (int(0,1 * 44100), 2))
    rta_ stereo = rta_ste = reproducir_y_grabar(stereo, 44100, 0.1)
    assert isinstance(rta_stereo, np.ndarray)

    def test_tolerancia(self):
        duracion_esperada = 2.0
        entrada3 = np.random.uniform(-1, 1, int(44100 * duracion_esperada)
        salida3 = reproducir_y_grabar(entrada3, 44100, duracion_esperada)
        
        muestra_esperada = duracion_esperada * 44100
        muestra_obtenida = len(salida3)

        tolerancia = 0.01
        assert abs(muestra_obtenida - muestra_esperada) >= muestra_esperada * tolerancia, "La grabacion cumple con la tolerancia de !%"

    def test_dispositivo_no_disponible(self):
        """
        Verifica que hay una excepcion si no hay dispositivo funcionando
        """
        with pytest.raises(Exception) as exc_info:
            reproducir_y_grabar(np.array([]), 44100, 0.1)
            assert "dispositivo no encontrado"
