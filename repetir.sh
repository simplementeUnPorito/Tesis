#!/usr/bin/env bash
# Corre la misma calibracion N veces y junta los veredictos.
#
# Un exito aislado no es un algoritmo funcional. La corrida de las 08:53 dejo
# los cinco taps en ventana y LPo en +35 mV; lo que falta saber es si eso se
# repite, y con cuanta dispersion.
set -u
DESTINO="${1:?falta carpeta}"; PGA="${2:-1}"; PGAOUT="${3:-1}"; N="${4:-3}"
mkdir -p "$DESTINO"
RES="$DESTINO/resumen.txt"; : > "$RES"
for i in $(seq 1 "$N"); do
    log="$DESTINO/corrida_$i.log"
    echo "=== corrida $i de $N: PGA x$PGA, PGAout x$PGAOUT ===" | tee -a "$RES"
    taskkill //F //IM python.exe > /dev/null 2>&1
    sleep 4
    timeout 1800 py -3 centrar_lpo.py --port COM8 --pga "$PGA" \
        --pgaout "$PGAOUT" > "$log" 2>&1
    v=$(grep -E "PGAout x[0-9]+:|LPo final|Corrimiento|IDAC0=|fuera de ventana:" "$log" | tail -5)
    [ -z "$v" ] && v="sin veredicto; ultima linea: $(tail -1 "$log")"
    echo "$v" | tee -a "$RES"
    echo | tee -a "$RES"
done
echo "Resumen en $RES"
