---
name: Dispersion Curve
description: Curva de dispersión experimental — [[Phase Velocity|velocidad de fase]] de Rayleigh como función de frecuencia, c_R(f); producto del procesamiento [[MASW Method|MASW]] y entrada a la inversión
type: reference
---

# Dispersion Curve — Curva de Dispersión Experimental

> [!CONCEPT] Definición
> La **curva de dispersión experimental** es el conjunto de pares $\{(f_i, c_R(f_i))\}$ que describe la [[Phase Velocity|velocidad de fase]] de las [[Rayleigh Waves|ondas de Rayleigh]] como función de la frecuencia, medida a partir del sismograma multicanal. Es el **producto central del [[Procesamiento de Señales|procesamiento]]** y la **entrada de la [[Inversión|inversión]]**: cada frecuencia $f_i$ corresponde a una [[Wavelength|longitud de onda]] $\lambda_i = c_R/f_i$ que aporta información sobre el perfil $V_S(z)$ a profundidades $z \approx \lambda_i/3$–$\lambda_i/2$ ([[Skin Depth]]). Se distingue de la [[Dispersion Relation|relación de dispersión]] teórica $\omega(k)$: la curva experimental contiene incertidumbre de medición, posibles contaminaciones de modos superiores y es discreta en frecuencia; la relación teórica es la función continua $c_R^{\text{teórica}}(\mathbf{m}, f)$ calculada para un modelo del subsuelo $\mathbf{m}$. La inversión ajusta la curva teórica a la experimental.
>
> — Foti et al. (2018), Cap. 4 (extracción), Cap. 6 (inversión), Cap. 7 (aplicaciones).

## Obtención experimental

La curva de dispersión se extrae del sismograma $u(x_j, t_n)$ mediante:

1. **Análisis f-k** ([[MASW Method|MASW]]): transformada de Fourier 2D → espectrograma $|U(\omega, k)|$ → cresta del modo fundamental → $c_R(f) = 2\pi f / k_{\text{cresta}}(f)$
2. **Tau-p / slant-stack**: suma coherente a lo largo de líneas de slowness → máximo de $|S(\tau, p)|$ → $c_R(f) = 1/p^*(f)$
3. **Espectro cruzado** ([[SASW Method|SASW]]): fase del espectro cruzado entre 2 receptores → $c_R(f) = 2\pi f \Delta x / \phi_{12}(f)$
4. **MOPA**: ajuste lineal fase-offset en el array → $c_R(f) = 2\pi f / \hat{k}(f)$ con incertidumbre directa

## Rango de frecuencias accesible

| Límite | Controlado por | Corresponde a |
|---|---|---|
| $f_{min}$ | Longitud total del arreglo $D$ | Profundidad máxima de investigación |
| $f_{max}$ | Espaciado de [[Geophone|geófono]] $\Delta x$ y fuente | Resolución superficial |

Las frecuencias fuera del rango $[f_{min}, f_{max}]$ tienen alta incertidumbre → no se usan en la inversión.

## Incertidumbre

La incertidumbre $\sigma_{c_R}(f)$ proviene de:
- Variabilidad entre disparos repetidos (fluctuación del campo de ondas)
- Anchura del pico espectral en f-k (inversamente proporcional a la apertura del arreglo)
- Presencia de modos superiores ([[Surface Wave Modes]]) que desplazan la cresta aparente
- [[Near-field Effect|Efectos de campo cercano]] en las frecuencias más bajas

## Modo fundamental vs. curva de velocidad aparente

Cuando hay superposición de modos ([[Mode Superposition]]), la cresta del espectrograma no corresponde a ningún modo individual sino a la **[[Phase Velocity|velocidad de fase]] aparente** — superposición ponderada por energía. Esto puede sesgarse respecto al modo fundamental real, produciendo errores en la inversión (hasta 50% en $V_S$ de capas profundas, Xu et al. 2006).

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — curva de dispersión como entrada de la inversión [[MASW Method|MASW]]
> **Paper 002 (Xia et al. 1999)** es el estudio canónico que establece el flujo procesamiento → curva de dispersión → inversión. La curva de dispersión experimental se extrae del espectrograma f-k de registros de 24 [[Geophone|geófono]] en Kansas (rango 5–50 Hz). El análisis de sensibilidad demuestra que cada punto $(f_i, c_R(f_i))$ de la curva contiene información principalmente de $V_S$ a profundidad $\approx \lambda_i/3$–$\lambda_i/2$. La inversión por mínimos cuadrados ajusta la curva teórica a la experimental minimizando el RMS: con modelo inicial de 3 capas, la curva teórica converge en <10 iteraciones y el perfil $V_S(z)$ resultante concuerda con borehole en error RMS < 15%.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, pp. 193–260 — extracción experimental |
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6, pp. 277–340 — uso en inversión |
| Xia et al. (1999), *Geophysics* 64(3) | Paper 002 — curva de dispersión como entrada de la inversión |
