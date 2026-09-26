import unittest
from unittest import mock

from lab import barrido_total


class AsegurarAdquisicionTests(unittest.TestCase):
    def setUp(self):
        self.estado_anterior = barrido_total._est
        barrido_total._est = {}

    def tearDown(self):
        barrido_total._est = self.estado_anterior

    def test_taps_fuera_de_rango_pero_recientes_prueban_adquisicion(self):
        for i in range(5):
            base = barrido_total.K_TAP + 4 * i
            barrido_total._est[base] = 108_000 + i
            barrido_total._est[base + 1] = 0
            barrido_total._est[base + 2] = 500

        self.assertTrue(barrido_total._taps_frescos())

    def test_vacia_captura_anterior_antes_de_cebar(self):
        comandos = []
        frescura = iter((False, True))

        with mock.patch.object(
                barrido_total, '_cmd',
                side_effect=lambda comando, espera=1.5: comandos.append(
                    (comando, espera))), \
             mock.patch.object(
                 barrido_total, '_taps_frescos',
                 side_effect=lambda: next(frescura)), \
             mock.patch.object(barrido_total.time, 'sleep'):
            self.assertTrue(barrido_total._asegurar_adquisicion())

        self.assertEqual(
            comandos,
            [('ctl report', 0.2), ('clear', 0.5),
             ('startwait 5', 4.0), ('ctl report', 0.2)],
        )


if __name__ == '__main__':
    unittest.main()


class SondeoIntegradoTests(unittest.TestCase):
    """El sondeo de medibilidad vive DENTRO de la ventana de medicion.

    Antes era una pasada aparte en el experimento, y esa pasada hacia su
    propio cambio de ganancia.  El firmware emite el origen y la semilla del
    punto UNA sola vez, en el cambio; `_visitar` los borra al empezar; con dos
    cambios el evento caia en el primero y toda visita salia con origen None y
    residuo None -o sea, justo el dato que el experimento existe para medir-.
    """

    def setUp(self):
        self.estado_anterior = barrido_total._est
        barrido_total._est = {}

    def tearDown(self):
        barrido_total._est = self.estado_anterior

    def _correr(self, valido, mover_idac, sondeo_s=10.0, ventana=60.0):
        reloj = {'t': 0.0}
        paso = 2.0

        def foto():
            reloj['t'] += paso
            if mover_idac:
                barrido_total._est[barrido_total.K_IDAC] = int(reloj['t'])
            return {'t': None, 'estado': 0, 'banda': 0,
                    'tap': [0, 0, 0, 0, 0],
                    'valido': [1, 1, 1, 1, 1 if valido else 0]}

        with mock.patch.object(barrido_total, '_fijar_ganancia',
                               return_value=True), \
             mock.patch.object(barrido_total, '_foto', side_effect=foto), \
             mock.patch.object(barrido_total.time, 'sleep'), \
             mock.patch.object(barrido_total.time, 'time',
                               side_effect=lambda: reloj['t']):
            return barrido_total._visitar(2, 4, ventana, muestreo=paso,
                                          sondeo_s=sondeo_s)

    def test_sin_respuesta_y_sin_movimiento_es_inmedible(self):
        with self.assertRaises(barrido_total.Inmedible) as caja:
            self._correr(valido=False, mover_idac=False)
        self.assertEqual(caja.exception.validas, 0)
        self.assertEqual(caja.exception.movimientos, 0)

    def test_lazo_moviendose_merece_la_ventana_entera(self):
        # Un lazo que mueve sus IDAC esta buscando: cortarlo mide impaciencia.
        serie, _, _, _, ok = self._correr(valido=False, mover_idac=True)
        self.assertTrue(ok)
        self.assertGreater(len(serie), 10)

    def test_tap_que_responde_no_se_corta(self):
        serie, _, _, _, _ = self._correr(valido=True, mover_idac=False)
        self.assertGreater(len(serie), 10)

    def test_sin_sondeo_el_comportamiento_no_cambia(self):
        serie, _, _, _, _ = self._correr(valido=False, mover_idac=False,
                                         sondeo_s=0.0)
        self.assertGreater(len(serie), 10)


