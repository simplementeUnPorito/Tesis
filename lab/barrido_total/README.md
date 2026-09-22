# Resultados locales del barrido

Esta carpeta se conserva fuera de Git, salvo este archivo. Cada visita se
agrega inmediatamente a `resultados.jsonl`; `INFORME.md` y `resumen.csv` se
regeneran después de cada combinación. La subcarpeta `.run/` contiene PID y log
del lanzador Linux.

Los resultados no se borran al ejecutar `git pull`. Para continuar una corrida,
use `../barrido_total.sh start`; el lanzador aplica `--reanudar` y sólo repite
visitas inválidas.

## Servidor Linux

Conecte el USB del ESP32 y ejecute desde la raíz del repositorio:

```bash
git submodule update --init --recursive
chmod +x lab/barrido_total.sh
./lab/barrido_total.sh start 3 240
```

El proceso sigue activo al cerrar SSH. Para operarlo:

```bash
./lab/barrido_total.sh status
./lab/barrido_total.sh log
./lab/barrido_total.sh stop
```

Un supervisor local reinicia automáticamente el proceso ante fallos
transitorios, con espera creciente, y siempre reanuda desde la última visita
terminada. Sólo después de agotar ocho recuperaciones escribe
`.run/alert.json`. La consulta compacta para un operador Codex es:

```bash
./lab/barrido_total.sh operator
```

Devuelve una sola línea `OK`, `COMPLETE` o `ALERT`. Codex debe permanecer en
silencio ante `OK`, cerrar el seguimiento ante `COMPLETE` y leer el log completo
únicamente ante `ALERT`; así el caso normal no consume razonamiento ni tokens.

El lanzador crea un entorno virtual, instala `pyserial` y busca primero un
puerto estable en `/dev/serial/by-id/`. Si hay más de un adaptador, indique el
del ESP32 explícitamente:

```bash
BARRIDO_PORT=/dev/serial/by-id/usb-... ./lab/barrido_total.sh start 3 240
```

El servidor no necesita PSoC Creator, KitProg ni PowerShell. Si el PSoC deja de
confirmar una ganancia, el script manda `psocreset` al ESP32; éste pulsa GPIO19
hacia PSoC P1[4], cuya ISR ejecuta `CySoftwareReset()`.
