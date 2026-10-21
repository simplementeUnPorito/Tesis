# Firmas de ruido y resta por software (2026-10-21)

Herramienta: `lab/firmas_ruido.py`. Firmas en `lab/firmas/` (`.npz` + `.json`
por fuente y configuración; índice `firmas.md`, figura `firmas.png`).

## Qué es una firma

Para cada fuente y configuración (tap, PGA, PGAout) se guardan:

- la **media** del brote alrededor de cada evento (−10 ms a ~0,92 del
  espaciado entre eventos, para no incluir el siguiente);
- las **componentes principales** de la variación entre eventos (hasta 8),
  con su varianza explicada;
- cuántas son **significativas**: las que superan el percentil 95 de la misma
  descomposición sobre la condición de referencia (PING o BASE) en las mismas
  posiciones (análisis paralelo, con varianza absoluta);
- la dispersión por muestra, la ganancia total y los directorios de origen.

Fuentes: escritura en la SD (por tap), transmisión ESP-NOW de 240 y 10 B (por
tap y ganancia del PGA), recepción, avisos I2C del PSoC y la baliza WiFi
(firma periódica de 102,4 ms, sin marcas de tiempo).

## Resta

`restar(x, posiciones, firma, modo=...)`, por evento:

| modo | qué ajusta | riesgo |
|---|---|---|
| `fija` | nada: resta la media (corrimiento ±2 muestras elegido en > 60 Hz) | ninguno, es lineal |
| `alta` | amplitud de media y componentes, solo sobre la parte > 60 Hz | bajo |
| `libre` | todo, en la banda completa | absorbe señal del geófono |

## Resultado (dejar-una-captura-afuera, `lab/firmas/evaluacion.md`)

Exceso de ruido eliminado = (antes − después)/(antes − referencia), en RMS.
Distorsión = RMS(resta(x+s) − resta(x) − s)/RMS(s), con s = paquetes de 20 Hz.

| Fuente | fija | alta + componentes | libre | distorsión de libre |
|---|---|---|---|---|
| **Escritura en la SD** | **88 %** (dist. 0) | **91 %** (dist. 0,2 %) | 88 % | 50 % |
| Transmisión 240 B (LPo) | 6 % | −90 % (empeora) | 7 % | 78 % |
| Transmisión 240 B (SEo) | 23 % | −21 % | 25 % | 85 % |
| Recepción | 17 % | 17 % (sin componentes significativas) | 21 % | 11 % |

Baliza (`lab/firmas/baliza.md`, W1c + W12e contra OFF):

| Plantilla | exceso 5-50 Hz | línea 9,77 Hz | distorsión |
|---|---|---|---|
| propia de cada captura | 24 % | 76 % | 27 % |
| de las otras capturas | 15 % | 42 % | 0 |

## Conclusión

- **La SD se resta**: su brote es repetible y con la plantilla fija se saca
  ~90 % del exceso sin tocar la señal. Después de rediseñar la placa, restar
  la firma residual de la SD es viable (las muestras escritas ya llevan
  marca).
- **La transmisión no se resta**: cada brote es distinto (sobre todo la
  duración del escalón de ~20 ms) y su energía es un escalón de baja
  frecuencia en la banda del geófono; lo que ajusta, se come la señal. Se
  evita (store-and-forward + `radiosil`) o se aísla.
- **La baliza** se resta solo en parte (la línea sí, la banda no) y con
  distorsión si la plantilla sale de la misma captura; `radiosil on 500` la
  saca entera (banda ×0,31).

Cuando cambie la placa: re-extraer con `python lab/firmas_ruido.py extraer
--todas` sobre las campañas nuevas (`campana_ruido.py --plan rf` y `sd`) y
evaluar con `evaluar --todas` y `baliza`.