class ReconexionTests(unittest.TestCase):
    """Una re-enumeracion del USB no puede matar una campana de ocho horas.

    Ocurrio el 2026-09-25 a los 20 min de arrancar: ClearCommError devolvio
    PermissionError 13, el hilo lector salio, `_lector_error` quedo puesto
    para siempre y toda visita posterior levantaba esa misma excepcion aunque
    el puerto ya hubiera vuelto -y habia vuelto-.
    """

    def setUp(self):
        self.anterior = (barrido_total._est, barrido_total._vivo,
                         barrido_total._lector_error,
                         barrido_total._reconexiones, dict(barrido_total._puerto))
        barrido_total._est = {}
        barrido_total._vivo = True
        barrido_total._lector_error = None
        barrido_total._reconexiones = 0
        barrido_total._puerto.clear()

    def tearDown(self):
        (barrido_total._est, barrido_total._vivo, barrido_total._lector_error,
         barrido_total._reconexiones, puerto) = self.anterior
        barrido_total._puerto.clear()
        barrido_total._puerto.update(puerto)

    def test_el_lector_reabre_y_avisa_cuantas_veces(self):
        vidas = [
            [b'#CTL 0 17 111\n', OSError('ClearCommError failed')],
            [b'#CTL 0 17 222\n', OSError('fin')],
        ]

        class FalsoPuerto(object):
            def __init__(self):
                self.lineas = list(vidas.pop(0)) if vidas else [OSError('fin')]
                self.cerrado = False

            port = baudrate = timeout = dtr = rts = exclusive = None

            def open(self):
                pass

            def readline(self):
                if not self.lineas:
                    barrido_total._vivo = False
                    return b''
                x = self.lineas.pop(0)
                if isinstance(x, Exception):
                    if not vidas:
                        barrido_total._vivo = False
                    raise x
                return x

            def close(self):
                self.cerrado = True

        falso = mock.Mock()
        falso.Serial = FalsoPuerto
        with mock.patch.object(barrido_total, 'serial', falso), \
             mock.patch.object(barrido_total.time, 'sleep'):
            barrido_total._leer()

        self.assertEqual(barrido_total._reconexiones, 1)
        # Y lo que llego antes de la caida no se mezcla con lo de despues: el
        # ESP arranco de cero, su telemetria vieja es de otra vida del nodo.
        self.assertEqual(barrido_total._est.get(17), 222)

    def test_esperar_puerto_desbloquea_cuando_vuelve(self):
        barrido_total._lector_error = 'se perdio COM8'
        barrido_total._puerto['s'] = object()

        def devolver():
            barrido_total._lector_error = None

        with mock.patch.object(barrido_total.time, 'sleep',
                               side_effect=lambda _s: devolver()):
            barrido_total._esperar_puerto(limite_s=30.0)

    def test_esperar_puerto_se_rinde_si_no_vuelve(self):
        barrido_total._lector_error = 'se perdio COM8'
        with mock.patch.object(barrido_total.time, 'sleep'):
            with self.assertRaises(RuntimeError):
                barrido_total._esperar_puerto(limite_s=0.0)


class DistintasTests(unittest.TestCase):
    """Una lectura repetida no es una medida nueva.

    El firmware publica `now - ctl_stamp[i]` como edad del tap.  Ya calibrado
    baja el barrido a 20 s y los reportes a 30 s, asi que la misma medida sale
    una y otra vez.  Contar lineas en vez de medidas hacia que una etapa
    asentada -el caso que queremos premiar- diera pico a pico 0,0 mV por
    construccion.  Es la misma trampa que ya produjo 39 semillas falsas de 68.
    """

    @staticmethod
    def _f(t, valor, edad_ms):
        return {'t': t, 'tap': [0, 0, 0, 0, valor],
                'valido': [1, 1, 1, 1, 1], 'edad': [0, 0, 0, 0, edad_ms]}

    def test_la_misma_medida_publicada_varias_veces_cuenta_una(self):
        # Una sola medida tomada en t=0, reportada a los 0, 2, 4 y 6 s: la
        # edad crece justo lo que crece el reloj.
        serie = [self._f(0, 100, 0), self._f(2, 100, 2000),
                 self._f(4, 100, 4000), self._f(6, 100, 6000)]
        self.assertEqual(len(barrido_total._distintas(serie, 4)), 1)

    def test_medidas_nuevas_con_edad_CONSTANTE_cuentan_todas(self):
        # El caso que rompio el primer intento: si el barrido y el reporte van
        # al mismo ritmo, la edad sale igual en medidas DISTINTAS.  Pedir que
        # la edad bajara perdia siete de ocho.
        serie = [self._f(t * 20.0, 100 + t, 300) for t in range(8)]
        self.assertEqual(len(barrido_total._distintas(serie, 4)), 8)

    def test_valor_repetido_con_medida_nueva_cuenta_dos_veces(self):
        # Quieto de verdad: dos medidas distintas que dan el mismo numero.
        # Tiene que distinguirse de la misma medida publicada dos veces.
        serie = [self._f(0, 100, 300), self._f(20, 100, 280)]
        self.assertEqual(len(barrido_total._distintas(serie, 4)), 2)

    def test_sin_edad_no_se_deduplica(self):
        # Conservador a proposito: antes que descartar una medida real, se
        # cuenta de mas.  Un banco que ya perdio datos por confiar no puede
        # permitirse un filtro que borre en silencio.
        serie = [{'t': 0, 'tap': [0, 0, 0, 0, 5], 'valido': [1] * 5}]
        self.assertEqual(len(barrido_total._distintas(serie, 4)), 1)


