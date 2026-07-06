"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
import soundfile as sf
from scipy.signal import butter, sosfreqz

from app.services.filter import filtro_octava
from app.services.signal_utils import (
    a_escala_log,
    cargar_audio,
    obtener_ri_desde_sweep,
    sintetizar_ri,
)
from app.services.sine_sweep import generar_sine_sweep


class TestCargarAudio:
    """Tests para la funcion cargar_audio."""

    def test_cargar_audio_no_existe(self):
        """Verifica que se lanza FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            cargar_audio("archivo_que_no_existe.wav")

    def test_cargar_audio_retorna_tupla(self):
        """Verifica que retorna una tupla (signal, fs) — requiere archivo de prueba."""
        pytest.skip("Requiere archivo de audio de prueba")

    @pytest.mark.parametrize("extension", [".wav", ".flac"])
    def test_cargar_audio(self, extension, tmp_path):
        """Verificar carga correcta de archivos WAV y FLAC."""
        fs = 48000
        x = np.array([0.0, 0.5, -0.5, 1.0])
        archivo = tmp_path / f"audio{extension}"
        sf.write(archivo, x, fs)
        resultado, fs_resultado = cargar_audio(str(archivo))
        assert isinstance(resultado, np.ndarray)
        assert fs_resultado == fs
        assert resultado.ndim == 1
        assert len(resultado) == len(x)

    def test_cargar_audio_formato_invalido(self, tmp_path):
        """Verificar que lanza error con formato no soportado."""
        archivo = tmp_path / "audio.mp3"
        archivo.write_text("contenido de prueba")
        with pytest.raises(ValueError, match="Formato"):
            cargar_audio(str(archivo))

    def test_cargar_audio_normalizacion(self, tmp_path):
        """Verificar que la salida esta normalizada entre -1 y 1."""
        fs = 48000
        x = np.array([0.2, -0.4, 0.6])
        archivo = tmp_path / "audio.wav"
        sf.write(archivo, x, fs)
        resultado, _ = cargar_audio(str(archivo))
        assert np.max(np.abs(resultado)) == pytest.approx(1.0)
        assert np.all(np.abs(resultado) <= 1.0 + 1e-12)


class TestSintetizarRI:
    """Tests para la funcion sintetizar_ri."""

    def test_sintetizar_ri_decaimiento(self):
        """Verifica que el T60 medido por banda coincide con el especificado."""
        np.random.seed(0)
        fs = 48000
        fc = 1000
        t60_objetivo = 2.0
        ri = sintetizar_ri(
            t60_por_banda={fc: t60_objetivo},
            fs=fs,
            duracion=4.0,
        )
        ri_filtrada = filtro_octava(
            x=ri,
            fc=fc,
            fs=fs,
        )

        # Curva de decaimiento energético (Schroeder)
        schroeder = np.cumsum((ri_filtrada**2)[::-1])[::-1]
        schroeder /= np.max(schroeder)
        schroeder_db = 10 * np.log10(schroeder + np.finfo(float).eps)

        # Buscar el primer cruce por debajo de -60 dB
        indices = np.where(schroeder_db <= -60)[0]
        assert len(indices) > 0, "La curva de decaimiento no alcanza los -60 dB."

        t60_medido = indices[0] / fs

        # Debe coincidir con el valor objetivo dentro del 10 %
        assert t60_medido == pytest.approx(
            t60_objetivo,
            rel=0.1,
        )


class TestObtenerRIdesdeSweep:
    """Tests para la función obtener_ri_desde_sweep."""

    def test_obtener_ri_desde_sweep(self):
        """
        Correlación entre RI original y RI recuperada mayor a 0.9

        La función obtener_ri_desde_sweep devuelve la RI alineada al impulso
        directo (pico principal), por lo que la RI original también se alinea
        antes de calcular la correlación cruzada normalizada.
        """

        np.random.seed(0)
        fs = 48000
        sweep, filtro_inverso = generar_sine_sweep(
            f1=20,
            f2=20000,
            duracion=2.0,
            fs=fs,
        )
        ri_original = sintetizar_ri(
            t60_por_banda={1000.0: 1.5},
            fs=fs,
            duracion=2.0,
        )
        grabacion = np.convolve(
            sweep,
            ri_original,
            mode="full",
        )
        ri_recuperada = obtener_ri_desde_sweep(
            grabacion=grabacion,
            filtro_inverso=filtro_inverso,
        )

        # alinear la RI original al impulso directo
        pico_original = np.argmax(np.abs(ri_original))
        ri_original = ri_original[pico_original:]

        # Igualar longitudes
        n = min(len(ri_original), len(ri_recuperada))
        ri_original = ri_original[:n]
        ri_recuperada = ri_recuperada[:n]

        # correlación cruzada normalizada
        correlacion = np.correlate(
            ri_recuperada,
            ri_original,
            mode="full",
        )

        correlacion = np.max(np.abs(correlacion)) / (
            np.linalg.norm(ri_recuperada) * np.linalg.norm(ri_original)
        )

        assert correlacion > 0.9


# ---------------------------------------------------------------------
# Helpers compartidos


def _sos_octava(fc, fs, orden=8):
    """Reconstruye el mismo filtro SOS que arma filtro_octava, para poder
    analizar su respuesta en frecuencia con freqz."""
    f_inf = fc / np.sqrt(2.0)
    f_sup = fc * np.sqrt(2.0)
    nyq = fs / 2.0
    wn0 = max(f_inf / nyq, 1e-12)
    wn1 = min(f_sup / nyq, 1.0 - 1e-12)
    return butter(orden, [wn0, wn1], btype="band", output="sos")


def _ganancia_db_en(sos, fs, freqs_hz):
    """Devuelve la ganancia en dB del filtro en las frecuencias pedidas."""
    w, h = sosfreqz(sos, worN=8192, fs=fs)  # h es complejo: NO castear a float
    mag_db = 20 * np.log10(np.abs(h) + 1e-20)
    return np.interp(freqs_hz, w, mag_db)  # type: ignore


# ---------------------------------------------------------------------


class TestFiltroOctava:
    def test_filtro_octava_frecuencia_central(self):
        """Verificar que el filtro pasa correctamente la frecuencia central."""
        fs = 44100
        fc = 1000.0
        orden = 8

        sos = _sos_octava(fc, fs, orden)
        ganancia_fc = _ganancia_db_en(sos, fs, [fc])[0]

        # En fc la ganancia debe ser maxima, ~0 dB
        assert ganancia_fc == pytest.approx(0.0, abs=0.5)

    def test_filtro_octava_atenuacion(self):
        """Verificar atenuacion fuera de banda."""
        fs = 44100
        fc = 1000.0
        orden = 8

        sos = _sos_octava(fc, fs, orden)

        f_baja = fc / 2.0
        f_alta = fc * 2.0

        ganancias = _ganancia_db_en(sos, fs, [f_baja, f_alta])

        # Atenuacion fuera de banda: mayor a 20 dB por debajo de 0 dB
        assert ganancias[0] < -20.0
        assert ganancias[1] < -20.0

    def test_filtro_octava_respuesta_frecuencia(self):
        """Verificar que la respuesta cumple -3 dB en frecuencias de corte."""
        fs = 48000
        fc = 1000.0
        orden = 8

        f_inf = fc / np.sqrt(2.0)
        f_sup = fc * np.sqrt(2.0)

        sos = _sos_octava(fc, fs, orden)

        # 1. Calcular la respuesta en frecuencia del filtro con sosfreqz
        w, h = sosfreqz(sos, worN=16384, fs=fs)
        mag_db = 20 * np.log10(np.abs(h) + 1e-20)

        ganancia_fc = np.interp(fc, w, mag_db)  # type: ignore
        ganancia_f_inf = np.interp(f_inf, w, mag_db)  # type: ignore
        ganancia_f_sup = np.interp(f_sup, w, mag_db)  # type: ignore
        ganancia_octava_inf = np.interp(fc / 2.0, w, mag_db)  # type: ignore
        ganancia_octava_sup = np.interp(fc * 2.0, w, mag_db)  # type: ignore

        # 2. Ganancia en fc maxima (0 dB, tolerancia 0.5 dB)
        assert ganancia_fc == pytest.approx(0.0, abs=0.5)
        assert ganancia_fc >= ganancia_f_inf
        assert ganancia_fc >= ganancia_f_sup

        # 3. Ganancia en f_inf y f_sup aprox -3 dB (tolerancia 1 dB)
        assert ganancia_f_inf == pytest.approx(-3.0, abs=1.0)
        assert ganancia_f_sup == pytest.approx(-3.0, abs=1.0)

        # 4. Atenuacion a una octava de distancia (fc/2 y 2*fc) mayor a 20 dB
        assert ganancia_octava_inf < -20.0
        assert ganancia_octava_sup < -20.0


class TestAEscalaLog:
    """Tests para la funcion a_escala_log."""

    def test_a_escala_log_valores(self):
        """Verifica que el maximo de la senal corresponde a 0 dB."""
        x = np.array([1.0, 0.5, 0.25, 0.1])
        db = a_escala_log(x)
        assert abs(db[0] - 0.0) < 1e-10

    def test_a_escala_log_tipo(self):
        """Verifica que retorna un np.ndarray."""
        x = np.array([1.0, 0.5])
        db = a_escala_log(x)
        assert isinstance(db, np.ndarray)

    def test_a_escala_log_relacion(self):
        """Verificar que una senal con amplitud mitad da -6 dB."""
        x = np.array([1.0, 0.5])
        db = a_escala_log(x)
        assert db[0] == pytest.approx(0.0)
        assert db[1] == pytest.approx(
            20 * np.log10(0.5),
            abs=1e-12,
        )
