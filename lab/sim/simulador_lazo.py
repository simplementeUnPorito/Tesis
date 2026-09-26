"""simulador_lazo.py - el lazo REAL del firmware contra una planta de PC.

Por que existe: cada idea sobre el lazo costaba entre 30 y 90 minutos de
banco, y varias murieron en el primer minuto.  Aca el mismo codigo C del
firmware -`control_config.c`, compilado tal cual, sin reescribir nada- corre
contra un modelo de la cadena analogica y una prueba tarda milisegundos.

Lo que NO es: un sustituto de la placa.  El modelo es de primer orden y los
parametros tienen incertidumbre; sirve para descartar ideas y para entender
mecanismos, no para dar por bueno un arreglo.  Todo lo que salga de aca se
confirma en la placa antes de creerselo.

## La planta

Medido el 2026-09-26 con el PI congelado (banda muerta ancha), escalones
alternados A-B-A-B-A y permanencias de 360 s (~9 tau):

    IDAC3 -> LPo     +0,45 mV por codigo   (x4/x16: 0,49 · x1/x1: 0,41)
    IDAC1 -> SUMo    -5,24 mV por codigo
    IDAC1 -> LPo    +17,79 mV por codigo   =>  LPo/SUMo = -3,40

IDAC2 no esta medido DIRECTAMENTE todavia, pero se despeja de la campana:
dos pares de visitas del mismo par de ganancia, con el mismo par lento y
distinto IDAC2, dan **+44,2 y +46,1 mV/codigo**.  La config dice -150, o sea
que esta mal en magnitud Y EN SIGNO.  El signo importa porque la guarda de
SUMo elige la direccion del paso grueso con el signo de COARSE_SLOPE_UV: si
esta invertido, la guarda empuja SUMo para el lado equivocado.  Pendiente de
confirmar con un escalon controlado en la placa.

Las dos etapas tienen retardo: el acople de 680 uF da tau ~ 40 s al camino
lento, y la etapa LP responde mas rapido (el sondeo de IDAC3 asentaba en
~75 s).  Ambos son parametros.

Uso:
    python lab/sim/simulador_lazo.py            valida contra la placa
    python lab/sim/simulador_lazo.py --escenarios
"""
import argparse
import ctypes
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CYD = os.path.join(AQUI, '..', '..', 'src', 'firmware', 'psoc',
                   'AcondicionamientoAnalogico.cydsn')

# Indices de ControlConfig (mismo orden que el enum del firmware).
CP = {'PGA': 0, 'PGAOUT': 1, 'PERIOD_MS': 4, 'TAU_MS': 5, 'KP_NUM': 6,
      'KP_DEN': 7, 'DEADBAND_UV': 8, 'FINE_STEP': 10, 'RESCUE_STEP': 11,
      'RESCUE_MS': 12, 'SUM_BAND_UV': 13, 'COARSE_STEP': 14,
      'FINE_SLOPE_UV': 15, 'COARSE_SLOPE_UV': 16, 'OPA_TARGET_UV': 20,
      'VALID_LOW_UV': 27, 'VALID_HIGH_UV': 28, 'MARGIN_UV': 29,
      'FINE_LIMIT': 34, 'COARSE_LIMIT': 35, 'HOLD_UV': 36, 'FINE_MID': 37,
      'COARSE_MS': 38, 'SETTLED_MS': 40, 'SETTLED_BAND_UV': 41,
      'WAKE_COUNT': 42, 'RECENTER_UV': 45, 'RECENTER_MS': 46}


def cargar(recompilar=False):
    dll = os.path.join(AQUI, 'lazo.dll')
    if recompilar or not os.path.exists(dll):
        import subprocess
        r = subprocess.run(
            ['gcc', '-O2', '-shared', '-o', dll, os.path.join(AQUI, 'shim.c'),
             os.path.join(CYD, 'control_config.c'), '-I', CYD],
            capture_output=True, text=True)
        if r.returncode:
            raise SystemExit('no compila:\n' + r.stderr)
    d = ctypes.CDLL(dll)
    d.sim_get.restype = ctypes.c_int32
    d.sim_fine.restype = ctypes.c_int16
    d.sim_coarse.restype = ctypes.c_int16
    d.sim_slope.restype = ctypes.c_int32
    d.sim_rescue_step.restype = ctypes.c_int16
    d.sim_defaults()
    return d