class VeredictoEstrictoTests(unittest.TestCase):
    """Series degeneradas que ya enganaron a este banco.

    Cada caso es un modo de falla real, no una hipotesis: la medida unica
    repetida, la quietud demasiado corta para significar algo, el clavado
    contra el riel y el punto en banda pero sin autoridad de actuador.  El
    simulacro encontro tres defectos antes de que costaran una noche de banco,
    asi que se queda.
    """

    @staticmethod
    def _f(t, lp, valido=1, edad=300, idac3=-100):
        return {'t': t, 'estado': 2, 'banda': 1 if valido else 0,
                'perfil': 1, 'uptime': 1000, 'idac': [5, 2, -5, idac3],
                'tap': [0, 0, 0, 0, lp], 'valido': [1, 1, 1, 1, valido],
                'edad': [0, 0, 0, 0, edad]}

    def _v(self, serie):
        return barrido_total._analizar(
            2, 4, serie, 1.0 if serie else None, None, 0, 240, True)

    def test_serie_vacia_no_revienta(self):
        self.assertEqual(self._v([])['veredicto_estricto'], 'FALLA')

    def test_una_medida_repetida_no_es_quietud(self):
        # Quince lineas de telemetria de UNA sola medida: el pico a pico da
        # 0,0 mV por construccion.  Ya produjo 39 semillas falsas de 68.
        serie = [self._f(t * 2.0, -3000, edad=t * 2000) for t in range(15)]
        v = self._v(serie)
        self.assertEqual(v['muestras_validas_LPo'], 1)
        self.assertEqual(v['veredicto_estricto'], 'FALLA')

    def test_quieto_poco_tiempo_no_alcanza(self):
        # Quieto solo los ultimos 40 s de una visita de 260: sobre una planta
        # de tau ~ 30-44 s eso es una constante de tiempo, no regimen.
        serie = [self._f(t * 2.0, -3000 if t * 2 > 220 else 90000)
                 for t in range(130)]
        self.assertEqual(self._v(serie)['veredicto_estricto'], 'FALLA')

    def test_quieto_el_tiempo_suficiente_pasa(self):
        serie = [self._f(t * 2.0, -3000 + (t % 3) * 100) for t in range(130)]
        v = self._v(serie)
        self.assertEqual(v['veredicto_estricto'], 'PASA')
        self.assertEqual(v['nota'], 'A')

    def test_con_el_barrido_lento_tambien_pasa(self):
        # Ya asentado el firmware barre cada 20 s: diez medidas son 180 s.  El
        # criterio tiene que valer en los dos regimenes, que es justo lo que
        # un numero fijo de muestras no puede hacer.
        serie = [self._f(t * 20.0, -3000 + (t % 2) * 50) for t in range(10)]
        self.assertEqual(self._v(serie)['veredicto_estricto'], 'PASA')

    def test_clavado_contra_el_riel_no_pasa(self):
        serie = [self._f(t * 2.0, 90000) for t in range(130)]
        v = self._v(serie)
        self.assertEqual(v['nota'], 'D')
        self.assertEqual(v['veredicto_estricto'], 'FALLA')

    def test_en_banda_pero_sin_autoridad_no_pasa(self):
        # LPo perfecto con IDAC3 a 240 de 255: la primera deriva termica se lo
        # lleva puesto.  Mirar donde quedo el ACTUADOR, no solo la salida.
        serie = [self._f(t * 2.0, -3000, idac3=-240) for t in range(130)]
        v = self._v(serie)
        self.assertEqual(v['nota'], 'A')
        self.assertTrue(v['fragil'])
        self.assertEqual(v['veredicto_estricto'], 'FALLA')
