---
name: 2D Fourier Transform
description: Transformada de Fourier bidimensional aplicada al sismograma u(x,t) — base del análisis f-k en MASW; convierte datos tiempo-espacio en espacio frecuencia-número de onda
type: reference
---

# 2D Fourier Transform — Transformada de Fourier 2D

> [!CONCEPT] Definición
> La **transformada de Fourier 2D** descompone el sismograma $u(x, t)$ (registros de $N$ geófonos) en sus componentes sinusoidales en el dominio de la frecuencia $f$ y el número de onda $k$. Es la base del **análisis f-k** del [[MASW Method|MASW]]: $U(\omega, k) = \sum_{j,n} u(x_j, t_n)\, e^{-i(\omega t_n - k x_j)}$. En el espectrograma $|U(\omega, k)|$, cada modo de propagación aparece como una **cresta** cuya posición $(f, k_{\text{cresta}})$ da directamente la velocidad de fase $c_R(f) = 2\pi f / k_{\text{cresta}}$. La resolución en frecuencia es $\Delta f = 1/T$ (controlada por la duración del registro $T$) y la resolución en número de onda es $\Delta k = 2\pi/D$ (controlada por la apertura total del arreglo $D = N\Delta x$). La separación de modos en el espectrograma depende de $\Delta k$: arreglos más largos resuelven mejor los modos superiores.
>
> — Foti et al. (2018), Cap. 4, §4.2, pp. 195–215; Park et al. (1999).

## Definición matemática

Para un sismograma discreto $u(x_j, t_n)$ con $j = 1, \ldots, N_x$ geófonos y $n = 1, \ldots, N_t$ muestras temporales:

$$U(\omega, k) = \sum_{j=1}^{N_x} \sum_{n=1}^{N_t} u(x_j, t_n)\, e^{-i(\omega t_n - k x_j)}$$

Esta es la DFT 2D del sismograma. En la práctica se implementa en dos etapas:
1. **FFT temporal**: $U(x_j, \omega) = \text{FFT}[u(x_j, \cdot)]$ — para cada geófono
2. **FFT espacial**: $U(\omega, k) = \text{FFT}_k[U(\cdot, \omega)]$ — para cada frecuencia

El orden es intercambiable (linealidad). La complejidad total es $O(N_x N_t \log(N_x N_t))$.

## Propiedades relevantes para MASW

| Propiedad | Expresión | Significado físico |
|---|---|---|
| Resolución en frecuencia | $\Delta f = 1/T$ | Mayor duración → más resolución frecuencial |
| Resolución en wavenumber | $\Delta k = 2\pi/D$ | Mayor apertura → mejor separación modal |
| Alias temporal (Nyquist) | $f_{max} = f_s/2$ | Frecuencia de muestreo limita rango espectral |
| Alias espacial | $k_{max} = \pi/\Delta x$ | Espaciado geófono limita wavenumber máximo |

## Extracción de la curva de dispersión

El espectrograma $|U(\omega, k)|$ se analiza para identificar las crestas que corresponden a modos de [[Surface Wave Modes|Rayleigh]]:

1. Para cada frecuencia $f_i$, encontrar el máximo de $|U(2\pi f_i, k)|$ en $k$: $k^*(f_i) = \arg\max_k |U(f_i, k)|$
2. La velocidad de fase: $c_R(f_i) = 2\pi f_i / k^*(f_i)$
3. La [[Dispersion Curve|curva de dispersión experimental]] es $\{(f_i, c_R(f_i))\}_{i=1}^{N_f}$

## Relación con otros métodos de procesamiento

| Método | Base matemática | Equivalencia |
|---|---|---|
| f-k directo | DFT 2D | Este método |
| [[Procesamiento de Señales|Tau-P / slant-stack]] | Transformada de Radon | Equivalente en el límite de densidad infinita de $p$ |
| [[SASW Method|Espectro cruzado]] | DFT 1D por par | Caso especial con $N_x = 2$ |
| Beamforming | DFT espacial con pesos | Generalización con taper espacial |

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — 2D FFT como estándar para extracción de la curva de dispersión MASW
> **Paper 001 (Park, Miller & Xia 1999)** introduce el análisis f-k mediante 2D FFT como el método de referencia para MASW, reemplazando el método de espectro cruzado de dos receptores del [[SASW Method|SASW]]. Con 24 geófonos a espaciado 1.5 m (apertura $D = 34.5$ m), el espectrograma f-k muestra una cresta del modo fundamental de Rayleigh estrecha y bien definida entre 5–30 Hz. La resolución en número de onda $\Delta k = 2\pi/34.5 \approx 0.18$ rad/m permite separar visualmente el modo fundamental de los superiores en todo el rango de frecuencias útil. El trabajo establece que la 2D FFT sobre el sismograma completo es más robusta y reproducible que el análisis por pares de receptores del SASW, porque promedia la información de todos los geófonos simultáneamente, reduciendo el efecto del ruido incoherente.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2, pp. 195–215 — análisis f-k completo |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — 2D FFT como estándar MASW |
