"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np
import pytest

from app.services.acoustic_parameters import (
    calcular_parametros_acusticos,
    integral_schroeder,
    regresion_lineal,
    suavizar_signal,
)
from app.services.filter import filtro_octava
from app.services.signal_utils import sintetizar_ri

# -----------------------------------------------------------------------------------------------


class TestSuavizarSignal:
    def test_suavizar_hilbert_envolvente(self):
        """La envolvente debe ser no negativa y suave."""

        fs = 48000
        t = np.linspace(0, 1, fs, endpoint=False)
        # senal oscilante con decaimiento, simula una RI
        signal = np.sin(2 * np.pi * 440 * t) * np.exp(-3 * t)
        envolvente = suavizar_signal(signal, ventana="hilbert")

        # No negativa
        assert np.all(envolvente >= 0)

        # Suave: la envolvente varia mucho menos brusco que la senal original
        # (menor "rugosidad" medida como la derivada de segundo orden)
        rugosidad_original = np.sum(np.abs(np.diff(signal, n=2)))
        rugosidad_envolvente = np.sum(np.abs(np.diff(envolvente, n=2)))
        assert rugosidad_envolvente < rugosidad_original

    def test_suavizar_media_movil_longitud(self):
        """La salida debe tener la misma longitud que la entrada."""
        signal = np.random.randn(1000)
        resultado = suavizar_signal(signal, ventana=50)
        assert len(resultado) == len(signal)

    # Tests adicionales para casos de error

    def test_suavizar_ventana_invalida(self):
        """Un string distinto de 'hilbert' debe lanzar ValueError."""
        signal = np.random.randn(100)
        with pytest.raises(ValueError):
            suavizar_signal(signal, ventana="mediana")

    def test_suavizar_ventana_negativa(self):
        """Un tamano de ventana no positivo debe lanzar ValueError."""
        signal = np.random.randn(100)
        with pytest.raises(ValueError):
            suavizar_signal(signal, ventana=0)


# -------------------------------------------------------------------------------


class TestIntegralSchroeder:
    """Tests para la funcion integral_schroeder."""

    def test_integral_schroeder_decreciente(self):
        """Verifica que la EDC es monotonamente decreciente."""
        ri = np.random.randn(1000)
        edc = integral_schroeder(ri)
        assert np.all(np.diff(edc) <= 0)

    def test_schroeder_maximo_cero_db(self):
        """El primer valor de la integral de Schroeder debe ser 0 dB."""
        np.random.seed(0)
        ri = np.random.randn(10000) * np.exp(-np.linspace(0, 5, 10000))
        curva = integral_schroeder(ri)
        assert curva[0] == pytest.approx(0.0, abs=1e-6)

    def test_schroeder_ri_sintetizada(self):
        """
        Para una RI sintetizada con T60 conocido, la curva de Schroeder
        debe ser aproximadamente lineal con pendiente -60/T60 dB/s.
        """
        np.random.seed(0)
        fs = 48000
        fc = 1000
        t60 = 2.0
        ri = sintetizar_ri(t60_por_banda={fc: t60}, fs=fs, duracion=3.0)
        ri_filtrada = filtro_octava(ri, fc=fc, fs=fs)
        curva = integral_schroeder(ri_filtrada)
        t = np.arange(len(curva)) / fs
        # Ajustar sobre el tramo -5 a -35 dB (evita ruido en los extremos)
        mask = (curva <= -5) & (curva >= -35)
        pendiente_esperada = -60.0 / t60
        m, _ = np.polyfit(t[mask], curva[mask], 1)
        assert m == pytest.approx(pendiente_esperada, rel=0.15)

    # Test adicional para caso de error
    def test_schroeder_entrada_vacia(self):
        """Debe lanzar ValueError si la RI esta vacia."""
        with pytest.raises(ValueError):
            integral_schroeder(np.array([]))

    def test_integral_schroeder_forma(self):
        """Verifica que la EDC tiene la misma longitud que la entrada."""
        ri = np.random.randn(1000)
        edc = integral_schroeder(ri)
        assert len(edc) == len(ri)


# -------------------------------------------------------------------------------


