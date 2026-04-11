---
name: Convolution Theorem
description: Teorema que establece que la convolución en el dominio del tiempo equivale a la multiplicación en el dominio de la frecuencia — F{f*g}=F(f)·F(g) — base del procesamiento espectral de señales sísmicas y del modelado de la respuesta instrumental
type: reference
---

# Convolution Theorem — Teorema de Convolución

> [!CONCEPT] Definición
> El **teorema de convolución** establece que la [[Fourier Series|transformada de Fourier]] de la convolución de dos funciones es igual al producto de sus transformadas individuales:
> $$\mathcal{F}\{f(t) * g(t)\} = F(\omega) \cdot G(\omega)$$
> donde $F(\omega) = \mathcal{F}\{f(t)\}$ y $G(\omega) = \mathcal{F}\{g(t)\}$, y la convolución se define como:
> $$(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) \, g(t - \tau) \, d\tau$$
> El inverso también es válido: $\mathcal{F}\{f(t) \cdot g(t)\} = F(\omega) * G(\omega) / (2\pi)$ (convolución en frecuencia). En procesamiento sísmico, el teorema de convolución es fundamental porque:
> (1) **Modelo convolucional**: la señal sísmica registrada es la convolución de la fuente $s(t)$, la respuesta del medio $h(t)$ y la respuesta instrumental $i(t)$ — su deconvolución en el dominio de la frecuencia se convierte en simple división espectral; (2) **[[Spectral Leakage|ventaneo temporal]]**: truncar una señal = multiplicar por la ventana → el espectro resultante = convolución del espectro original con la transformada de la ventana; (3) **[[Cross-Correlation|correlación cruzada]]**: $R_{12}(\tau) = s_1(-\tau) * s_2(\tau)$ — en frecuencia: $\hat{R}_{12}(\omega) = S_1^*(\omega) \cdot S_2(\omega)$, base de la [[SASW Method|metodología SASW]] y [[Seismic Interferometry|interferometría sísmica]].
>
> — Foti et al. (2018), §3.3.1, pp. 124–128; Bracewell (2000), *The Fourier Transform and Its Applications*, §3.

## Aplicaciones en análisis de ondas superficiales

### Función de transferencia

El sistema de medición [[MASW Method|MASW]] puede modelarse como un sistema lineal:
$$u_{obs}(t) = s(t) * G(t, r) * i(t) + n(t)$$

donde $s(t)$ es la fuente, $G(t,r)$ es la función de Green del medio a distancia $r$, e $i(t)$ es la respuesta del geófono. En el dominio de la frecuencia:
$$U_{obs}(\omega) = S(\omega) \cdot G(\omega, r) \cdot I(\omega) + N(\omega)$$

La deconvolución fuente-receptor divide por $S(\omega)$ — razón por la que la [[Cross-Correlation|correlación cruzada]] entre dos receptores cancela $S(\omega)$ automáticamente.

### Correlación cruzada como convolución

$$R_{12}(\tau) = \int u_1(t) \, u_2(t + \tau) \, dt = u_1(-\tau) * u_2(\tau)$$

En frecuencia: $\hat{R}_{12}(\omega) = U_1^*(\omega) \cdot U_2(\omega)$ — extrae la diferencia de fase entre receptores, que es la base de la estimación de $V_R(\omega)$ en [[MASW Method|MASW]] (véase [[Cross-Correlation]]).

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — filtrado f-k por multiplicación espectral en [[MASW Method|MASW]]
> Park et al. (1999, *Geophysics* 64(3)) aplican el teorema de convolución en su algoritmo [[MASW Method|MASW]] para extraer la [[Dispersion Curve|curva de dispersión]]: transforman la sección de sismogramas al dominio $f$-$k$ (DFT 2D, esencialmente una convolución doble), identifican el modo dominante como el lóbulo de máxima amplitud, y reconstruyen la [[Dispersion Curve|curva de dispersión]] extrayendo el pico de amplitud a cada frecuencia. El filtrado de modos superiores se realiza directamente en el dominio $f$-$k$ (multiplicación por una máscara espectral = convolución en el dominio espacio-tiempo) — ilustrando el uso directo del teorema de convolución para separación modal. El procesamiento completo de 24 trazas a 256 puntos tarda < 0.1 s con FFT — ventaja computacional directa del teorema.
>
> — Research Database (Park et al. 1999); Foti et al. (2018), §3.3.1, pp. 124–128.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.1 — análisis espectral y modelo convolucional |
| Bracewell, R.N. (2000), *The Fourier Transform* | §3 — teorema de convolución y sus aplicaciones |
| Park et al. (1999), *Geophysics* 64(3) | Algoritmo [[MASW Method|MASW]] con transformada f-k |
