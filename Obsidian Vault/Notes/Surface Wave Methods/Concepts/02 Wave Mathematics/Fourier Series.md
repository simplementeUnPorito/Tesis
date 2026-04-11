---
name: Fourier Series
description: Representación de señales periódicas como suma de componentes armónicas — base del análisis espectral en procesamiento sísmico y el fundamento de la transformada de Fourier discreta usada en [[MASW Method|MASW]]
type: reference
---

# Fourier Series — Serie de Fourier

> [!CONCEPT] Definición
> La **serie de Fourier** es la descomposición de una señal periódica $s(t)$ de período $T$ como suma discreta de funciones armónicas (senos y cosenos):
> $$s(t) = \sum_{n=-\infty}^{\infty} c_n \, e^{i 2\pi n t / T}, \qquad c_n = \frac{1}{T} \int_0^T s(t) \, e^{-i 2\pi n t / T} \, dt$$
> Los coeficientes $c_n$ forman el **espectro discreto** de amplitud y fase de la señal. La serie de Fourier es la base de la [[Fourier Series|transformada de Fourier discreta]] (DFT) utilizada en el análisis de señales sísmicas: la DFT discretiza el eje de tiempo ($t \to t_j = j \Delta t$) y asume periodicidad de la señal ventaneada — lo que introduce [[Spectral Leakage|spectral leakage]] cuando la señal no es periódica dentro del intervalo de análisis. La serie de Fourier en el dominio espacial (variable $x$, longitud de onda $\lambda = 2\pi/k$) conduce a la transformada $f$-$k$ utilizada en [[MASW Method|MASW]] para separar modos de ondas superficiales (Foti Ecs. 3.17–3.20). La condición de Nyquist ($F_s > 2f_{\max}$) surge del muestreo de la serie: la representación discreta genera réplicas del espectro a múltiplos de $F_s$, y solo se distinguen frecuencias hasta $F_s/2$.
>
> — Foti et al. (2018), §3.3.1–3.3.3, pp. 125–135; Bracewell (2000), *The Fourier Transform and Its Applications*.

## De la serie de Fourier a la transformada

| Señal | Dominio de la transformada | Espectro |
|-------|--------------------------|---------|
| Periódica continua | Frecuencias discretas $n/T$ | Serie de Fourier |
| Aperiódica continua | Frecuencias continuas $f$ | Transformada de Fourier (FT) |
| Periódica discreta (muestreada) | Frecuencias discretas hasta $F_s/2$ | DFT |
| Aperiódica discreta | Idem | DTFT |

En procesamiento sísmico se trabaja siempre con señales **discretas y finitas**, por lo que la DFT (implementada como FFT — Fast Fourier Transform) es el algoritmo central.

## Par de Fourier relevante para ondas superficiales

La transformada de Fourier convierte la convolución en multiplicación:
$$s(t) * h(t) \xrightarrow{\mathcal{F}} S(f) \cdot H(f)$$

Este es el **[[Convolution Theorem|teorema de convolución]]** — esencial para modelar la respuesta de sensores, ventanas temporales y filtros en [[MASW Method|MASW]].

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — análisis espectral de ondas Rayleigh en [[MASW Method|MASW]]
> Foti et al. (2018, §3.3.1, Fig. 3.6) presentan el análisis espectral de una señal de onda Rayleigh registrada a 30 m de la fuente en el sitio La Salle. El espectro de amplitud $|S(f)|$ muestra energía concentrada entre 4 y 40 Hz, con un pico dominante a 12 Hz correspondiente al modo fundamental de Rayleigh. La fase espectral $\angle S(f)$ crece linealmente con la frecuencia — pendiente $-2\pi r/V_R(f)$ — verificando la propagación dispersiva. La DFT implementada mediante FFT convierte los 2000 puntos temporales (2 s a 1000 Hz) en 1000 componentes espectrales de resolución $\Delta f = 0.5$ Hz. La comparación de fases entre receptores a distintas distancias permite extraer la [[Dispersion Curve|curva de dispersión]] $V_R(f)$ — el dato primario de [[MASW Method|MASW]] (véase §3.4.1).
>
> — Foti et al. (2018), §3.3.1, pp. 124–128, Figs. 3.6–3.7.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.1 — análisis espectral de ondas superficiales |
| Bracewell, R.N. (2000), *The Fourier Transform and Its Applications* | Teoría completa de la transformada de Fourier |
| Proakis & Manolakis (2006), *Digital Signal Processing* | DFT y FFT en procesamiento de señales |