class TestRegresionLineal:
    """Tests para la funcion regresion_lineal."""

    def test_regresion_lineal_pendiente(self):
        """Verificar pendiente con datos conocidos."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        y = np.array([1.0, 3.0, 5.0, 7.0, 9.0])  # y = 2x + 1
        pendiente, ordenada, _ = regresion_lineal(x, y)
        assert pendiente == pytest.approx(2.0, abs=1e-9)
        assert ordenada == pytest.approx(1.0, abs=1e-9)

    def test_regresion_datos_perfectamente_lineales(self):
        """Para datos perfectamente lineales, R^2 debe ser 1.0."""
        x = np.linspace(0, 10, 50)
        m_real, b_real = -3.5, 2.0
        y = m_real * x + b_real
        pendiente, ordenada, r2 = regresion_lineal(x, y)
        assert pendiente == pytest.approx(m_real, abs=1e-9)
        assert ordenada == pytest.approx(b_real, abs=1e-9)
        assert r2 == pytest.approx(1.0, abs=1e-9)

    # Tests adicionales para casos de error

    def test_regresion_lineal_con_ruido(self):
        """Verifica que la regresion se aproxima a la recta con datos ruidosos."""
        np.random.seed(42)
        x = np.linspace(0, 10, 100)
        y = 3.0 * x + 5.0 + np.random.normal(0, 0.1, 100)
        pendiente, ordenada, _ = regresion_lineal(x, y)
        assert pendiente == pytest.approx(3.0, abs=0.05)
        assert ordenada == pytest.approx(5.0, abs=0.2)

    def test_regresion_longitudes_distintas(self):
        """Debe lanzar ValueError si x e y tienen longitudes distintas."""
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([1.0, 2.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)

    def test_regresion_pocos_puntos(self):
        """Debe lanzar ValueError con menos de 2 puntos."""
        x = np.array([1.0])
        y = np.array([1.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)

    def test_regresion_x_constante(self):
        """Debe lanzar ValueError si todos los x son iguales (recta vertical)."""
        x = np.array([5.0, 5.0, 5.0])
        y = np.array([1.0, 2.0, 3.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)


# -------------------------------------------------------------------------------


class TestCalcularParametrosAcusticos:
    def test_t30_dentro_de_tolerancia(self):
        """
        Sintetizar una RI con T60 = 2.0 s, calcular parametros
        y verificar que T30 esta dentro del +-10% del valor conocido.
        """
        np.random.seed(0)
        fs = 48000
        fc = 1000
        t60_objetivo = 2.0

        ri = sintetizar_ri(t60_por_banda={fc: t60_objetivo}, fs=fs, duracion=4.0)

        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=[fc])

        t30 = parametros["T30"][fc]
        assert t30 == pytest.approx(t60_objetivo, rel=0.10)

    def test_d50_rango_valido(self):
        """D50 debe estar entre 0% y 100%."""
        np.random.seed(0)
        fs = 48000
        fc = 1000
        ri = sintetizar_ri(t60_por_banda={fc: 1.0}, fs=fs, duracion=2.0)

        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=[fc])

        d50 = parametros["D50"][fc]
        assert 0.0 <= d50 <= 100.0

    def test_c80_consistencia(self):
        """Para una RI con mucha energia temprana, C80 debe ser positivo."""
        fs = 48000
        fc = 1000
        n_samples = int(2.0 * fs)

        # RI artificial con toda la energia concentrada en los primeros 10 ms
        # (mucho antes del corte de 80 ms que usa C80), y silencio despues
        ri = np.zeros(n_samples)
        ri[: int(0.01 * fs)] = np.random.randn(int(0.01 * fs))

        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=[fc])

        c80 = parametros["C80"][fc]
        assert c80 > 0

    # Tests adicionales para verificar la estructura de salida y el manejo de múltiples bandas

    def test_estructura_del_diccionario(self):
        """La salida debe tener la forma dict[str, dict[fc, valor]]."""
        np.random.seed(0)
        fs = 48000
        ri = sintetizar_ri(t60_por_banda={1000: 1.0}, fs=fs, duracion=2.0)

        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=[1000])

        assert set(parametros.keys()) == {"EDT", "T10", "T20", "T30", "T60", "D50", "C80"}
        for clave in parametros:
            assert 1000 in parametros[clave]
            assert isinstance(parametros[clave][1000], float)

    def test_multiples_bandas(self):
        """Debe calcular parametros para todas las bandas pedidas."""
        np.random.seed(0)
        fs = 48000
        bandas = [500.0, 1000.0, 2000.0]
        ri = sintetizar_ri(
            t60_por_banda={500: 1.5, 1000: 1.5, 2000: 1.5},
            fs=fs,
            duracion=3.0,
        )

        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=bandas)

        for clave in ("EDT", "T20", "T30"):
            assert set(parametros[clave].keys()) == set(bandas)

    def test_edt_t20_t30_similares_en_ri_sintetica(self):
        """
        Para una RI sintetica ideal (decaimiento exponencial puro sin
        reflexiones tempranas), EDT ~= T20 ~= T30.
        """
        np.random.seed(0)
        fs = 48000
        fc = 1000
        t60 = 1.5

        ri = sintetizar_ri(t60_por_banda={fc: t60}, fs=fs, duracion=3.0)
        parametros = calcular_parametros_acusticos(ri, fs=fs, bandas=[fc])

        edt = parametros["EDT"][fc]
        t20 = parametros["T20"][fc]
        t30 = parametros["T30"][fc]

        assert edt == pytest.approx(t30, rel=0.15)
        assert t20 == pytest.approx(t30, rel=0.15)

    def test_calcular_parametros_sin_filtrar(self):
        """Con sin_filtrar=True, calcula sobre la RI completa sin pasar por filtro_octava."""
        fs = 48000
        t60_conocido = 2.0
        # fc=1000 es arbitraria: solo se usa para sintetizar el decaimiento,
        # sin_filtrar=True hace que calcular_parametros_acusticos NO filtre por banda
        ri = sintetizar_ri(t60_por_banda={1000.0: t60_conocido}, fs=fs, duracion=3.0)

        resultado = calcular_parametros_acusticos(ri, fs, sin_filtrar=True)

        assert set(resultado["T30"].keys()) == {0.0}

        t30 = resultado["T30"][0.0]
        assert abs(t30 - t60_conocido) / t60_conocido < 0.10
