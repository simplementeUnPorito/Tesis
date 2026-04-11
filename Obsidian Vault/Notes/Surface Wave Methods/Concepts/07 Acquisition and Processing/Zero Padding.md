---
name: Zero Padding
description: Técnica de procesamiento que añade ceros al final de una señal antes de la FFT para aumentar la resolución frecuencial aparente del espectro — usada en [[MASW Method|MASW]] para interpolar el panel f-k y estimar con mayor precisión el pico de [[Phase Velocity|velocidad de fase]] a cada frecuencia
type: reference
---

# Zero Padding — Relleno con Ceros

> [!CONCEPT] Definición
> El **zero padding** (relleno con ceros) es una técnica de procesamiento digital que consiste en añadir muestras de valor cero al final de una señal de longitud $N$ antes de calcular su DFT, extendiendo artificialmente la secuencia a $N' > N$ puntos (típicamente $N' = 2N$ o $N' = 4N$ para usar FFT eficientemente). El efecto en el dominio espectral es una **interpolación** del espectro continuo en más puntos frecuenciales: la resolución frecuencial verdadera $\Delta f = 1/T$ (donde $T = N \Delta t$ es la duración real de la señal) no cambia, pero la DFT de longitud $N'$ evalúa el espectro en $N'/2$ frecuencias con espaciado $\Delta f' = 1/(N' \Delta t) = \Delta f / (N'/N)$. En términos matemáticos, el zero padding equivale a **sincinterpolación** del espectro. En [[MASW Method|análisis MASW]], el zero padding se aplica tanto en el dominio temporal (para interpolar el espectro de amplitud de cada traza) como en el dominio espacial (para interpolar el panel $f$-$k$), permitiendo localizar con mayor precisión el pico de [[Phase Velocity|velocidad de fase]] $\hat{V}_R(f)$ a cada frecuencia sin aumentar el número de mediciones de campo.
>
> — Foti et al. (2018), §3.4.1, pp. 147–152; Proakis & Manolakis (2006), §8.7.

## Efecto en el panel f-k

En [[MASW Method|MASW]] 2D, el zero padding espacial extiende el arreglo de $N$ [[Geophone|geófono]] a $N_{zp}$ puntos antes de la DFT espacial:

- **Sin zero padding**: $N_k = N/2$ frecuencias espaciales, resolución $\Delta k = 2\pi/D$ (apertura del arreglo)
- **Con zero padding (×4)**: $4N_k$ frecuencias espaciales, resolución aparente $\Delta k' = \Delta k/4$

La resolución verdadera no mejora (el criterio de Rayleigh $\Delta k_{min} = 2\pi/D$ no cambia), pero la localización del máximo del panel $f$-$k$ se hace más precisa, reduciendo el error de cuantización en la estimación de $V_R(f)$ de $\pm \Delta k/2$ a $\pm \Delta k'/2 = \pm \Delta k/8$.

## Regla práctica para [[MASW Method|MASW]]

Para el análisis $f$-$k$ de un arreglo de $N$ [[Geophone|geófono]]:
- **Dominio temporal**: rellenar hasta $N' = 2^p$ donde $2^p \geq 4N_t$ (al menos 4× la longitud original)
- **Dominio espacial**: rellenar hasta $N_{zp} = 8N$ o más para obtener interpolación suave del panel

El zero padding no introduce información nueva — solo facilita la interpolación. La mejora en la estimación de $V_R(f)$ es válida siempre que el pico en el panel $f$-$k$ sea la componente dominante (campo lejano, baja contaminación de [[Body Waves|ondas de cuerpo]]).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — zero padding en análisis [[MASW Method|MASW]] del sitio Memphis
> Foti et al. (2018, §3.4.1, Fig. 7.16) ilustran el efecto del zero padding en el análisis [[MASW Method|MASW]] del sitio Mud Island, Memphis. Con $N = 24$ [[Geophone|geófono]] a $\Delta x = 2$ m (apertura $D = 46$ m), la resolución espectral nativa es $\Delta k = 0.137$ rad/m, equivalente a $\pm 5$ m/s de incertidumbre en $V_R$ a 10 Hz. Con zero padding ×8 ($N_{zp} = 192$), la [[Dispersion Curve|curva de dispersión]] extraída del panel $f$-$k$ muestra una dispersión de ±0.6 m/s entre realizaciones — reducción ×8 del error de cuantización. La comparación con el perfil SCPT muestra acuerdo dentro del 5% en el rango 5–30 Hz tras la inversión — confirmando que la precisión mejorada por zero padding se traslada a mejor resolución del perfil $V_S(z)$.
>
> — Foti et al. (2018), §3.4.1, pp. 147–152, Fig. 7.16.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.4.1 — análisis espectral con zero padding en [[MASW Method|MASW]] |
| Proakis & Manolakis (2006), *Digital Signal Processing* | §8.7 — zero padding y sincinterpolación espectral |
