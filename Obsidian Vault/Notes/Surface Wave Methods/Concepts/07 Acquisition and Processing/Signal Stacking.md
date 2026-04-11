---
name: Signal Stacking
description: Suma coherente de múltiples disparos sísmicos para aumentar la relación señal-ruido S/N en ensayos MASW — mejora S/N en factor √N para ruido no coherente, esencial en sitios con alta actividad urbana o señales sísmicas débiles
type: reference
---

# Signal Stacking — Apilamiento de Señales

> [!CONCEPT] Definición
> El **signal stacking** (apilamiento de señales) es la suma coherente de $N$ realizaciones de la señal sísmica registradas bajo las mismas condiciones (misma posición de fuente y receptores, en diferentes disparos):
> $$s_{stack}(t) = \frac{1}{N} \sum_{i=1}^{N} s_i(t)$$
> Para señal determinista $S(t)$ y ruido aleatorio no correlacionado $n_i(t)$: $s_i(t) = S(t) + n_i(t)$. La suma produce:
> $$s_{stack}(t) = S(t) + \frac{1}{N}\sum_{i=1}^N n_i(t)$$
> La señal se suma coherentemente (misma amplitud $S(t)$ en todas las realizaciones), mientras el ruido se promedia con ganancia $\sim \sqrt{N}$ en términos de S/N. Por tanto:
> $$\text{SNR}_{stack} = \sqrt{N} \cdot \text{SNR}_{single}$$
> En [[MASW Method|análisis MASW]], el stacking permite registrar curvas de dispersión de calidad en sitios con alto ruido ambiental (zonas urbanas, proximidad a carreteras) donde un solo disparo produce S/N insuficiente para la extracción confiable del modo fundamental de Rayleigh. El procedimiento estándar es 3–8 disparos por posición, stacking en el dominio del tiempo antes del análisis $f$-$k$.
>
> — Foti et al. (2018), §3.4.1, pp. 147–152; Park et al. (1999), *Geophysics* 64(3).

## Stacking en el dominio de la frecuencia

Una alternativa al stacking temporal es el **stacking espectral** o *phase-weighted stacking*:
$$S_{stack}(f) = \left|\frac{1}{N}\sum_{i=1}^N e^{i\phi_i(f)}\right|^p \cdot \frac{1}{N}\sum_{i=1}^N |S_i(f)|$$

donde $\phi_i(f)$ es la fase de cada disparo. El factor de coherencia $|N^{-1}\sum e^{i\phi_i}|$ es 1 cuando todas las fases son iguales (señal pura) y tiende a 0 para fases aleatorias (ruido) — suprime más agresivamente el ruido incoherente que el stacking lineal.

## Condiciones para stacking efectivo

- **Repeatibilidad de la fuente**: la posición y energía de la fuente deben ser consistentes entre disparos
- **Estacionariedad del ruido**: el fondo de ruido debe tener propiedades estadísticas estables durante la adquisición
- **Sincronización temporal**: el momento exacto del disparo ($t_0$) debe ser consistente o correcto para alinear las trazas

En MASW con martillo, el **trigger** electrónico en el cabezal del martillo marca $t_0$ con precisión < 0.1 ms — condición esencial para que el stacking sea coherente a frecuencias > 50 Hz.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — mejora S/N por stacking en sitio urbano de Kansas
> Park et al. (1999, *Geophysics* 64(3), 800–808) demuestran el efecto del stacking en un ensayo MASW realizado a 50 m de una carretera concurrida en Kansas. Con un solo disparo, el panel $f$-$k$ muestra el modo fundamental de Rayleigh apenas visible sobre el ruido de tráfico a frecuencias < 12 Hz (S/N ≈ 2). Con 8 disparos apilados, la S/N mejora a $\approx 5.7 \approx \sqrt{8} \times 2$ — consistente con la predicción teórica. La curva de dispersión extraída del stack cubre el rango 4–40 Hz sin ambigüedad, permitiendo inversión hasta ~18 m de profundidad. Sin stacking, la inversión solo es confiable por encima de 12 Hz (profundidad < 8 m). El estudio concluye que 5–8 disparos son suficientes para la mayoría de sitios urbanos con ruido moderado.
>
> — Park et al. (1999), *Geophysics* 64(3), 800–808; Foti et al. (2018), §3.4.1.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.4.1 — apilamiento en adquisición MASW |
| Park et al. (1999), *Geophysics* 64(3), 800–808 | Stacking en MASW con ruido ambiental alto |
| Scherbaum (1996), *Of Poles and Zeros* | Teoría del stacking y mejora S/N |
