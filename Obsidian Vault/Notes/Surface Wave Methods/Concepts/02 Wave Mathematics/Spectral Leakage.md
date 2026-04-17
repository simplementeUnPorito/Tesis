---
name: Spectral Leakage
description: Distorsión espectral causada por el truncamiento de señales no periódicas en la DFT — genera lóbulos laterales que contaminan el espectro f-k de [[MASW Method|MASW]] y pueden enmascarar modos de Rayleigh de baja amplitud
type: reference
---

# Spectral Leakage — Fuga Espectral

> [!CONCEPT] Definición
> El **spectral leakage** (fuga espectral) es el fenómeno por el cual la energía de una componente frecuencial "se derrama" hacia frecuencias vecinas en el espectro DFT cuando la señal es **truncada** a una longitud finita. La DFT asume implícitamente que la señal es periódica dentro del intervalo de análisis $[0, T]$; si la señal no completa un número entero de ciclos en ese intervalo, los extremos del segmento son discontinuos y generan discontinuidades artificiales que producen lóbulos laterales (*side lobes*) en el espectro. Matemáticamente, el efecto de truncar la señal infinita $s(t)$ a una ventana $w(t)$ (e.g., ventana rectangular de duración $T$) se traduce en el espectro como una convolución:
> $$S_{ventaneada}(f) = S(f) * W(f)$$
> donde $W(f) = T \, \text{sinc}(\pi f T)$ es la transformada de la ventana rectangular, cuyo lóbulo principal tiene ancho $2/T$ y cuyos lóbulos laterales no decaen rápidamente (solo como $1/f$). En [[MASW Method|MASW]], el spectral leakage en el dominio espacio-temporal contamina el panel $f$-$k$ y puede enmascarar modos de [[Surface Waves|ondas superficiales]] de baja amplitud adyacentes a modos dominantes. La solución estándar es aplicar **ventanas de análisis** (Hann, Hamming, Tukey) que suavizan los extremos de la señal, reduciendo los lóbulos laterales a costa de una ligera pérdida de resolución frecuencial.
>
> — Foti et al. (2018), §3.3.5, pp. 135–138; Harris (1978), *Proc. IEEE* 66(1), 51–83.

## Efecto en el dominio f-k de [[MASW Method|MASW]]

La ventana temporal y espacial combina sus efectos en el panel 2D:

$$S_{ventaneado}(f, k) = S(f, k) * W_t(f) * W_x(k)$$

donde $W_t(f)$ es la transformada de la ventana temporal y $W_x(k)$ la de la ventana espacial. Los lóbulos laterales de $W_x(k)$ limitan la capacidad de **resolver modos cercanos** en [[Wavenumber|número de onda]]: dos modos con diferencia $\Delta k$ son distinguibles solo si $\Delta k > 2\pi/D$ (resolución de Rayleigh), donde $D$ es la apertura del arreglo.

## Ventanas de análisis estándar

| Ventana | Lóbulo principal (ancho) | Lóbulo lateral (dB) | Pérdida de resolución |
|---------|--------------------------|--------------------|-----------------------|
| Rectangular | $2/T$ | -13 dB | Ninguna |
| Hann | $4/T$ | -31.5 dB | ×2 |
| Hamming | $4/T$ | -42.5 dB | ×2 |
| Blackman | $6/T$ | -58 dB | ×3 |
| Tukey (α=0.5) | $\approx 3/T$ | ~-25 dB | ×1.5 |

La [[Hann Window|ventana de Hann]] (coseno elevado) es el estándar en procesamiento sísmico [[MASW Method|MASW]]: buen balance entre supresión de lóbulos (-31.5 dB) y resolución (pérdida ×2). La ventana [[Hamming Window|Hamming]] ofrece mayor supresión (-42.5 dB) al costo de lóbulos más amplios.

## Extensión al dominio espacial

El mismo fenómeno ocurre en el dominio espacial: el arreglo finito de $N$ [[Geophone|geófono]] sobre longitud $D$ actúa como una ventana rectangular espacial $W_x(x)$. El spectral leakage espacial limita la separación de modos en $k$ y puede generar **alias espaciales** si $\Delta x > \lambda_{\min}/2$ (condición de Nyquist espacial).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — efecto del ventaneo en el panel f-k del sitio Pisa
> Foti et al. (2018, §3.3.5, Figs. 3.14–3.15) comparan el panel $f$-$k$ del sitio Pisa obtenido con ventana rectangular vs. ventana Hann para un arreglo de 24 [[Geophone|geófono]] a $\Delta x = 2$ m. Con ventana rectangular, los lóbulos laterales del modo fundamental de Rayleigh a 10 Hz (dominante) contaminan la región del primer modo superior a 12 Hz, impidiendo su identificación. Con ventana Hann (lóbulos a -31.5 dB), el primer modo superior aparece claramente como cresta secundaria en el panel $f$-$k$, permitiendo su extracción para inversión multimodal. La diferencia cuantitativa: reducción de los lóbulos de -13 dB (rectangular) a -31.5 dB (Hann) — equivalente a que señales 37× más débiles puedan identificarse sin contaminación del modo dominante.
>
> — Foti et al. (2018), §3.3.5, pp. 135–138, Figs. 3.14–3.15.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.5 — ventaneo y spectral leakage en [[MASW Method|MASW]] |
| Harris, F.J. (1978), *Proc. IEEE* 66(1), 51–83 | Análisis comparativo de ventanas de análisis |
| Proakis & Manolakis (2006), *Digital Signal Processing* | §8 — DFT, FFT y efectos de ventaneo |
