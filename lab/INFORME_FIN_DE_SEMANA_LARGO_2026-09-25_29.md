# Informe del fin de semana largo — 25 al 29 de septiembre de 2026

## Resumen ejecutivo

Durante el fin de semana se cerró la instrumentación del banco, se midió la
autoridad real de los actuadores, se corrigieron varios falsos positivos de las
herramientas de campaña, se probó y descartó una hipótesis de control, se
consolidó el camino de captura de ruido y se ejecutó el experimento de emisión
ESP-NOW simultánea a la adquisición.

Los resultados principales son:

1. La limitación de las ganancias altas no es solamente de sintonía: varios
   repartos llevan etapas analógicas al riel. La regla que mejor se sostiene es
   usar PGA relativamente bajo y PGAout alto para una misma ganancia total.
2. La pendiente fina medida de IDAC3 es aproximadamente 450 uV/código y no
   escala con PGAout, coherente con que actúa después de esa etapa.
3. Cambiar el objetivo lento de SUM a OPA_SUM no mejoró los pares que fallaban;
   el A/B fue negativo y el cambio se revirtió.
4. El ensayo RF produjo 60 capturas completas de 250 lotes y cero lotes
   faltantes. En los cuatro puntos estables no se observó un incremento
   reproducible del RMS de 10–50 Hz atribuible a la transmisión.
5. La medición real del efecto de la SD sigue pendiente por una condición
   física: después de un reinicio manual, el PSoC responde pero informa
   `SD present=0`. El software necesario para recuperar lotes completos desde
   la SD ya quedó implementado en la variante I2C y probado en host.

## 1. Banco y calidad de evidencia

Se endureció el criterio de una visita válida. Una lectura repetida por la
telemetría ya no cuenta como una medición nueva; se exige edad válida, cantidad
mínima de muestras y cobertura temporal suficiente. Esto evita declarar
quietud con una única foto vieja cuyo pico a pico daba artificialmente cero.

También se dejó un banco unificado para campañas, con:

- confirmación de ganancia y estado de adquisición;
- puntos de operación y semillas auditables;
- reinicio del PSoC precedido por `stop` y verificación posterior;
- restauración de parámetros de operación;
- criterios básico y estricto separados;
- conservación de resultados resumidos y exclusión de series crudas pesadas.

La revisión estática de las herramientas encontró nueve riesgos capaces de
falsear campañas. Entre ellos: muestras duplicadas, taps inválidos, cruces de
cero en escalones, restauración incompleta, controles etiquetados como
asentados sin evidencia, CRC de volcados no validado y ausencia de identidad de
captura. Esos hallazgos guiaron las correcciones posteriores y explican por qué
no se reutilizaron sin más todos los resultados históricos.

## 2. Rescate del experimento de semillas

Se auditaron 88 visitas de dos campañas con defectos conocidos. Se rescataron
54 visitas (61 %), todas en códigos PGA bajos x1/x2/x4, para comparar MEMORIA
contra CONTROL. Las columnas de comportamiento —veredicto, tiempo de
estabilización, nota e IDAC final— son utilizables en ese subconjunto; las
columnas de origen/semilla/residuo se descartaron donde quedaron contaminadas.

En FRÍO y DESDE_X1, MEMORIA y CONTROL tuvieron mediana de estabilización de
2,0 s. En DESDE_ALTA, la comparación cruda dio 66,8 s para MEMORIA y 39,4 s
para CONTROL. No se interpretó como ventaja causal porque esa diferencia no era
el objetivo del rescate. Las 34 visitas de PGA alto no aportaron comparación:
además del control sembrado en parte de ellas, ninguna llegó a PASA.

## 3. Planta, actuadores y simulación

Se construyeron herramientas de escalón y una matriz de autoridad para los
cuatro IDAC sobre los cinco taps. Los hallazgos que quedaron en pie son:

- IDAC3 tiene una pendiente de régimen cercana a 0,45 mV/código.
- Esa pendiente se mantiene aproximadamente igual al cambiar PGAout, lo que
  confirma que IDAC3 se inyecta después de PGAout.
- IDAC2 actúa antes de PGAout y su efecto sobre LPo sí escala con esa ganancia.
- La pendiente gruesa configurada conserva el signo correcto. Cambiar sólo el
  signo rompe el lazo; la magnitud continúa siendo un parámetro sensible.
- El estimador instantáneo de pendiente del firmware subestima la pendiente de
  régimen y vuelve el PI más agresivo.
- Existe un caso muerto concreto: SUM fuera de banda con LPo válido pero
  desplazado. La guarda bloquea el PI fino aunque todavía haya autoridad para
  corregir LPo.

