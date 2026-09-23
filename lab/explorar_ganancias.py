"""explorar_ganancias.py - busca pares de ganancia por ENCIMA de los validados.

    py -3 explorar_ganancias.py [ventana_s]

Los seis pares del barrido de regresion llegan hasta ganancia conjunta 96
(x4/x24 y x24/x4). Esto prueba combinaciones mas altas para ver donde esta el
techo real del instrumento, no el de la busqueda. Usa el mismo veredicto que
banco_pi.py: banda declarada Y |LPo| adentro hasta el final.
"""
import sys, threading, time
import banco_pi as b

# (codigo_pga, codigo_pgaout) -> ganancia conjunta
# Medidos todos PASA el 2026-09-19 en una sola visita. Los tres mejores se
# revalidan con dos vueltas antes de darlos por buenos: una corrida es una
# corrida.
PARES = ((2, 5),    # x4  / x24 =  96  (referencia ya validada)
         (3, 5),    # x8  / x24 = 192
         (4, 5))    # x16 / x24 = 384

if __name__ == '__main__':
    ventana = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    threading.Thread(target=b._leer, daemon=True).start()
    time.sleep(1.5)
    b.prueba_ganancias(pares=PARES, vueltas=2, ventana=ventana)
    b._vivo = False
    time.sleep(0.3)
