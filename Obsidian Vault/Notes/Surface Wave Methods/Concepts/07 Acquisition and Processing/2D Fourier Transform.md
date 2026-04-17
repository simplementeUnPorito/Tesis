---
name: 2D Fourier Transform
description: Transformada de Fourier bidimensional aplicada al sismograma u(x,t) — base del análisis f-k en [[MASW Method|MASW]]; convierte datos tiempo-espacio en espacio frecuencia-[[Wavenumber|número de onda]]
type: reference
---

# 2D Fourier Transform — Transformada de Fourier 2D

> [!CONCEPT] Definición
> La **transformada de Fourier 2D** descompone el sismograma $u(x, t)$ (registros de $N$ [[Geophone|geófono]]) en sus componentes sinusoidales en el dominio de la frecuencia $f$ y el [[Wavenumber|número de onda]] $k$. Es la base del **análisis f-k** del [[MASW Method|MASW]]: $U(\omega, k) = \sum_{j,n} u(x_j, t_n)\, e^{-i(\omega t_n - k x_j)}$. En el espectrograma $|U(\omega, k)|$, cada modo de propagación aparece como una **cresta** cuya posición $(f, k_{\text{cresta}})$ da directamente la [[Phase Velocity|velocidad de fase]] $c_R(f) = 2\pi f / k_{\text{cresta}}$. La resolución en frecuencia es $\Delta f = 1/T$ (controlada por la duración del registro $T$) y la resolución en [[Wavenumber|número de onda]] es $\Delta k = 2\pi/D$ (controlada por la apertura total del arreglo $D = N\Delta x$). La separación de modos en el espectrograma depende de $\Delta k$: arreglos más largos resuelven mejor los modos superiores.
>
> — Foti et al. (2018), Cap. 4, §4.2, pp. 195–215; Park et al. (1999).

## Definición matemática

Para un sismograma discreto $u(x_j, t_n)$ con $j = 1, \ldots, N_x$ [[Geophone|geófono]] y $n = 1, \ldots, N_t$ muestras temporales:

$$U(\omega, k) = \sum_{j=1}^{N_x} \sum_{n=1}^{N_t} u(x_j, t_n)\, e^{-i(\omega t_n - k x_j)}$$

Esta es la DFT 2D del sismograma. En la práctica se implementa en dos etapas:
1. **FFT temporal**: $U(x_j, \omega) = \text{FFT}[u(x_j, \cdot)]$ — para cada [[Geophone|geófono]]
2. **FFT espacial**: $U(\omega, k) = \text{FFT}_k[U(\cdot, \omega)]$ — para cada frecuencia

El orden es intercambiable (linealidad). La complejidad total es $O(N_x N_t \log(N_x N_t))$.

## Propiedades relevantes para [[MASW Method|MASW]]

| Propiedad | Expresión | Significado físico |
|---|---|---|
| Resolución en frecuencia | $\Delta f = 1/T$ | Mayor duración → más resolución frecuencial |
| Resolución en wavenumber | $\Delta k = 2\pi/D$ | Mayor apertura → mejor separación modal |
| Alias temporal (Nyquist) | $f_{max} = f_s/2$ | Frecuencia de muestreo limita rango espectral |
| Alias espacial | $k_{max} = \pi/\Delta x$ | Espaciado [[Geophone|geófono]] limita wavenumber máximo |

## Extracción de la [[Dispersion Curve|curva de dispersión]]

El espectrograma $|U(\omega, k)|$ se analiza para identificar las crestas que corresponden a modos de [[Surface Wave Modes|Rayleigh]]:

1. Para cada frecuencia $f_i$, encontrar el máximo de $|U(2\pi f_i, k)|$ en $k$: $k^*(f_i) = \arg\max_k |U(f_i, k)|$
2. La [[Phase Velocity|velocidad de fase]]: $c_R(f_i) = 2\pi f_i / k^*(f_i)$
3. La [[Dispersion Curve|curva de dispersión experimental]] es $\{(f_i, c_R(f_i))\}_{i=1}^{N_f}$

## Relación con otros métodos de procesamiento

| Método | Base matemática | Equivalencia |
|---|---|---|
| f-k directo | DFT 2D | Este método |
| [[Procesamiento de Señales|Tau-P / slant-stack]] | Transformada de Radon | Equivalente en el límite de densidad infinita de $p$ |
| [[SASW Method|Espectro cruzado]] | DFT 1D por par | Caso especial con $N_x = 2$ |
| Beamforming | DFT espacial con pesos | Generalización con taper espacial |
| **Phase-shift** (Park 1998) | Suma de fases $\sum u_{norm} \cdot e^{i\omega x/c_T}$ | Alta resolución con pocos [[Geophone|geófono]]; estándar de MASWaves/SurfSeis |

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — 2D FFT como estándar para extracción de la [[Dispersion Curve|curva de dispersión]] [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** introduce el análisis f-k mediante 2D FFT como el método de referencia para [[MASW Method|MASW]], reemplazando el método de espectro cruzado de dos receptores del [[SASW Method|SASW]]. Con 24 [[Geophone|geófono]] a espaciado 1.5 m (apertura $D = 34.5$ m), el espectrograma f-k muestra una cresta del modo fundamental de Rayleigh estrecha y bien definida entre 5–30 Hz. La resolución en [[Wavenumber|número de onda]] $\Delta k = 2\pi/34.5 \approx 0.18$ rad/m permite separar visualmente el modo fundamental de los superiores en todo el rango de frecuencias útil. El trabajo establece que la 2D FFT sobre el sismograma completo es más robusta y reproducible que el análisis por pares de receptores del [[SASW Method|SASW]], porque promedia la información de todos los [[Geophone|geófono]] simultáneamente, reduciendo el efecto del ruido incoherente.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3).

> [!EXAMPLE] Evidencia empírica: Ólafsdóttir et al. (2018) — MASWaves: validación del phase-shift en 3 sitios islandeses
> **Paper 022 (Ólafsdóttir, Erlingsson & Bessason 2018, CGJ 55(2):217–233)** presenta la herramienta open-source MASWaves (MATLAB) que implementa el phase-shift de Park et al. (1998) para extracción de [[Dispersion Curve|curvas de dispersión]] con bandas de incertidumbre. Validada en 3 sitios de Islandia (Arnarbæli, Bakkafjara, Hella) con 24 [[Geophone|geófono]] GS-11D de 4.5 Hz y sledgehammer, los espectrogramas f-k obtenidos con MASWaves son **equivalentes a los de Geopsy** (software de referencia europea) en los mismos datos. La herramienta documentada incluye datos de muestra, guía de usuario y código fuente libre (también disponible en Python como MASWavesPy). Relevancia directa: mismo hardware que la presente tesis (4.5 Hz geophones); herramienta libre lista para aplicar sin software comercial.
>
> — Research Database, entrada 022 (core); Ólafsdóttir et al. (2018), *Can. Geotech. J.* 55(2):217–233.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2, pp. 195–215 — análisis f-k completo |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — 2D FFT como estándar [[MASW Method|MASW]] |
| Park, Miller & Xia (1998), SEG abstract | Paper 023 — algoritmo phase-shift, 761 citas; base de MASWaves y SurfSeis |
| Ólafsdóttir et al. (2018), *CGJ* 55(2):217–233 | Paper 022 — MASWaves phase-shift; validación Geopsy en 3 sitios islandeses |
