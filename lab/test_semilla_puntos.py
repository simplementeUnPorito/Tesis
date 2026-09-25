"""Tests de lab/semilla_puntos.py con unittest (sin dependencias externas)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from lab import semilla_puntos as sp


def visita(
    marca="2026-01-01 00:00:00",
    pga=1,
    pgaout=1,
    pga_cod=0,
    pgaout_cod=0,
    vuelta=1,
    veredicto="PASA",
    lpo=0.0,
    pp=1.0,
    idac=(0, 0, 0, 0),
    muestras_validas=20,
    **extra,
):
    """Arma una visita sintética mínima con los campos que usa el script.

    Por defecto trae `taps.LP.valido_pct` y `duracion_s` tales que
    `n_validas()` da exactamente `muestras_validas` (20 por defecto, bien
    por encima del umbral de 15), para que los tests que no ponen a prueba
    la guarda de muestras válidas no se vean afectados por ella. Pasar
    `taps=` o `duracion_s=` en `extra` pisa este valor por defecto.
    """
    d = {
        "marca": marca,
        "pga": pga,
        "pgaout": pgaout,
        "pga_cod": pga_cod,
        "pgaout_cod": pgaout_cod,
        "vuelta": vuelta,
        "veredicto": veredicto,
        "LPo_final_mV": lpo,
        "LPo_pp_final_mV": pp,
        "idac_final": list(idac),
        "duracion_s": muestras_validas * sp.MUESTREO_S,
        "taps": {"LP": {"valido_pct": 100.0}},
    }
    d.update(extra)
    return d


class TestDeduplicacion(unittest.TestCase):
    def test_dedup_por_marca_pga_pgaout_vuelta(self):
        # Misma clave repetida (simula una campaña que arrastra la semilla de otra).
        v1 = visita(marca="A", pga=1, pgaout=1, vuelta=1, lpo=10.0)
        v1_dup = visita(marca="A", pga=1, pgaout=1, vuelta=1, lpo=10.0)
        # Clave distinta por vuelta.
        v2 = visita(marca="A", pga=1, pgaout=1, vuelta=2, lpo=20.0)
        # Clave distinta por marca.
        v3 = visita(marca="B", pga=1, pgaout=1, vuelta=1, lpo=30.0)

        resultado = sp.deduplicar([v1, v1_dup, v2, v3])
        self.assertEqual(len(resultado), 3)

    def test_dedup_no_borra_visitas_de_pares_distintos(self):
        visitas = [
            visita(marca="A", pga=1, pgaout=1, vuelta=1),
            visita(marca="A", pga=2, pgaout=1, vuelta=1, pga_cod=1),
        ]
        resultado = sp.deduplicar(visitas)
        self.assertEqual(len(resultado), 2)


class TestNota(unittest.TestCase):
    """Umbrales de nota, siempre con pp y muestras_validas de sobra (1.0 y 20)
    para aislar el umbral de |LPo| que se está probando en cada caso."""

    def test_umbral_nota_a_borde(self):
        self.assertEqual(sp.nota_de(24.3, 1.0, 20), "A")
        self.assertEqual(sp.nota_de(24.31, 1.0, 20), "B")

    def test_umbral_nota_b_borde(self):
        self.assertEqual(sp.nota_de(48.5, 1.0, 20), "B")
        self.assertEqual(sp.nota_de(48.51, 1.0, 20), "C")

    def test_umbral_nota_c_borde(self):
        self.assertEqual(sp.nota_de(73.0, 1.0, 20), "C")
        self.assertEqual(sp.nota_de(73.01, 1.0, 20), "D")

    def test_nota_d_lejos_del_borde(self):
        self.assertEqual(sp.nota_de(200.0, 1.0, 20), "D")

    def test_nota_a_lejos_del_borde(self):
        self.assertEqual(sp.nota_de(0.0, 1.0, 20), "A")


class TestGuardaMuestrasValidas(unittest.TestCase):
    """La guarda que faltaba: sin ventana de pp llena (>=15 muestras válidas
    de LPo), la visita no tiene nota, sin importar qué tan bueno se vea
    `LPo_final_mV` o `LPo_pp_final_mV`."""

    def test_borde_14_rechaza_15_acepta(self):
        # |LPo| y pp de sobra dentro de umbral; sólo cambia muestras_validas.
        self.assertIsNone(sp.nota_de(1.0, 1.0, 14))
        self.assertEqual(sp.nota_de(1.0, 1.0, 15), "A")

    def test_una_sola_muestra_valida_con_pp_cero_no_tiene_nota(self):
        # El caso que rompía todo: con 1 sola muestra válida, max-min de una
        # lista de un elemento da 0.0 y un pp de 0.0 se veía "perfectamente
        # quieto" sin serlo. La visita no debe recibir nota ni ser candidata.
        v = visita(
            pga_cod=0, pgaout_cod=0, lpo=5.0, pp=0.0, idac=(1, 1, 1, 1),
            taps={"LP": {"valido_pct": 0.7}}, duracion_s=961.9,
        )
        nv = sp.n_validas(v)
        self.assertLess(nv, 15)
        self.assertIsNone(sp.nota_de(abs(v["LPo_final_mV"]), v["LPo_pp_final_mV"], nv))

        mejores = sp.elegir_mejores([v])
        self.assertNotIn((0, 0), mejores)

    def test_n_validas_desde_valido_pct_y_duracion(self):
        # 100 % de validez sobre 40 s de barrido a 2 s/muestra -> 20 muestras.
        v = visita(taps={"LP": {"valido_pct": 100.0}}, duracion_s=40.0)
        self.assertEqual(sp.n_validas(v), 20)
        # 2.6 % sobre 962 s (caso real citado: x16/x1) -> ronda a 13.
        v2 = visita(taps={"LP": {"valido_pct": 2.6}}, duracion_s=962.2)
        self.assertEqual(sp.n_validas(v2), 13)

    def test_n_validas_sin_taps_da_cero(self):
        v = visita()
        del v["taps"]
        self.assertEqual(sp.n_validas(v), 0)

    def test_n_validas_sin_duracion_da_cero(self):
        v = visita()
        del v["duracion_s"]
        self.assertEqual(sp.n_validas(v), 0)


class TestPasaEstricto(unittest.TestCase):
    def test_umbral_pp_borde(self):
        # pp < 30 estricto: 30.0 no pasa, 29.99 sí (si LPo está dentro de ventana).
        self.assertTrue(sp.pasa_estricto(29.99, 0.0))
        self.assertFalse(sp.pasa_estricto(30.0, 0.0))

    def test_umbral_no_clavado_borde(self):
        self.assertTrue(sp.pasa_estricto(1.0, 73.0))
        self.assertFalse(sp.pasa_estricto(1.0, 73.01))

    def test_falla_por_ambos(self):
        self.assertFalse(sp.pasa_estricto(50.0, 100.0))


class TestPenal(unittest.TestCase):
    def test_penal_cero_por_debajo_de_200(self):
        self.assertEqual(sp.penal(0), 0.0)
        self.assertEqual(sp.penal(199), 0.0)
        self.assertEqual(sp.penal(200), 0.0)

    def test_penal_crece_por_encima_de_200(self):
        self.assertEqual(sp.penal(201), 5.0)
        self.assertEqual(sp.penal(210), 50.0)
        self.assertEqual(sp.penal(255), 275.0)

    def test_penal_es_monotona(self):
        self.assertLess(sp.penal(210), sp.penal(220))


class TestFragilVsNoFragil(unittest.TestCase):
    def test_no_fragil_gana_aunque_tenga_peor_lpo(self):
        # Candidato frágil: |LPo| pequeño pero IDAC3 clavado contra el tope.
        fragil = visita(pga_cod=3, pgaout_cod=3, lpo=1.0, pp=1.0, idac=(10, 10, 10, 250))
        # Candidato no frágil: |LPo| más grande pero dentro de nota B e IDAC3 sano.
        no_fragil = visita(pga_cod=3, pgaout_cod=3, lpo=40.0, pp=1.0, idac=(10, 10, 10, 50))

        mejores = sp.elegir_mejores([fragil, no_fragil])
        elegido = mejores[(3, 3)]
        self.assertFalse(elegido["fragil"])
        self.assertEqual(elegido["LPo_final_mV"], 40.0)

    def test_entre_dos_no_fragiles_gana_menor_score(self):
        peor = visita(pga_cod=0, pgaout_cod=0, lpo=40.0, idac=(0, 0, 0, 0))
        mejor = visita(pga_cod=0, pgaout_cod=0, lpo=5.0, idac=(0, 0, 0, 0))
        mejores = sp.elegir_mejores([peor, mejor])
        self.assertEqual(mejores[(0, 0)]["LPo_final_mV"], 5.0)

    def test_visita_nota_d_no_es_candidata(self):
        # |LPo| = 100 mV -> nota D, no debe entrar aunque sea la única visita del par.
        v = visita(pga_cod=0, pgaout_cod=0, lpo=100.0)
        mejores = sp.elegir_mejores([v])
        self.assertNotIn((0, 0), mejores)

    def test_idac_incompleto_se_descarta(self):
        v = dict(visita(pga_cod=0, pgaout_cod=0, lpo=1.0))
        v["idac_final"] = [1, 2, 3]  # sólo 3 valores, no 4
        mejores = sp.elegir_mejores([v])
        self.assertNotIn((0, 0), mejores)


class TestPenalIdac2(unittest.TestCase):
    def test_score_penaliza_idac2_tambien(self):
        # Mismo LPo e IDAC3, pero uno tiene IDAC2 alto -> peor score.
        base = visita(pga_cod=0, pgaout_cod=0, lpo=5.0, idac=(0, 0, 10, 0))
        con_idac2_alto = visita(pga_cod=0, pgaout_cod=0, lpo=5.0, idac=(0, 0, 220, 0))
        s_base = sp.score_de(abs(base["LPo_final_mV"]), base["idac_final"])
        s_alto = sp.score_de(abs(con_idac2_alto["LPo_final_mV"]), con_idac2_alto["idac_final"])
        self.assertGreater(s_alto, s_base)


class TestEmpaquetadoPar(unittest.TestCase):
    def test_par_pga_cod_por_9_mas_pgaout_cod(self):
        casos = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 9),
            (8, 8, 80),
            (3, 5, 32),
        ]
        for pga_cod, pgaout_cod, esperado in casos:
            self.assertEqual(pga_cod * 9 + pgaout_cod, esperado)

    def test_reporte_incluye_par_correcto(self):
        v = visita(pga_cod=2, pgaout_cod=3, lpo=1.0, idac=(0, 0, 0, 0))
        mejores = sp.elegir_mejores([v])
        reporte = sp.construir_reporte(mejores, fuentes=[])
        punto = reporte["puntos"][0]
        self.assertEqual(punto["par"], 2 * 9 + 3)


class TestComandos(unittest.TestCase):
    def test_formato_de_linea(self):
        v = visita(pga_cod=0, pgaout_cod=0, lpo=1.0, idac=(1, -2, 3, -4))
        mejores = sp.elegir_mejores([v])
        reporte = sp.construir_reporte(mejores, fuentes=[])
        lineas = sp.imprimir_comandos(reporte, incluir_fragiles=False)
        self.assertEqual(lineas, ["punto 0 1 -2 3 -4"])

    def test_fragiles_se_omiten_por_defecto(self):
        v = visita(pga_cod=0, pgaout_cod=0, lpo=1.0, idac=(1, 1, 1, 250))
        mejores = sp.elegir_mejores([v])
        reporte = sp.construir_reporte(mejores, fuentes=[])
        self.assertEqual(sp.imprimir_comandos(reporte, incluir_fragiles=False), [])
        self.assertEqual(len(sp.imprimir_comandos(reporte, incluir_fragiles=True)), 1)


class TestIntegracionDatosReales(unittest.TestCase):
    """Corre sobre los jsonl reales del repo y verifica los conteos conocidos."""

    def test_conteos_reales(self):
        raiz = Path(__file__).resolve().parent.parent
        rutas = [
            raiz / "lab" / "barrido_local_20260922" / "resultados.jsonl",
            raiz / "lab" / "barrido_reaprendizaje_20260923" / "resultados.jsonl",
        ]
        for r in rutas:
            if not r.exists():
                self.skipTest(f"no se encontró {r} (test de integración, requiere los datos reales)")

        visitas_crudas, fuentes = sp.cargar_visitas([str(r) for r in rutas])
        visitas = sp.deduplicar(visitas_crudas)

        self.assertEqual(len(visitas), 191)

        conteo = {"PASA": 0, "FALLA": 0, "APRENDIENDO": 0}
        for v in visitas:
            conteo[v["veredicto"]] += 1

        self.assertEqual(conteo["PASA"], 90)
        self.assertEqual(conteo["FALLA"], 66)
        self.assertEqual(conteo["APRENDIENDO"], 35)

        # Con la guarda de muestras válidas (>=15) puesta, de los 81 pares
        # posibles sólo 42 tienen un punto candidato de nota A/B; de esos,
        # 31 son no frágiles; y 5 pares tuvieron 2 o más candidatas en pugna.
        mejores = sp.elegir_mejores(visitas)
        self.assertEqual(len(mejores), 42)

        no_fragiles = sum(1 for v in mejores.values() if not v["fragil"])
        self.assertEqual(no_fragiles, 31)

        con_dos_o_mas = sum(1 for v in mejores.values() if v["n_candidatas"] >= 2)
        self.assertEqual(con_dos_o_mas, 5)


if __name__ == "__main__":
    unittest.main()
