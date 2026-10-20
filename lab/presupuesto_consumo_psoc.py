"""Presupuesto de consumo del lado analogico (PSoC + front-end) a 5 V.

Suma la corriente de cada bloque que usa el proyecto AcondicionamientoAnalogico
(cyfitter.h: 4 opamps, 4 bloques SC, 4 VIDAC8 como IDAC, ADC DelSig, DFB, CPU a
24 MHz) segun las hojas de datos, mas las cargas externas, y aplica un factor de
seguridad. Uso: python lab/presupuesto_consumo_psoc.py [factor]  (default 2)

Fuentes de los valores [mA] (tipico, maximo):
  CPU/digital: CY8C58LP datasheet 001-84932 Rev *H, tabla 11-2, FCPU = 24 MHz.
  Opamp:       OpAmp_v1_90.pdf, IDD potencia alta.
  SC/PGA:      PGA_v2_0.pdf, IDD potencia alta.
  ADC DelSig:  ADC_DelSig_v3_30.pdf, IDD_20 sin buffer (+ IBUFF si buffer).
  IDAC8:       IDAC8_v2_0.pdf, IDD modo lento, rango 31,875 uA.
  DFB:         CY8C58LP tabla 11-58, 64 taps, interpolado a 24 MHz.
Lo marcado 'aprox.' no sale de una hoja de datos verificada.
"""
import sys

# (bloque, cantidad, tipico_mA, maximo_mA, nota)
BLOQUES = [
    ('CPU + digital (24 MHz, cache)', 1, 8.9, 10.5, 'datasheet familia'),
    ('Opamp potencia alta (OPAbp/lp/ref/sum)', 4, 1.0, 2.5, 'OpAmp_v1_90'),
    ('Bloque SC potencia alta (PGAgain/n/p/out)', 4, 1.5, 1.65, 'PGA_v2_0'),
    ('ADC DelSig 18 bits, sin buffer', 1, 1.5, 1.5, 'ADC_DelSig_v3_30 (solo max)'),
    ('Buffer de entrada del ADC (si se usa)', 1, 2.5, 2.5, 'ADC_DelSig_v3_30 (solo max)'),
    ('VIDAC8 como IDAC (consumo propio)', 4, 0.044, 0.100, 'IDAC8_v2_0'),
    ('Salida de los IDAC (fondo de escala)', 4, 0.032, 0.032, '31,875 uA cada uno'),
    ('DFB (filtro), 24 MHz', 1, 0.33 * 24, 0.53 * 24, 'tabla 11-58 escalada'),
    ('UDB: I2C, UART, SPI, timers', 1, 1.0, 3.0, 'aprox.'),
    ('Cargas externas de los opamps (R de 6,8-150 k)', 1, 0.3, 1.0, 'aprox.: |Vo-Vref|/R'),
    ('LED de encendido del kit', 1, 2.0, 5.0, 'aprox.'),
    ('Aislador I2C ISO1640, lado PSoC', 1, 2.0, 5.0, 'aprox.'),
    ('Aislador ISO7741, lado PSoC (4 canales)', 1, 3.6, 6.0, '0,9-1,5 mA/canal (TI)'),
    ('LDO TPS7A20 (consumo propio)', 1, 0.0065, 0.0065, 'TI'),
]
KITPROG = ('KitProg sin separar (otro PSoC 5LP + USB)', 1, 15.0, 30.0, 'aprox.')

CONVERTIDORES = [('UCC12050 en 5,4 V', 90.0), ('UCC12050 en 5,0 V', 100.0),
                 ('UCC33420 en 5,0/5,5 V', 300.0)]


def total(filas):
    t = sum(n * a for _, n, a, _, _ in filas)
    m = sum(n * b for _, n, _, b, _ in filas)
    return t, m


def main():
    factor = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    print('%-48s %4s %8s %8s  %s' % ('bloque', 'n', 'tip mA', 'max mA', 'fuente'))
    for nom, n, a, b, nota in BLOQUES + [KITPROG]:
        print('%-48s %4d %8.2f %8.2f  %s' % (nom, n, n * a, n * b, nota))
    for etiqueta, filas in (('sin KitProg', BLOQUES), ('con KitProg', BLOQUES + [KITPROG])):
        t, m = total(filas)
        print('\n%s: tipico %.1f mA, maximo %.1f mA, maximo x %.1f = %.1f mA'
              % (etiqueta, t, m, factor, m * factor))
        for conv, imax in CONVERTIDORES:
            margen = imax - m * factor
            print('   %-24s %5.0f mA -> margen %+6.1f mA %s'
                  % (conv, imax, margen, 'OK' if margen > 0 else 'NO ALCANZA'))


if __name__ == '__main__':
    main()