El simulador ejecuta el código C real del lazo mediante un shim de host. Sirvió
para separar errores de lógica de límites físicos, pero no reproduce saturación
analógica; por eso no se usó para certificar pares de ganancia alta.

## 4. Cambios de control probados

Se amplió de forma acotada la condición que permite descargar el vernier y se
preservó un punto de retorno: tag `bueno-20260926` y dos imágenes HEX archivadas.
La validación se concentró en no empeorar x4/x16 y x8/x16 antes de extender la
campaña.

También se probó regular el par lento contra OPA_SUM en vez de SUM. El resultado
fue negativo:

| Par | Línea base | Con OPA_SUM |
|---|---:|---:|
| x16/x16 | 0/6, siempre aprendiendo | LPo -266,6 mV |
| x32/x4 | 0/6 | LPo -273,8 mV |
| x16/x8 | 0/6 | LPo -269,1 mV |
| x4/x16 | 5/6 | LPo -29,6 mV |

Los tres pares fallidos siguieron contra el riel. El cambio fue inocuo para el
control, pero inútil, y se revirtió. Esto descartó que el problema principal
fuera simplemente elegir el tap equivocado como objetivo.

## 5. Ganancias usadas para el ensayo RF

La campaña RF final se ejecutó sólo sobre el conjunto previamente demostrado
estable:

- x4/x16;
- x4/x24;
- x4/x32;
- x8/x16.

x4/x50 se había medido antes de corregir la selección. Sus 12 capturas se
conservan como exploratorias, pero no se usa como evidencia de estabilidad: la
campaña de control previa no sostuvo quietud en ese punto.

## 6. Experimento de transmisión durante la medición

### Protocolo

En condición RF se arranca `rftest` antes de `startwait`. El ESP32 transmite
tramas ESP-NOW de 200 bytes cada 20 ms durante toda la captura de 250 lotes
(7.500 muestras a 2.604 Hz). Al terminar la adquisición se corta RF y recién
entonces se vuelcan los datos por USB. Por tanto, el ensayo mide transmisión y
adquisición simultáneas; el transporte posterior de los datos no contamina la
ventana medida.

Cada repetición usa el orden BASE–RF–RF–BASE. Los dos BASE extremos sirven para
estimar la deriva durante el bloque. Antes de la campaña, una prueba corta
confirmó 150 tramas emitidas en 3 s y cero fallos.

### Integridad

- 48/48 corridas nuevas válidas en las cuatro ganancias estables.
- 12/12 corridas exploratorias válidas en x4/x50.
- 60 archivos, todos con exactamente 250 lotes.
- 0 lotes faltantes.
- Tres bloques ABBA por punto; seis capturas BASE y seis RF por ganancia.

### Resultado pareado por bloque

La tabla informa la mediana de los tres cocientes `RF/BASE` pareados. Entre
paréntesis figura el rango observado entre bloques.

| Par | RMS 10–50 Hz RF/BASE | RMS banda ancha RF/BASE |
|---|---:|---:|
| x4/x16 | 1,09 (0,82–1,89) | 1,00 (0,99–2,48) |
| x4/x24 | 1,00 (0,97–2,78) | 1,17 (0,92–4,56) |
| x4/x32 | 0,85 (0,81–0,94) | 0,95 (0,56–1,44) |
| x8/x16 | 0,09 (0,07–1,35) | 0,11 (0,10–0,98) |
| x4/x50, exploratorio | 1,00 (0,94–1,11) | 1,37 (1,29–1,54) |

### Interpretación

No aparece un incremento reproducible en 10–50 Hz sobre los puntos estables.
Los valores menores que uno no significan que la radio quite ruido: muestran
que la señal de entrada cambió bruscamente dentro de algunos bloques y dominó
la diferencia. Ejemplos extremos incluyen transiciones de un RMS casi de piso
a cientos o miles de cuentas entre capturas consecutivas.

El único patrón consistente fue el aumento de banda ancha en x4/x50, con
mediana 1,37 veces BASE. Como x4/x50 no demostró estabilidad de control, esto
queda como indicio y no como conclusión de diseño.

Con estos datos no se puede afirmar dependencia del ruido RF con la ganancia.
Sí se puede afirmar que, en los puntos estables ensayados y bajo el ruido de
entrada presente, la transmisión no produjo una penalización reproducible en
la banda útil de 10–50 Hz. Una cuantificación más fina requiere repetir con la
entrada terminada o una fuente estable, para que el movimiento ambiental no
oculte una perturbación pequeña.

Datos: `lab/ruido_antena_20260928/`; resumen:
`lab/ruido_antena_20260928/resumen.csv`.

## 7. Búsqueda de ganancias mayores

