"""Pruebas de analisis_ruido.py con volcados sinteticos.

Sin placa no se puede probar la adquisicion, pero SI todo el camino desde el
formato del volcado hasta los numeros: decodificacion de 24 bits con signo,
lotes faltantes, RMS de banda, y la comparacion dentro de la captura usando
las marcas de escritura de SD.
"""
import json
import os
import tempfile
import unittest

import numpy as np

from lab import analisis_ruido as ar


def _volcado(ruta, muestras, flags=None, meta=None, seq0=0, saltar=()):
    """Escribe un volcado con el mismo formato que emite `dumpusb`."""
    n_lotes = len(muestras) // ar.MUESTRAS_POR_LOTE
    flags = flags if flags is not None else np.zeros(len(muestras), np.uint8)
    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps({'meta': meta or {}, 'cabecera': {}}) + '\n')
        for L in range(n_lotes):
            if L in saltar:
                continue
            b = bytearray()
            for i in range(ar.MUESTRAS_POR_LOTE):
                k = L * ar.MUESTRAS_POR_LOTE + i
                v = int(muestras[k]) & 0xFFFFFF
                b += bytes([v & 0xFF, (v >> 8) & 0xFF,          # raw_lo/hi+
                            0, 0, 0,                            # alog (siempre 0)
                            v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF,
                            0, int(flags[k])])
            fh.write('%d %s\n' % (seq0 + L, b.hex()))


class Decodificacion(unittest.TestCase):
    def test_24_bits_con_signo_se_interpretan_negativos(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            base = [-1, -2048, 0, 2047, -8388608, 8388607]
            vals = np.array(base * (ar.MUESTRAS_POR_LOTE // len(base)))
            self.assertEqual(len(vals), ar.MUESTRAS_POR_LOTE)  # lote completo
            _volcado(r, vals)
            _, _, digi, _, _ = ar.cargar(r)
            np.testing.assert_array_equal(digi, vals)

    def test_un_valor_de_24_bits_no_se_trunca_a_16(self):
        # raw_lo/raw_hi son solo los 16 bits bajos y se envuelven; el analisis
        # tiene que leer digi, no raw.
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            vals = np.full(ar.MUESTRAS_POR_LOTE, 100000)
            _volcado(r, vals)
            _, _, digi, _, _ = ar.cargar(r)
            self.assertEqual(int(digi[0]), 100000)


class LotesFaltantes(unittest.TestCase):
    def test_cuenta_los_huecos_de_seq(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            vals = np.zeros(ar.MUESTRAS_POR_LOTE * 10)
            _volcado(r, vals, saltar=(3, 7))
            _, seqs, _, _, _ = ar.cargar(r)
            self.assertEqual(ar.lotes_faltantes(seqs), 2)

    def test_sin_huecos_da_cero(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            _volcado(r, np.zeros(ar.MUESTRAS_POR_LOTE * 5))
            _, seqs, _, _, _ = ar.cargar(r)
            self.assertEqual(ar.lotes_faltantes(seqs), 0)


class LecturaDesdeSD(unittest.TestCase):
    def test_extrae_el_lote_completo_emitido_por_sdread(self):
        # Una captura larga no pasa por dumpusb: cada `sdread` tiene que
        # devolver exactamente el mismo payload de 30 SampleBytes que el
        # volcado RAM, para que el analisis no pierda muestras intermedias.
        payload = bytes(i % 256 for i in range(ar.MUESTRAS_POR_LOTE * 10)).hex()
        lineas = [
            '[USB] SDREAD seq=7 raw[0]=0 raw[29]=0 sumRaw=0',
            '#SDREAD 7 ' + payload,
        ]
        self.assertEqual(ar.lote_sdread(lineas, 7), (7, payload))

    def test_junta_lotes_solo_si_la_secuencia_esta_completa(self):
        payload = bytes(i % 256 for i in range(ar.MUESTRAS_POR_LOTE * 10)).hex()
        self.assertEqual(
            ar.lotes_sdread(['#SDREAD 0 ' + payload, '#SDREAD 1 ' + payload], 2),
            [(0, payload), (1, payload)],
        )
        self.assertIsNone(ar.lotes_sdread(['#SDREAD 0 ' + payload], 2))


class RmsDeBanda(unittest.TestCase):
    def test_un_tono_dentro_de_la_banda_se_mide(self):
        fs = ar.FS_NATIVA
        n = 8192
        t = np.arange(n) / fs
        amp = 100.0
        x = amp * np.sqrt(2) * np.sin(2 * np.pi * 30.0 * t)
        self.assertAlmostEqual(ar.rms_banda(x), amp, delta=amp * 0.12)

    def test_un_tono_fuera_de_la_banda_no_se_cuenta(self):
        fs = ar.FS_NATIVA
        n = 8192
        t = np.arange(n) / fs
        x = 1000.0 * np.sin(2 * np.pi * 500.0 * t)      # muy afuera de 10-50
        self.assertLess(ar.rms_banda(x), 50.0)

    def test_la_continua_no_cuenta_como_ruido(self):
        # El offset es donde el lazo dejo el punto de trabajo, no ruido.
        x = np.full(8192, 5000.0)
        self.assertLess(ar.rms_banda(x), 1.0)


class DentroDeLaCaptura(unittest.TestCase):
    def test_separa_muestras_marcadas_por_escritura_de_sd(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            n = ar.MUESTRAS_POR_LOTE * 20
            rng = np.random.default_rng(0)
            x = rng.normal(0, 10, n)
            flags = np.zeros(n, np.uint8)
            # una de cada diez muestras cae durante una escritura y es ruidosa
            marca = np.arange(0, n, 10)
            flags[marca] = ar.FLAG_SD_WRITE
            x[marca] += rng.normal(0, 200, marca.size)
            _volcado(r, np.round(x).astype(int), flags,
                     meta={'pga': 1, 'pgaout': 1, 'condicion': 'SD',
                           'repeticion': 1})
            f = ar.resumen(r)
            self.assertEqual(f['muestras_marcadas_sd'], marca.size)
            self.assertGreater(f['rms_durante_sd'], 5 * f['rms_fuera_de_sd'])

    def test_sin_marcas_no_inventa_la_comparacion(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            _volcado(r, np.zeros(ar.MUESTRAS_POR_LOTE * 5),
                     meta={'pga': 1, 'pgaout': 1, 'condicion': 'BASE'})
            f = ar.resumen(r)
            self.assertIsNone(f['rms_durante_sd'])
            self.assertEqual(f['muestras_marcadas_sd'], 0)


class ReferidoALaEntrada(unittest.TestCase):
    def test_divide_por_la_ganancia_nominal(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'a.txt')
            fs = ar.FS_NATIVA
            n = ar.MUESTRAS_POR_LOTE * 200
            t = np.arange(n) / fs
            x = np.round(300 * np.sin(2 * np.pi * 25.0 * t)).astype(int)
            _volcado(r, x, meta={'pga': 4, 'pgaout': 8, 'condicion': 'BASE'})
            f = ar.resumen(r)
            self.assertEqual(f['ganancia'], 32)
            self.assertAlmostEqual(
                f['rms_banda_uV_ref_entrada'] * 32, f['rms_banda_uV'], places=6)


if __name__ == '__main__':
    unittest.main()