class Planta(object):
    """Modelo de primer orden de la cadena, en microvoltios.

    SUMo y LPo persiguen su valor de regimen con sus propias constantes de
    tiempo.  Los offsets son lo que distingue un par de ganancia de otro: se
    ajustan para que el punto de reposo coincida con el medido en la placa.
    """

    def __init__(self, off_sum=0.0, off_lp=0.0,
                 b_fine=450.0, a_lp=-3.40, c_coarse=45000.0,
                 s_idac1=-5240.0, s_idac0=-600.0, coarse_a_sum=20000.0,
                 tau_slow=40.0, tau_lp=25.0, ruido=0.0):
        self.off_sum, self.off_lp = off_sum, off_lp
        self.b_fine, self.a_lp, self.c_coarse = b_fine, a_lp, c_coarse
        self.s_idac1, self.s_idac0 = s_idac1, s_idac0
        self.coarse_a_sum = coarse_a_sum
        self.tau_slow, self.tau_lp = tau_slow, tau_lp
        self.ruido = ruido
        self.sumo = 0.0
        self.lpo = 0.0
        self._sem = 12345

    def _rnd(self):
        # Ruido reproducible sin depender de la libreria del sistema.
        self._sem = (1103515245 * self._sem + 12345) & 0x7FFFFFFF
        return (self._sem / float(0x7FFFFFFF) - 0.5) * 2.0

    def objetivo(self, i0, i1, i2, i3):
        sumo = (self.off_sum + self.s_idac0 * i0 + self.s_idac1 * i1
                + self.coarse_a_sum * i2)
        lpo = self.off_lp + self.a_lp * sumo + self.b_fine * i3 + self.c_coarse * i2
        return sumo, lpo

    def avanzar(self, dt, i0, i1, i2, i3):
        s_ss, l_ss = self.objetivo(i0, i1, i2, i3)
        self.sumo += (s_ss - self.sumo) * (1.0 - pow(2.718281828, -dt / self.tau_slow))
        self.lpo += (l_ss - self.lpo) * (1.0 - pow(2.718281828, -dt / self.tau_lp))
        if self.ruido:
            return (self.sumo + self._rnd() * self.ruido,
                    self.lpo + self._rnd() * self.ruido)
        return self.sumo, self.lpo


def correr(d, planta, i0, i1, fine0, coarse0, segundos=1200.0, dt=3.0,
           forzar_s=0, traza=False):
    """Corre el PI real contra la planta y devuelve la trayectoria."""
    d.sim_pi_reset(ctypes.c_int16(fine0), ctypes.c_int16(coarse0))
    if forzar_s:
        d.sim_force(ctypes.c_uint32(0), ctypes.c_uint32(int(forzar_s * 1000)))
    planta.sumo, planta.lpo = planta.objetivo(i0, i1, coarse0, fine0)
    filas = []
    t = 0.0
    while t < segundos:
        t += dt
        fine, coarse = d.sim_fine(), d.sim_coarse()
        sumo, lpo = planta.avanzar(dt, i0, i1, coarse, fine)
        lpv = d.sim_valid(ctypes.c_int32(int(lpo)))
        sumv = d.sim_valid(ctypes.c_int32(int(sumo)))
        d.sim_step(ctypes.c_uint32(int(t * 1000)), ctypes.c_int32(int(lpo)),
                   ctypes.c_int(lpv), ctypes.c_int32(int(sumo)),
                   ctypes.c_int(sumv))
        filas.append((t, sumo / 1000.0, lpo / 1000.0, d.sim_fine(),
                      d.sim_coarse(), d.sim_holding(), d.sim_slope()))
        if traza and int(t) % 60 < dt:
            print('   %5.0fs SUMo=%7.1f LPo=%8.1f  I2=%4d I3=%5d hold=%d slope=%s'
                  % (t, sumo / 1000.0, lpo / 1000.0, d.sim_coarse(),
                     d.sim_fine(), d.sim_holding(), d.sim_slope()))
    return filas


