"""Tests para los endpoints de la API (Milestone 3)."""

import io

import numpy as np
import pytest
import soundfile as sf
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def wav_sintetico_valido() -> io.BytesIO:
    """WAV sintético válido en memoria, para tests de endpoints."""
    fs = 48000
    t = np.linspace(0, 1, fs, endpoint=False)
    señal = np.exp(-3 * t) * np.sin(2 * np.pi * 440 * t)  # decaimiento exponencial simple

    buffer = io.BytesIO()
    sf.write(buffer, señal, fs, format="WAV")
    buffer.seek(0)
    return buffer


class TestHealthEndpoint:
    """Tests para el endpoint /health."""

    def test_health_returns_200(self):
        """Verifica que /health responde con status 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self):
        """Verifica que el status es 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_includes_version(self):
        """Verifica que la respuesta incluye la version."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data

    def test_health_includes_timestamp(self):
        """Verifica que la respuesta incluye el timestamp."""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data


class TestSignalsEndpoints:
    def test_pink_noise_devuelve_wav(self):
        """POST /pink-noise debe devolver un WAV valido con la duracion pedida."""
        response = client.post("/api/v1/signals/pink-noise", json={"duracion": 1.0, "fs": 44100})

        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

        data, fs = sf.read(io.BytesIO(response.content))
        assert fs == 44100
        assert len(data) == 44100

    def test_sine_sweep_devuelve_wav_mono(self):
        """POST /sine-sweep debe devolver un WAV mono (solo la senal a reproducir)."""
        response = client.post(
            "/api/v1/signals/sine-sweep",
            json={"f1": 20, "f2": 20000, "duracion": 1.0, "fs": 44100},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

        data, fs = sf.read(io.BytesIO(response.content))
        assert fs == 44100
        assert data.ndim == 1  # mono, no estereo/zip

    def test_synthetic_ir_devuelve_wav(self):
        """POST /synthetic-ir debe devolver una RI sintetica como WAV."""
        response = client.post(
            "/api/v1/signals/synthetic-ir",
            json={"t60_por_banda": {"1000": 1.5}, "fs": 44100, "duracion": 3.0},
        )

        assert response.status_code == 200

        data, fs = sf.read(io.BytesIO(response.content))
        assert fs == 44100

    def test_pink_noise_duracion_invalida_da_422(self):
        """Una duracion negativa debe devolver 422 (validacion Pydantic), no 500."""
        response = client.post("/api/v1/signals/pink-noise", json={"duracion": -1.0, "fs": 44100})
        assert response.status_code == 422

    def test_sine_sweep_f2_menor_a_f1_da_422(self):
        """f2 <= f1 es un error de negocio (no de tipo/rango), debe dar 422 no 500."""
        response = client.post(
            "/api/v1/signals/sine-sweep",
            json={"f1": 20000, "f2": 20, "duracion": 1.0, "fs": 44100},
        )
        assert response.status_code == 422


class TestRootEndpoint:
    """Tests para el endpoint raiz /."""

    def test_root_returns_200(self):
        """Verifica que / responde con status 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_api_info(self):
        """Verifica que la raiz devuelve informacion de la API."""
        response = client.get("/")
        data = response.json()
        assert data["name"] == "RIR-API"
        assert "docs" in data


class TestAcousticsEndpoints:
    def test_parameters_endpoint_devuelve_parametros_validos(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/acoustics/parameters",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        body = response.json()
        assert set(body["parameters"].keys()) == {"T10", "T20", "T30", "EDT"}
        assert body["parameters"]["T30"] > 0

    def test_parameters_by_bands_devuelve_formato_esperado(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/acoustics/parameters/by-bands",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        body = response.json()

        assert set(body["parameters"].keys()) == {"T30", "T20", "T10", "EDT"}
        assert set(body["center_frequencies"]) == {125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0}
        assert body["band_results"]  # no vacío


class TestAnalysisEndpoints:
    def test_impulse_response_by_bands_devuelve_formato_esperado(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/analysis/impulse-response/by-bands",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        body = response.json()

        assert body["analysis_settings"]["lundeby_applied"] is False
        assert body["analysis_settings"]["cutoff_time"] is None
        assert body["noise_analysis"]["estimated_snr_db"] > 0
        assert set(body["parameters"].keys()) == {"T30", "T20", "T10", "EDT"}

    def test_impulse_response_devuelve_formato_esperado(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/analysis/impulse-response",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        body = response.json()

        assert "bandwidth" not in body["analysis_settings"]
        assert body["analysis_settings"]["lundeby_applied"] is False
        assert set(body["parameters"].keys()) == {"T10", "T20", "T30", "EDT"}
        assert body["noise_analysis"]["estimated_snr_db"] > 0


class TestUtilsNpyEndpoints:
    def test_schroeder_devuelve_npy_valido(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/utils/schroeder",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/octet-stream"

        array = np.load(io.BytesIO(response.content))
        assert array[0] == pytest.approx(0.0, abs=1e-9)  # primer valor ~0 dB (tolerancia de float)
        assert response.headers["x-lundeby-applied"] == "false"

    def test_log_scale_devuelve_npy_valido(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/utils/log-scale",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        array = np.load(io.BytesIO(response.content))
        # comparación con tolerancia: evita sorpresas de redondeo de punto flotante
        assert np.max(array) == pytest.approx(0.0, abs=1e-9)  # normalizado a 0 dB


class TestUtilsSmoothingEndpoint:
    def test_smoothing_hilbert_devuelve_wav(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/utils/smoothing",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"
        assert response.headers["x-method"] == "hilbert"

    def test_smoothing_moving_average_sin_window_ms_da_422(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/utils/smoothing?method=moving_average",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 422


class TestFiltersEndpoints:
    def test_band_devuelve_zip_con_headers(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/filters/band",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert "x-center-frequencies" in response.headers

    def test_single_band_devuelve_wav(self, wav_sintetico_valido):
        response = client.post(
            "/api/v1/filters/single-band?center_freq=1000",
            files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

    def test_frequencies_devuelve_lista(self):
        response = client.get("/api/v1/filters/frequencies")
        assert response.status_code == 200
        body = response.json()
        assert body["num_bands"] == len(body["frequencies"])


def test_health_endpoint():
    """Verificar que /health responde correctamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analysis_endpoint(wav_sintetico_valido):
    """Enviar un archivo WAV a /api/v1/analysis/impulse-response y verificar respuesta."""
    response = client.post(
        "/api/v1/analysis/impulse-response",
        files={"file": ("test.wav", wav_sintetico_valido, "audio/wav")},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body["parameters"].keys()) == {"T10", "T20", "T30", "EDT"}


def test_invalid_file_returns_422():
    """Verificar que un archivo invalido retorna 422 Unprocessable Entity."""
    archivo_corrupto = io.BytesIO(b"esto no es un WAV valido")
    response = client.post(
        "/api/v1/analysis/impulse-response",
        files={"file": ("corrupto.wav", archivo_corrupto, "audio/wav")},
    )
    assert response.status_code == 422
