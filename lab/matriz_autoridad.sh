#!/bin/bash
# matriz_autoridad.sh - mide la autoridad de los cuatro IDAC en toda la cadena.
#
# Orden DELIBERADO: lo que mas decide, primero.  Si hay que cortar, se corta
# por abajo y lo importante ya esta medido.
#
#  1-2  IDAC0 a PGA x4 y x50 (PGAout x1)
#       Es LA medicion del fin de semana.  La topologia dice que el corrimiento
#       de la referencia del INA atraviesa el PGA variable entero, o sea que su
#       autoridad escala con G.  Si ademas da la pendiente, R0 sale despejada:
#       hoy el firmware dice 15 k y los datos de campana sugieren ~680 Ohm, y
#       ya paso antes que un #define de resistencia estuviera viejo (el del LP
#       decia 1 k cuando eran 10 k, y erro la autoridad de IDAC3 por 10x).
#       Ademas: los dos puntos juntos dicen si escala o no, que es lo que
#       decide si hay que cambiar componentes el martes.
#
#  3-4  IDAC1 a PGA x4 y x50 (PGAout x1)
#       Deberia ser PLANO: inyecta en la referencia del BP, que esta despues
#       del PGA variable.  Si sale plano confirma la topologia entera; si
#       escala, algo del esquematico no es lo que creemos.
#
#  5-6  IDAC2 a PGAout x4 y x24 (PGA x1)
#       Inyecta en el sumador, antes de PGAout: su efecto sobre OPA_SUM NO
#       deberia escalar y sobre SUM y LP SI.  De ahi sale el valor real de
#       CP_COARSE_SLOPE_UV referido a x24, que hoy esta en -150 mV/codigo sin
#       respaldo medido y del que depende el descargue del vernier.
#
#   7   IDAC3 a PGAout x24 (PGA x1)
#       Tercer punto para confirmar que NO escala.  Ya medido 0,41 a x1 y 0,49
#       a x16; si a x24 sigue igual, queda cerrado que inyecta despues de
#       PGAout y que un solo FINE_SLOPE sirve para los 81 pares.
#
# Codigos de ganancia: 0=x1 1=x2 2=x4 3=x8 4=x16 5=x24 6=x32 7=x48 8=x50
#
# Uso:  bash lab/matriz_autoridad.sh            todo
#       bash lab/matriz_autoridad.sh 1 2        solo los pasos 1 y 2
set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p lab/autoridad

corrida() {
    local n="$1" idac="$2" pga="$3" pgaout="$4" nota="$5"
    local salida="lab/autoridad/paso${n}_idac${idac}.json"
    if [ -f "$salida" ]; then
        echo "== paso $n ya estaba hecho ($salida); se saltea"
        return 0
    fi
    echo
    echo "======================================================================"
    echo "== paso $n: IDAC$idac  PGA=cod$pga  PGAout=cod$pgaout"
    echo "== $nota"
    echo "======================================================================"
    python -u lab/escalon_idac.py --idac "$idac" --pga "$pga" \
        --pgaout "$pgaout" --salida "$salida" 2>&1
    local r=$?
    if [ $r -ne 0 ]; then
        echo "== paso $n FALLO con codigo $r"
    fi
    return $r
}

pasos="${*:-1 2 3 4 5 6 7}"
for p in $pasos; do
  case "$p" in
    1) corrida 1 0 2 0 "IDAC0 a PGA x4: da la pendiente base y R0" ;;
    2) corrida 2 0 8 0 "IDAC0 a PGA x50: escala x12,5 respecto del paso 1?" ;;
    3) corrida 3 1 2 0 "IDAC1 a PGA x4: base" ;;
    4) corrida 4 1 8 0 "IDAC1 a PGA x50: deberia ser PLANO vs el paso 3" ;;
    5) corrida 5 2 0 2 "IDAC2 a PGAout x4" ;;
    6) corrida 6 2 0 5 "IDAC2 a PGAout x24: escala en SUM/LP, plano en OPA_SUM?" ;;
    7) corrida 7 3 0 5 "IDAC3 a PGAout x24: tercer punto, deberia NO escalar" ;;
    *) echo "paso desconocido: $p" ;;
  esac
done
echo
echo "======================================================================"
echo "matriz terminada.  Crudos en lab/autoridad/"
ls -la lab/autoridad/ 2>/dev/null
