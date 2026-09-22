# Operador Codex del barrido

Ejecutar `./lab/barrido_total.sh operator` en el servidor. La salida es el
contrato completo del operador:

- `OK`: no hacer nada y no notificar. La recuperación predecible pertenece al
  supervisor, no a Codex.
- `COMPLETE`: informar una sola vez que terminó y dejar de vigilar.
- `ALERT`: inspeccionar `lab/barrido_total/.run/barrido.log`, el journal del
  servicio (`journalctl --user -u barrido-total.service`) y
  `lab/barrido_total/resultados.jsonl`. Intentar únicamente acciones seguras y
  reversibles. Se puede ejecutar `./lab/barrido_total.sh restart 3 240` después
  de corregir una causa concreta. Notificar sólo si persiste, si falta el
  hardware/puerto, o si hace falta una decisión humana.

No leer logs ni hacer diagnósticos cuando la salida sea `OK`. No modificar
ganancias, criterios, firmware ni pinout como reacción automática.

El demonio `barrido_codex_operator.py` observa únicamente `alert.json`; no
consulta a ningún modelo durante estados `OK`, `waiting_for_device` o
`recovering`. Cada alerta distinta se entrega a Codex una sola vez y se archiva
para impedir reintentos que consuman tokens.
