# Validación nocturna consolidada — 2026-09-10

## Resumen ejecutivo

Se ejecutaron 69,7 minutos de pruebas automáticas continuas sobre hardware. La
prueba no se limitó a repetir un caso: el primer endurance descubrió una falla,
se corrigió la política de rescate, se verificó físicamente la contención y se
repitió una tanda larga con la versión final.

Resultado de la versión vigente:

- 10/10 campañas completas;
- 100/100 cambios funcionales PASS;
- secuencia por campaña: x1→x2→x4→x8→x16→x24→x32→x48→x50→x1;
- fase 1: 10/10 PASS, 62,53 ± 0,85 s;
- recorrido completo: 121,78 ± 1,93 s; p95 124,32 s; máximo 124,81 s;
- cambios normales: 4,80..9,01 s;
- 0 búsquedas amplias, 0 visitas de rescate a rieles y 0 abortos;
- 10 reintentos de escritura IDAC recuperados automáticamente;
- punto constante `[19,140,254,83]`.

Para 100/100 éxitos, el intervalo Wilson bilateral de 95 % de la probabilidad
de éxito por cambio es 96,3..100 %. Para 10/10 campañas, el intervalo es más
amplio, 72,2..100 %, por el tamaño muestral menor.

## Evolución de la prueba

### 1. Endurance original: falla descubierta

Archivo: `calibracion_nueva/dos_fases_endurance_15x_20260909.json`.

La tanda se detuvo deliberadamente a los 16,7 min. Después de seis campañas
completas, una lectura x2 apenas fuera del rango físico disparó la antigua
búsqueda de rescate. La malla rápida no respetó la memoria lenta, visitó extremos
y dejó IDAC2/IDAC3 en `-255`. Este resultado invalida esa política de rescate.

### 2. Guarda sin barrido: falla contenida

Archivos:

- `calibracion_nueva/dos_fases_guard_validation_20260909.json`;
- `calibracion_nueva/dos_fases_endurance_guarded_15x_20260909.json`;
- `RESULTADOS_ENDURANCE_DOS_FASES_2026-09-10.md`.

La malla quedó prohibida para puntos con historial. Una campaña corta dio 10/10.
Luego, en 15 campañas continuas:

- 14/15 campañas completas;
- 141/142 cambios intentados PASS, IC95 % Wilson 96,1..99,9 %;
- fase 1 15/15 PASS, 62,31 ± 0,70 s;
- un x2 persistió inválido;
- se restauró x1 sin barrer rieles;
- la campaña siguiente volvió a completar 10/10;
- 0 eventos de búsqueda amplia o riel.

La evidencia demostró que la guarda era segura, pero también que insistir en x2
durante tres verificaciones empeoraba ch2/ch3 por la memoria de la planta.

### 3. Recuperación neutra de fase 2: versión vigente

Archivos:

- `calibracion_nueva/dos_fases_endurance_recovery_10x_20260910.json`;
- `calibracion_nueva/dos_fases_endurance_recovery_10x_20260910_summary.json`;
- `RESULTADOS_ENDURANCE_RECOVERY_DOS_FASES_2026-09-10.md`.

Si una reverificación normal no recupera el punto, el programa vuelve a la
ganancia anterior, coloca únicamente IDAC2/IDAC3 en cero durante 30 s, reaplica
el historial y hace un último intento. No repite fase 1 ni explora códigos.
Si ese intento falla, restaura la configuración anterior y aborta el cambio.

La versión final completó 10/10 campañas y 100/100 cambios. La recuperación
excepcional no fue necesaria en esta tanda, por lo que su lógica se cubrió además
con tres pruebas unitarias: recuperación en segunda lectura, recuperación tras
descarga neutra y aborto seguro persistente.

## Estadística de la versión final

| PGAout | PASS | tiempo medio ± DE (s) | p95 (s) | LPo medio ± DE vs Vref (mV) | cinco taps válidos |
|---:|---:|---:|---:|---:|---:|
| x1 | 20/20 | 5,59 ± 1,51 | 8,94 | +2084,5 ± 0,5 | 10/20 |
| x2 | 10/10 | 5,45 ± 1,36 | 7,95 | +2220,3 ± 89,4 | 9/10 |
| x4 | 10/10 | 5,27 ± 1,28 | 7,11 | +2279,1 ± 18,6 | 0/10 |
| x8 | 10/10 | 5,86 ± 1,70 | 8,86 | +2189,7 ± 33,6 | 0/10 |
| x16 | 10/10 | 7,48 ± 1,70 | 8,99 | +2131,0 ± 16,5 | 0/10 |
| x24 | 10/10 | 5,68 ± 1,70 | 8,91 | +2140,1 ± 0,5 | 0/10 |
| x32 | 10/10 | 5,27 ± 1,30 | 7,13 | +2122,0 ± 0,7 | 0/10 |
| x48 | 10/10 | 6,27 ± 1,92 | 8,95 | +2141,8 ± 0,6 | 0/10 |
| x50 | 10/10 | 6,66 ± 2,00 | 9,01 | +2139,1 ± 0,8 | 0/10 |

x1 aparece 20 veces porque cada campaña comienza y termina allí. Las primeras
diez lecturas x1 tuvieron los cinco taps válidos; después del recorrido, los
taps internos ya no siempre eran válidos. No confundir esto con la salida LPo:
el criterio funcional y los 100 PASS exigen PGAgain, BPo y LPo válidos.

## Conclusiones y límites

1. La arquitectura temporal sí funciona: fase 1 se ejecuta una vez y cada
   cambio normal sólo ejecuta fase 2 en menos de 10 s.
2. La versión final no satura la salida funcional en la tanda de 100 cambios y
   no realiza búsquedas que lleven deliberadamente el circuito a rieles.
3. ch2/ch3 no permanecen legibles a ganancias altas y tampoco después de todos
   los retornos a x1. Es una limitación física/arquitectónica vigente.
4. LPo es legible pero está cerca del riel alto; no está centrado en Vref.
5. La escritura EEPROM de `[19,140,254,83]` fue aceptada previamente, pero aún
   falta verificar restauración mediante un power-cycle físico real.

## Reproducción

La campaña larga se ejecuta sin intervención con:

```powershell
python src/interfaces/python/autocalibracion_dos_fases.py calibrate-gains `
  --port COM8 `
  --gains 1,2,4,8,16,24,32,48,50,1 `
  --budget-s 180 `
  --campaign-repeats 10 `
  --keep-on-pass `
  --output lab/calibracion_nueva/endurance.json
```

El resumen estadístico reproducible se genera con:

```powershell
python src/interfaces/python/analizar_endurance_dos_fases.py `
  lab/calibracion_nueva/endurance.json `
  --json lab/calibracion_nueva/endurance_summary.json `
  --markdown lab/endurance_summary.md
```
