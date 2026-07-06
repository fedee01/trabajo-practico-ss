"""Tests para los servicios de generacion de senales (Milestone 1)."""

import numpy as np
import pytest
import sounddevice as sd
from scipy.signal import fftconvolve, welch

from app.services.pink_noise import generar_ruido_rosa
from app.services.reproducir_grabar import reproducir_y_grabar
from app.services.sine_sweep import generar_sine_sweep


class TestGenerarRuidoRosa:
    """Tests para la funcion generar_ruido_rosa."""

    def test_ruido_rosa_duracion(self):
        """Verifica que la longitud de la senal corresponda a duracion * fs."""
        duracion = 2.0
        fs = 44100
        ruido = generar_ruido_rosa(duracion, fs)
        expected_length = int(duracion * fs)
        assert len(ruido) == expected_length

    def test_ruido_rosa_tipo(self):
        """Verifica que la funcion retorna un np.ndarray."""
        ruido = generar_ruido_rosa(1.0, 44100)
        assert isinstance(ruido, np.ndarray)

    def test_ruido_rosa_normalizado(self):
        """Verifica que la senal esta normalizada entre -1 y 1."""
        ruido = generar_ruido_rosa(1.0, 44100)
        assert np.max(np.abs(ruido)) <= 1.0

    def test_ruido_rosa_espectro(self):
        np.random.seed(0)
        ruido = generar_ruido_rosa(10, 44100)
        frecuencias, psd = welch(ruido, fs=44100, nperseg=8192)
        mascara = (frecuencias >= 100) & (frecuencias <= 10000)
        psd_db = 10 * np.log10(psd[mascara])
        octavas = np.log2(frecuencias[mascara])
        pendiente, _ = np.polyfit(octavas, psd_db, 1)
        assert -4 <= pendiente <= -2


class TestGenerarSineSweep:
    """Tests para la funcion generar_sine_sweep."""

    def test_sine_sweep_retorna_tupla(self):
        """Verifica que retorna una tupla con dos arrays."""
        resultado = generar_sine_sweep(20, 20000, 1.0, 44100)
        assert isinstance(resultado, tuple)
        assert len(resultado) == 2
        assert isinstance(resultado[0], np.ndarray)
        assert isinstance(resultado[1], np.ndarray)

    def test_sine_sweep_duracion(self):
        """Verifica que ambas senales tienen la longitud correcta."""
        duracion = 3.0
        fs = 44100
        sweep, filtro_inv = generar_sine_sweep(20, 20000, duracion, fs)
        expected_length = int(duracion * fs)
        assert len(sweep) == expected_length
        assert len(filtro_inv) == expected_length

    def test_sweep_convolucion_impulso(self):
        """
        Verifica que la convolución del sweep con su filtro inverso
        produce una aproximación a un impulso.
        """
        sweep, filtro = generar_sine_sweep(f1=20, f2=20000, duracion=5, fs=48000)
        convolucion = fftconvolve(sweep, filtro, mode="full")
        pico_max = np.argmax(np.abs(convolucion))
        energia_pico = convolucion[pico_max] ** 2
        ventana = 100
        mascara = np.ones(len(convolucion), dtype=bool)
        inicio = max(0, pico_max - ventana)
        fin = min(len(convolucion), pico_max + ventana + 1)
        mascara[inicio:fin] = False
        energia_resto = np.mean(convolucion[mascara] ** 2)  # energía promedio del resto de senal
        relacion_db = 10 * np.log10(energia_pico / energia_resto)
        assert relacion_db >= 40


class TestReproducirYGrabar:
    """Tests para la funcion reproducir_y_grabar."""

    @pytest.mark.parametrize("channels", [1, 2])
    def test_reproducir_y_grabar_forma(self, monkeypatch, channels):
        """Verifica que la función acepta señales mono y estéreo."""

        fs = 48000
        duracion = 2.0

        # señal de 1 segundo
        shape = (fs,) if channels == 1 else (fs, channels)
        signal = np.random.randn(*shape)

        monkeypatch.setattr(
            sd,
            "check_input_settings",
            lambda **kwargs: None,
        )
        monkeypatch.setattr(
            sd,
            "check_output_settings",
            lambda **kwargs: None,
        )
        monkeypatch.setattr(
            sd,
            "playrec",
            lambda data, samplerate, channels, dtype: np.zeros(
                (data.shape[0], channels),
                dtype=np.float32,
            ),
        )
        monkeypatch.setattr(sd, "wait", lambda: None)

        recording = reproducir_y_grabar(
            signal,
            fs,
            duracion,
        )

        n_esperado = int(fs * duracion)
        assert recording.shape == (
            n_esperado,
            channels,
        )

    def test_reproducir_y_grabar_sin_dispositivo(self, monkeypatch):
        """Verifica que se informa correctamente cuando no hay dispositivo de audio."""
        fs = 48000
        duracion = 2.0
        signal = np.random.randn(fs)

        def error(**kwargs):
            raise Exception("No hay dispositivo disponible")

        monkeypatch.setattr(sd, "check_input_settings", error)

        with pytest.raises(RuntimeError, match="Problema con la configuración"):
            reproducir_y_grabar(signal, fs, duracion)

    def test_reproducir_y_grabar_senal_vacia(self):
        """Verifica que una señal vacía lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            reproducir_y_grabar(np.array([]), fs=48000, duracion_grabacion=2.0)

    def test_reproducir_y_grabar_duracion_insuficiente(self):
        """Verifica que una duración de grabación menor al playback lanza ValueError."""
        signal = np.random.randn(48000)  # 1 segundo
        with pytest.raises(ValueError, match="al menos"):
            reproducir_y_grabar(signal, fs=48000, duracion_grabacion=0.5)  # pre-roll+señal > 0.5s

    def test_reproducir_y_grabar_duracion_grabada_incorrecta(self, monkeypatch):
        """Verifica que una discrepancia > 1% en la duración grabada lanza RuntimeError."""
        fs = 48000
        signal = np.random.randn(fs)

        monkeypatch.setattr(sd, "check_input_settings", lambda **kwargs: None)
        monkeypatch.setattr(sd, "check_output_settings", lambda **kwargs: None)
        # simula que el dispositivo grabó de menos (5% menos de lo esperado)
        monkeypatch.setattr(
            sd,
            "playrec",
            lambda data, samplerate, channels, dtype: np.zeros(
                (int(data.shape[0] * 0.95), channels), dtype=np.float32
            ),
        )
        monkeypatch.setattr(sd, "wait", lambda: None)

        with pytest.raises(RuntimeError, match="Duración de grabación inesperada"):
            reproducir_y_grabar(signal, fs, duracion_grabacion=2.0)
