"""Pruebas sin hardware para el orquestador de campanas de ruido."""
import shutil
import sys
from pathlib import Path

from lab import campana_ruido


def test_plan_rf_y_filtro_solo_conservan_orden_y_ajustes():
    plan = campana_ruido.cargar_plan("rf")

    assert [paso["exp"] for paso in plan[:4]] == [
        "W1_radio", "W1b_ping", "W5_lpo_pgaout1", "W3b_potencia"
    ]
    assert plan[2] == {
        "exp": "W5_lpo_pgaout1",
        "cond": ["PING", "RF10", "RF240", "RX"],
        "rep": 3,
        "pga": 3,
        "pgaout": 0,
        "tap": 4,
        "nota": "Comparacion RF y recepcion en LPo",
        "requiere_maestro": True,
    }
    assert [p["exp"] for p in campana_ruido.filtrar_plan(plan, "W5,W9")] == [
        "W5_lpo_pgaout1",
        "W5_tap0", "W5_tap1", "W5_tap2", "W5_tap3",
        "W9_ganancia_pga0", "W9_ganancia_pga2", "W9_ganancia_pga4",
    ]


def test_comando_de_medicion_usa_python_y_scripts_absolutos(tmp_path):
    paso = campana_ruido.cargar_plan("rf")[2]

    comando = campana_ruido.comando_medicion(
        paso, tmp_path, port="COM8", maestro="COM6", nota="placa A"
    )

    assert comando[0] == sys.executable
    assert Path(comando[1]).is_absolute()
    assert comando[2:8] == [
        "correr", "--port", "COM8", "--maestro", "COM6", "--raiz"
    ]
    assert comando[comando.index("--cond") + 1:comando.index("--rep")] == [
        "PING", "RF10", "RF240", "RX"
    ]
    assert comando[comando.index("--nota") + 1] == (
        "placa A; Comparacion RF y recepcion en LPo"
    )


def test_subproceso_silencioso_termina_como_colgado(tmp_path):
    falso = tmp_path / "silencioso.py"
    falso.write_text(
        "import time\ntime.sleep(30)\n",
        encoding="utf-8",
    )
    log = tmp_path / "campana.log"

    resultado = campana_ruido.ejecutar_con_vigilancia(
        [sys.executable, str(falso)],
        log,
        silencio_s=0.15,
        limite_s=5.0,
        intervalo_s=0.02,
    )

    assert resultado.estado == "colgado"
    assert resultado.motivo == "silencio"
    assert "!! colgado" in log.read_text(encoding="utf-8")


def test_codigo_3_termina_como_no_convergio(tmp_path):
    falso = tmp_path / "no_convergio.py"
    falso.write_text(
        "raise SystemExit(3)\n",
        encoding="utf-8",
    )
    log = tmp_path / "campana.log"

    resultado = campana_ruido.ejecutar_con_vigilancia(
        [sys.executable, str(falso)],
        log,
        silencio_s=5.0,
        limite_s=5.0,
        intervalo_s=0.02,
    )

    assert resultado.estado == "no_convergio"
    assert resultado.motivo == "codigo 3"
    assert resultado.retorno == 3
    salida = campana_ruido.escribir_campana_md(
        tmp_path,
        estado={"pasos": {"W_timeout": {"estado": resultado.estado}}},
    )
    assert "Estado: no_convergio" in salida.read_text(encoding="utf-8")


def test_campana_md_incluye_tabla_del_ejemplo_w5_tap0(tmp_path):
    origen = Path(__file__).parent / "ruido_rf_20261020" / "W5_tap0"
    destino = tmp_path / "W5_tap0"
    shutil.copytree(origen, destino)

    salida = campana_ruido.escribir_campana_md(tmp_path, estado={})
    texto = salida.read_text(encoding="utf-8")

    assert "W5_tap0" in texto
    assert "sin estado" in texto
    assert "| cond | n | p2p cuentas | veredicto |" in texto
    assert "| PING | 4 | 18.1+-0.52 | referencia |" in texto
    assert "| RF240 | 4 | 338+-2.2e+02 | EFECTO |" in texto
