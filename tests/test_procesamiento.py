"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
import soundfile as sf

from app.services.signal_utils import a_escala_log, cargar_audio


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
            abs=1e-12, )