Después del ensayo RF se buscaron puntos por encima de la mayor ganancia total
estable demostrada (128). Estas pruebas se hicieron **sin RF**: primero había
que demostrar que el lazo podía estabilizarlas antes de contaminar la prueba
con transmisión.

| Par | Ganancia total | Resultado sin RF | Alcance |
|---|---:|---|---|
| x4/x48 | 192 | FALLA | 0/1 visita; LPo pp final 98,3 mV |
| x8/x24 | 192 | FALLA | 0/1 visita; sin `t_estable` tras 1260 s |
| x8/x32 | 256 | FALLA/APRENDIENDO | 0/6 visitas en frío, desde x1 y desde alta |
| x16/x16 | 256 | FALLA histórica | 0/6; siempre aprendiendo, LPo -266,6 mV |

x8/x32 agotó la matriz completa: memoria y control en frío, desde x1/x1 y
desde ganancia alta. Las tres visitas con memoria terminaron en FALLA y las
tres de control siguieron APRENDIENDO hasta agotar la ventana; ninguna produjo
un `t_estable`. Por tanto, ninguno de los puntos nuevos se habilitó para RF y
el mayor nivel que conserva evidencia de estabilidad sigue siendo ganancia
total 128 (x4/x32 y x8/x16).

Datos: `lab/campana_altas_20260929/`,
`lab/campana_altas_x8x24_20260929/` y
`lab/campana_altas_x8x32_20260929/`.

## 8. Experimento de SD

La campaña inicial de 250 lotes no activaba el almacenamiento real del PSoC:
la RAM admite hasta 512 lotes. Por eso `sdstress` no equivalía a medir el
drenaje real y esos resultados no se consideran válidos para cuantificar SD.

Se implementó la recuperación de lotes completos con `sdread`:

- salida `#SDREAD` con las 30 muestras de 10 bytes por lote;
- implementación portada y compilada en la variante activa I2C;
- parser de host que exige secuencia completa y 600 caracteres hex por lote;
- 12/12 pruebas unitarias del analizador aprobadas;
- firmware I2C compilado y cargado; `probe psoc=1` verificado.

Se hizo además un `psocreset` manual. El PSoC reinició, informó estado IDLE y
respondió a `probe`, pero antes y después del reinicio devolvió:

```
SD status=0x00 present=0 type=0 selftest=0
```

Por tanto, no se ejecutó una captura larga fingiendo que la SD estaba activa.
El pendiente es físico: insertar o reconectar una tarjeta reconocida y repetir
con más de 512 lotes, seguido por lectura `sdread` completa.

## 9. Verificaciones y commits clave

Verificaciones finales realizadas:

- firmware ESP32 I2C `slave2`: compilación PlatformIO exitosa;
- enlace ESP32–PSoC: `probe psoc=1`;
- emisión ESP-NOW: 150 envíos, 0 fallos en la prueba corta;
- suite de host: 63/63 pruebas unitarias;
- campaña RF: 60/60 archivos completos, 0 lotes faltantes.
- ganancias mayores: x8/x32 completó 6/6 visitas, 0 estables; x4/x48 y
  x8/x24 fallaron su primera visita y no se expusieron a RF.

Commits de referencia:

- `9e6a10f8`: banco unificado y controles del instrumento;
- `4023c618`: pendiente real de IDAC3 y efecto en el lazo;
- `a77622d8`: secuencia y verificación de `psocreset`;
- `45411c20`: simulador del lazo con código C real;
- `77e0aa10`: matriz de autoridad de los cuatro IDAC;
- `0285b43d`: A/B de OPA_SUM, resultado negativo y reversión;
- `1c441cb4`: espera correcta de la captura de ruido;
- `93500f0c`: validación de lotes completos leídos desde SD;
- `764126f` (submódulo ESP32): salida completa `sdread` en firmware I2C;
- `4df0092f`: repositorio principal apuntando a la versión I2C corregida.
- `8ed20435`: campaña reproducible BASE/RF y separación explícita del
  diagnóstico SD sintético.

## 10. Estado al cierre

Queda funcional y verificado el banco para campañas de control y para comparar
BASE contra transmisión RF simultánea. El ensayo RF está terminado y sus datos
están íntegros, aunque el ruido ambiental limita la sensibilidad de la
comparación. No se encontró un punto estable por encima de ganancia total 128.
El ensayo SD queda preparado de extremo a extremo en software, pero no puede
cerrarse hasta que el hardware detecte la tarjeta.

El próximo paso mínimo y falsable es: conectar una SD reconocida, confirmar
`present=1`, capturar más de 512 lotes y exigir que `sdread` reconstruya todas
las secuencias antes de calcular cualquier RMS.
