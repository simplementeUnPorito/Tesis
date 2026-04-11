---
name: Dirac Comb
description: Tren de deltas de Dirac III(t) = Σδ(t-nΔt) que modela el muestreo temporal discreto en adquisición sísmica — genera periodicidad espectral y aliasing cuando la señal contiene frecuencias por encima de Nyquist
type: reference
---

# Dirac Comb — Tren de Deltas (Shah Function)

> [!CONCEPT] Definición
> El **Dirac comb** (o *Shah function*) es la distribución periódica definida como suma infinita de [[Dirac Delta|deltas de Dirac]]:
> $$\mathrm{III}_{\Delta t}(t) = \sum_{n=-\infty}^{\infty} \delta(t - n\Delta t)$$
> donde $\Delta t$ es el intervalo de muestreo temporal. El **muestreo** de una señal continua $s(t)$ se modela como la multiplicación por el Dirac comb:
> $$s_s(t) = s(t) \cdot \mathrm{III}_{\Delta t}(t) = \sum_n s(n\Delta t) \, \delta(t - n\Delta t)$$
> La transformada de Fourier del Dirac comb es también un Dirac comb:
> $$\mathcal{F}\{\mathrm{III}_{\Delta t}(t)\} = F_s \cdot \mathrm{III}_{F_s}(f), \qquad F_s = 1/\Delta t$$
> Por el [[Convolution Theorem|teorema de convolución]], el espectro de la señal muestreada es la **convolución** del espectro continuo $S(f)$ con el comb de frecuencias:
> $$S_s(f) = F_s \sum_n S(f - n F_s)$$
> Esto genera **réplicas** del espectro a múltiplos de $F_s$. Si $S(f)$ contiene componentes con $|f| > F_s/2$ (frecuencia de Nyquist), las réplicas se solapan — produciendo **[[Spectral Leakage|aliasing]]** (solapamiento espectral irreversible). En adquisición [[MASW Method|MASW]], el criterio de Nyquist requiere $\Delta t < 1/(2f_{\max})$: para $f_{\max} = 100$ Hz se necesita $\Delta t < 5$ ms (es decir $F_s > 200$ Hz). La práctica estándar usa $F_s = 1000$–$2000$ Hz para registros MASW superficiales (Foti et al. 2018, §3.3.3).
>
> — Foti et al. (2018), §3.3.3, pp. 130–135; Bracewell (2000), *The Fourier Transform*, §5; Nyquist (1928).

## Extensión al dominio espacial

El muestreo espacial de un arreglo de $N$ geófonos a separación $\Delta x$ se modela con el Dirac comb espacial:
$$\mathrm{III}_{\Delta x}(x) = \sum_{n=0}^{N-1} \delta(x - n\Delta x)$$

Genera el espectro en número de onda con réplicas a múltiplos de $k_s = 2\pi/\Delta x$. El aliasing espacial ocurre cuando $k > k_s/2 = \pi/\Delta x$, equivalente a la condición $\Delta x < \lambda_{\min}/2$ — criterio de Nyquist espacial para MASW (ver sección 3.3.3 de Foti).

## Filtros antialiasing

| Dominio | Solución | Implementación |
|---------|---------|----------------|
| Temporal | Filtro antialiasing hardware (paso bajo) | Condensador RC antes del ADC |
| Temporal | Sobremuestreo + decimación digital | DSP en tarjeta de adquisición |
| Espacial | Diseño del arreglo: $\Delta x < \lambda_{\min}/2$ | Selección del espaciado entre geófonos |
| Espacial | Arreglo no uniforme (muestreo comprimido) | Geófonos en posiciones irregulares |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — aliasing espacial en MASW con arreglo 3 m
> Foti et al. (2018, §3.3.3, Fig. 3.11) ilustran el aliasing espacial en un ensayo MASW con $\Delta x = 3$ m: a 50 Hz, $\lambda_R \approx 200/50 = 4$ m (para $V_R = 200$ m/s en la capa superficial), de modo que $\Delta x > \lambda_{\min}/2 = 2$ m — incumpliendo el criterio de Nyquist. El panel $f$-$k$ muestra réplicas aliasadas que se solapan con el modo fundamental en la región $k > k_{Nyq} = \pi/3 \approx 1.05$ rad/m, produciendo picos espúreos de velocidad aparente entre 50 y 80 Hz. La solución correcta es usar $\Delta x \leq 1.5$ m (o descartar frecuencias $> f_{Nyq}$ en la inversión). Foti concluye que el aliasing espacial es la fuente más común de errores sistemáticos en análisis MASW de alta frecuencia con arreglos de geófonos espaciados > 2 m.
>
> — Foti et al. (2018), §3.3.3, pp. 130–135, Fig. 3.11.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.3 — muestreo y aliasing en MASW |
| Bracewell, R.N. (2000), *The Fourier Transform* | §5 — Shah function y muestreo |
| Nyquist, H. (1928), *Bell System Tech. J.* | Teorema de muestreo original |
