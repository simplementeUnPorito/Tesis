# Tres hallazgos del 2026-09-12 por la tarde, y dos retractaciones

## 1. RETRACTADO: no hay histéresis. Era falta de asentamiento

Durante la tarde afirmé que el mismo código de IDAC3 daba resultados opuestos
según de dónde se viniera, y lo presenté como histéresis.

**Es falso.** Repetido con esperas de 100 s por punto, o sea tres constantes de
tiempo, en vez de los 4 s originales:

| IDAC3 | subiendo | bajando | diferencia |
|---|---|---|---|
| −50 | −5.578,8 | −5.581,5 | −2,7 |
| −25 | −5.580,3 | −5.579,6 | +0,8 |
| 0 | −5.579,6 | −5.580,3 | −0,8 |
| +25 | +1.879,0 | +1.878,6 | −0,4 |
| +50 | +1.877,9 | +1.878,6 | +0,8 |
| +75 | +1.878,2 | +1.878,2 | 0,0 |

Peor diferencia: **3 mV sobre una excursión de 7.461**. Cero histéresis.

Lo que había visto con esperas de 4 s era el rezago de una cadena con τ de 30 s:
subiendo las lecturas van atrasadas hacia abajo y bajando hacia arriba, lo que se
ve **idéntico** a una histéresis sin serlo.

**Esto obliga a poner en duda el hallazgo de "el estado depende del camino"** del
2026-09-12 a la mañana, que se apoyaba en comparaciones con esperas cortas. Puede
seguir siendo cierto por otras razones, pero la evidencia que lo sostenía no
alcanza. Queda marcado como no demostrado.

## 2. La unidad del banco son CUENTAS del ADC, no microvolts

Elías preguntó cómo podía ser que un tap leyera −5.580 mV si todo el PSoC vive
entre 0 y 5 V. Tenía razón: ese número es imposible y no es una tensión.

Investigando salió el mecanismo del factor 19,9157 que `escala_banco.py` declaraba
sin explicar:

- El ADC en configuración ±2,5 V tiene **52.429 cuentas por volt**, o sea
  **19,073 µV por cuenta** (`ADC_CF_2V5_COUNTS_PER_VOLT` en el código generado).
- El firmware trabaja en cuentas y lo dice explícitamente en `calibration.c`:
  "el ADC entrega el nivel absoluto (unas 52429 cuentas/V en CF_2V5)".
- El lado de Python las llama `mean_uv`, o sea microvolts. **El nombre miente.**

El factor medido con tester, 19,9157, es un 4,4 % mayor que los 19,073 nominales,
y eso lo explica que Vdda real sea 4,826 V en vez de 5,0, un 3,5 % abajo.

**Consecuencias.** La escala está bien y la recta medida es correcta, así que no
hay que cambiar números. Lo que hay que cambiar son los nombres, y sobre todo hay
que dejar de imprimir tensiones extrapoladas fuera de la ventana: una lectura por
debajo de 880,4 mV de banco significa "el ADC llegó a su tope", no "el tap está a
−5,6 V".

## 3. El paso de IDAC3 es 800 a 2.000 mV por código, y por eso no sirve

Medido con esperas de 100 s, con PGA x50 y PGAout x4:

| IDAC3 | LPo |
|---|---|
| 0 | por debajo de la ventana |
| +5 | +1.854 mV |
| +10 | +1.879, riel |
| +15 en adelante | +1.879, riel |

La salida cruza **todo su recorrido útil**, unos 4.000 mV, entre los códigos 0 y
5. O sea entre 800 y 2.000 mV por código.

**No es que a IDAC3 le falte autoridad: le sobra tanto que no puede aterrizar
dentro de la ventana.** La banda útil mide uno o dos códigos. Eso corrige la
conclusión vieja de que "IDAC3 no sirve": sirve, pero es catorce veces demasiado
grueso.

### El valor de resistencia que corresponde

La tensión por código es la corriente por la resistencia, así que para pasos más
finos hace falta una resistencia más chica, en proporción directa.

| resistencia | mV por código | códigos útiles en la ventana | fondo de escala |
|---|---|---|---|
| 6.680 actual | 800 a 2.000 | 1 a 5 | ±204 V |
| 1.000 | 120 | ~33 | ±30 V |
| **470 recomendada** | **56** | **~70** | **±14 V** |
| 330 | 40 | ~100 | ±10 V |

**Recomendación: 470 Ω.** Da unos setenta códigos útiles, que es resolución de
sobra y hasta evita necesitar el vernier en esta etapa.

La preocupación por perder recorrido no aplica: con 470 Ω el fondo de escala son
catorce voltios, tres veces más de lo que la cadena puede recorrer físicamente.
Este actuador tiene tanto exceso que se puede dividir la resistencia por diez y
sigue sobrando.

Se prefiere 470 sobre 330 porque cuanto más chica la resistencia, más corriente
pide el actuador para el mismo efecto, y con IDAC2 ya se vio que trabajar cerca
del fondo de escala trae problemas.

### Qué verificar después del cambio

1. Que la banda útil quede donde se predice, unos setenta códigos.
2. Que el actuador sea **estable** en la zona donde va a trabajar, con
   `comparar_deriva_por_codigo.py`. Es lo que le falló a IDAC2 pasados los 180
   códigos y no se puede dar por sentado.
