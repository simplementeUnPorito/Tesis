---
name: Hamming Window
description: Ventana de análisis espectral con coeficientes (0.54, 0.46) que reduce los lóbulos laterales a -42.5 dB con pérdida ×2 de resolución frecuencial — variante de la ventana de Hann usada en análisis f-k de [[MASW Method|MASW]]
type: reference
---

# Hamming Window — Ventana de Hamming

> [!CONCEPT] Definición
> La **ventana de Hamming** es una [[Window Function|función de ventana]] espectral definida como:
> $$w_{Hamming}(n) = 0.54 - 0.46 \cos\!\left(\frac{2\pi n}{N-1}\right), \qquad 0 \leq n \leq N-1$$
> Sus coeficientes $(a_0 = 0.54, a_1 = 0.46)$ están optimizados para **minimizar el primer lóbulo lateral** en la transformada de Fourier de la ventana, logrando -42.5 dB de supresión frente a los -13 dB de la ventana rectangular. A diferencia de la [[Hann Window|ventana de Hann]] ($a_0 = 0.5, a_1 = 0.5$), los extremos de la ventana Hamming **no llegan a cero** ($w(0) = 0.08$, $w(N-1) = 0.08$) — lo que genera una pequeña discontinuidad en los bordes que produce lóbulos laterales que no decaen tan rápidamente ($\propto 1/f$ vs. $1/f^3$ para Hann), pero el lóbulo lateral *inmediato al principal* es más bajo (-42.5 dB vs. -31.5 dB de Hann). En [[MASW Method|MASW]], la ventana Hamming se usa cuando se requiere mayor supresión del primer lóbulo lateral para evitar la contaminación entre modos de [[Surface Waves|ondas superficiales]] con velocidades próximas, a costa de una pérdida de resolución ×2 respecto a la ventana rectangular (ancho del lóbulo principal = $4/T$ vs. $2/T$).
>
> — Harris (1978), *Proc. IEEE* 66(1), 51–83; Foti et al. (2018), §3.3.5, p. 137.

## Comparación Hamming vs. Hann

| Propiedad | Hann | Hamming |
|-----------|------|---------|
| Coeficientes | $(0.5, 0.5)$ | $(0.54, 0.46)$ |
| Valor en extremos | $0$ (cero exacto) | $0.08$ (no-cero) |
| Primer lóbulo lateral | -31.5 dB | -42.5 dB |
| Decaimiento de lóbulos | $\propto 1/f^3$ | $\propto 1/f$ |
| Ancho del lóbulo principal | $4/T$ | $4/T$ |
| Uso recomendado | Sísmica superficial estándar | Señales con modos muy próximos |

La ventana de Hamming es preferida cuando el primer lóbulo lateral es el problema (modos de Rayleigh con $\Delta k$ pequeño); la de Hann es mejor cuando se necesita que todos los lóbulos sean bajos (señal con amplitudes muy diferentes entre componentes lejanas).

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — ventaneo en análisis f-k multichannel [[MASW Method|MASW]]
> Park et al. (1999, *Geophysics* 64(3)) aplican la ventana de Hamming en el dominio temporal a cada traza del arreglo multicanal antes de la transformada $f$-$k$ en su algoritmo [[MASW Method|MASW]] original. La elección de Hamming sobre Hann se justifica porque los datos de campo muestran un primer modo superior muy próximo en [[Phase Velocity|velocidad de fase]] al modo fundamental (diferencia $\Delta V_R < 20\%$ en el rango 15–25 Hz) — condición donde el primer lóbulo lateral de Hann (-31.5 dB) podría confundir los modos. Con Hamming (-42.5 dB del primer lóbulo), la separación entre modos en el panel $f$-$k$ mejora lo suficiente para identificar el modo fundamental sin ambigüedad. Esta elección se volvió estándar en la implementación original del software SurfSeis (Park & Miller 1998).
>
> — Park et al. (1999), *Geophysics* 64(3), 800–808; Harris (1978), *Proc. IEEE* 66(1), 51–83.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Harris, F.J. (1978), *Proc. IEEE* 66(1), 51–83 | Definición y comparación de ventanas de análisis |
| Park et al. (1999), *Geophysics* 64(3), 800–808 | Uso en el algoritmo [[MASW Method|MASW]] original |
| Foti et al. (2018), *Surface Wave Methods* | §3.3.5 — ventaneo en procesamiento [[MASW Method|MASW]] |