def resumen(filas, n=20):
    cola = filas[-n:]
    lp = [f[2] for f in cola]
    return {'LPo': lp[-1], 'pp': max(lp) - min(lp), 'IDAC3': cola[-1][3],
            'IDAC2': cola[-1][4], 'hold': cola[-1][5], 'slope': cola[-1][6]}


def validar(d):
    """Compara el simulador contra puntos medidos en la placa.

    Si no reproduce lo observado, el modelo no sirve para decidir nada y hay
    que decirlo antes de sacar conclusiones con el."""
    print('=' * 70)
    print('VALIDACION contra la placa (campana del 2026-09-26)')
    print('=' * 70)
    casos = [
        # par, off_sum, off_lp ajustados al reposo medido, y lo observado
        ('x4/x16 CONTROL', dict(off_sum=-4700.0, off_lp=-30000.0),
         dict(LPo=-2.3, IDAC3=62)),
        ('x8/x8  MEMORIA', dict(off_sum=-34000.0, off_lp=130000.0),
         dict(LPo=26.6, IDAC3=-231)),
    ]
    for nombre, par, obs in casos:
        planta = Planta(**par)
        filas = correr(d, planta, 0, 0, 0, 0, segundos=1500.0, forzar_s=30)
        r = resumen(filas)
        print('%-16s simulado LPo=%7.1f mV IDAC3=%5d   |   placa LPo=%6.1f IDAC3=%5d'
              % (nombre, r['LPo'], r['IDAC3'], obs['LPo'], obs['IDAC3']))
    print()
    print('El modelo es de primer orden y IDAC2 no esta medido: sirve para')
    print('comparar MECANISMOS (fira o no fira el descargue, se clava o no el')
    print('vernier), no para predecir un numero exacto.')
    print()


def escenarios(d):
    print('=' * 70)
    print('ESCENARIO 1 - el descargue del vernier, se dispara?')
    print('=' * 70)
    print('Punto tipico de los pares fragiles: LPo asienta fuera de HOLD')
    print('(25 mV) pero dentro de la banda muerta (45), que es donde el')
    print('firmware NO ejecuta el descargue porque vive en la rama holding.')
    print()
    planta = Planta(off_sum=-34000.0, off_lp=130000.0)
    filas = correr(d, planta, 0, 0, 0, 0, segundos=2400.0, forzar_s=30)
    r = resumen(filas)
    i2 = [f[4] for f in filas]
    print('  resultado: LPo=%.1f mV  IDAC3=%d  IDAC2=%d  holding=%d'
          % (r['LPo'], r['IDAC3'], r['IDAC2'], r['hold']))
    print('  IDAC2 se movio %d veces en toda la corrida'
          % sum(1 for k in range(1, len(i2)) if i2[k] != i2[k - 1]))
    print('  pendiente que el lazo MIDIO sola: %s uV/codigo (config dice %d)'
          % (r['slope'], d.sim_get(CP['FINE_SLOPE_UV'])))
    print()
    print('=' * 70)
    print('ESCENARIO 2 - sensibilidad a HOLD_UV')
    print('=' * 70)
    print('Si el descargue solo corre dentro de HOLD, ensanchar HOLD deberia')
    print('alcanzar para que corra.  Es la forma MAS BARATA de probar la')
    print('hipotesis: un parametro, sin tocar codigo.')
    print()
    print('  %-10s %10s %8s %8s %s' % ('HOLD_UV', 'LPo_mV', 'IDAC3', 'IDAC2', 'holding'))
    base = d.sim_get(CP['HOLD_UV'])
    for hold in (25000, 35000, 44000):
        d.sim_set(CP['HOLD_UV'], ctypes.c_int32(hold))
        planta = Planta(off_sum=-34000.0, off_lp=130000.0)
        r = resumen(correr(d, planta, 0, 0, 0, 0, segundos=2400.0, forzar_s=30))
        print('  %-10d %10.1f %8d %8d %d'
              % (hold, r['LPo'], r['IDAC3'], r['IDAC2'], r['hold']))
    d.sim_set(CP['HOLD_UV'], ctypes.c_int32(base))
    print()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--recompilar', action='store_true')
    ap.add_argument('--escenarios', action='store_true')
    ap.add_argument('--traza', action='store_true')
    a = ap.parse_args()
    d = cargar(a.recompilar)
    validar(d)
    if a.escenarios:
        escenarios(d)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
