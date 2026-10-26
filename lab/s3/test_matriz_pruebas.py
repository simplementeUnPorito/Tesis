import importlib.util
from pathlib import Path


RUTA = Path(__file__).with_name("matriz_pruebas.py")
SPEC = importlib.util.spec_from_file_location("matriz_pruebas", RUTA)
matriz = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(matriz)


def captura(n2=200, n3=200, n4=200, faltan=0, nan=0):
    return {
        "nodos": {
            "2": {"lotes_vistos": n2, "n_faltan": faltan, "nan": nan, "muestras": n2 * 30},
            "3": {"lotes_vistos": n3, "n_faltan": faltan, "nan": nan, "muestras": n3 * 30},
            "4": {"lotes_vistos": n4, "n_faltan": faltan, "nan": nan, "muestras": n4 * 30},
        }
    }


def test_parsear_nodos_rechaza_repetidos_y_fuera_de_rango():
    assert matriz.parsear_nodos("2, 3,4") == [2, 3, 4]

    for texto in ("2,2", "0,2", "256", ""):
        try:
            matriz.parsear_nodos(texto)
        except ValueError:
            pass
        else:
            raise AssertionError(f"se aceptó una lista inválida: {texto!r}")


def test_resumir_captura_finita_exige_todos_los_lotes_y_cero_huecos():
    ok = matriz.resumir_captura(captura(), [2, 3, 4], lotes_esperados=200)
    mal = matriz.resumir_captura(captura(n3=199), [2, 3, 4], lotes_esperados=200)

    assert ok["pass"] is True
    assert ok["por_nodo"]["3"]["lotes_vistos"] == 200
    assert mal["pass"] is False
    assert "S3" in mal["cifras"]


def test_resumir_captura_sin_limite_exige_igualdad_y_cero_huecos():
    ok = matriz.resumir_captura(captura(2610, 2610, 2610), [2, 3, 4], mismos_lotes=True)
    mal = matriz.resumir_captura(captura(2610, 2609, 2610), [2, 3, 4], mismos_lotes=True)

    assert ok["pass"] is True
    assert mal["pass"] is False


def test_resumir_log_cuenta_incidentes_y_descarta_coredump_vacio():
    lineas = [
        "10:00:00 [M] [TXSTALL] sin avisos de envio hace 5000 ms",
        "10:00:00 [M] [TXSTALL] canal=1 sec=0",
        "10:00:01 [M] [FTM] S2 st=4 ev=3 modelo=0",
        "10:00:02 [M] vigia vencido",
        "10:00:03 [M] [S3>] [slaveS3 3] boot chip=ESP32-S3",
        "10:00:04 Guru Meditation Error: Core 1 panic'ed",
        "10:00:05 [M] [S2>] [COREDUMP] no hay (reset=3)",
        "10:00:06 [M] [S3>] [COREDUMP] tarea=loopTask pc=0x123",
        "10:00:07 [FTM] responder sin respuesta para S4",
    ]

    r = matriz.resumir_log(lineas)

    assert r == {
        "txstall": 1,
        "no_response_ftm": 1,
        "responder_sin_respuesta": 1,
        "vigia": 1,
        "reinicios_esclavos": 1,
        "panicos": 1,
        "coredump": 1,
    }


def test_resumir_sync_usa_el_start_del_tramo_y_nodos_convertidos():
    lineas = [
        "12:00:00 [M] [MASTER] START t0=100 ftm=1 mac=200",
        "12:00:01 [M] [S2>] [SYNCFTM] objetivo_maestro=300 real_maestro=311 err_us=11 conv=1",
        "12:00:01 [M] [S3>] [SYNCFTM] objetivo_maestro=300 real_maestro=325 err_us=25 conv=1",
        "12:00:01 [M] [S4>] [SYNCFTM] objetivo_maestro=300 real_maestro=319 err_us=19 conv=1",
    ]

    r = matriz.resumir_sync(lineas, [2, 3, 4], exigir_ftm=True, limite_us=20)

    assert r["pass"] is True
    assert r["start_ftm"] == 1
    assert r["metodo"] == "SYNCFTM"
    assert r["dispersion_us"] == 14


def test_resumir_sync_falla_si_falta_un_nodo_o_start_no_es_ftm():
    lineas = [
        "12:00:00 [M] [MASTER] START t0=100 ftm=0 mac=0",
        "12:00:01 [M] [S2>] [SYNCFTM] real_maestro=311 conv=1",
        "12:00:01 [M] [S3>] [SYNCFTM] real_maestro=312 conv=1",
    ]

    r = matriz.resumir_sync(lineas, [2, 3, 4], exigir_ftm=True, limite_us=20)

    assert r["pass"] is False
    assert r["nodos"] == [2, 3]


def test_resumir_duracion_valida_un_por_ciento_y_atraso_maximo():
    datos = {
        "fs": 2604.0,
        "segundos": 120.0,
        "final": {"2": 10416, "3": 10415, "4": 10417},
        "filas": [
            {"S2_atraso": 3.0, "S3_atraso": 8.0, "S4_atraso": 4.0},
            {"S2_atraso": 7.0, "S3_atraso": 2.0, "S4_atraso": 9.0},
        ],
    }

    r = matriz.resumir_duracion(datos, [2, 3, 4])

    assert r["pass"] is True
    assert r["esperado"] == 10416
    assert r["atraso_maximo"] == {"2": 7.0, "3": 8.0, "4": 9.0}


def test_resumir_duracion_falla_fuera_del_un_por_ciento():
    datos = {
        "fs": 2604.0,
        "segundos": 120.0,
        "final": {"2": 10200, "3": 10416, "4": 10416},
        "filas": [],
    }

    assert matriz.resumir_duracion(datos, [2, 3, 4])["pass"] is False


def test_plan_respeta_solo_saltar_y_pruebas_opcionales():
    ids = [p.id for p in matriz.armar_plan(solo={"rt_0", "ota"}, saltar=set(), con_ota=False,
                                           con_duracion=False)]
    assert ids == ["rt_0", "ota"]

    ids = [p.id for p in matriz.armar_plan(solo=set(), saltar={"async_1"}, con_ota=False,
                                           con_duracion=False)]
    assert "async_1" not in ids
    assert "ota" not in ids
    assert "duracion" not in ids
    assert ids[-1] == "salud"


def test_main_no_exige_nodo_ota_si_ota_no_esta_en_el_plan(capsys):
    codigo = matriz.main(["--dry-run", "--nodos", "2,3", "--solo", "salud"])

    assert codigo == 0
    assert "salud" in capsys.readouterr().out
