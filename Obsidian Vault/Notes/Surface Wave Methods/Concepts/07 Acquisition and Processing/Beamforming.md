---
name: Beamforming
description: Técnica de procesamiento de array para estimar la dirección y velocidad de propagación de ondas — generalización del análisis f-k con pesos espaciales; base de métodos pasivos [[MASW Method|MASW]] con ruido ambiental
type: reference
---

# Beamforming — Formación de Haz

> [!CONCEPT] Definición
> El **beamforming** (o *formación de haz*) es una técnica de procesamiento de array que estima la **[[Phase Velocity|velocidad de fase]] y dirección de propagación** de ondas sísmicas combinando linealmente las señales de múltiples receptores con pesos $w_j$ y retardos $\tau_j$: $B(\omega, k) = |\sum_j w_j U(x_j, \omega) e^{ik x_j}|^2$. Es la generalización del análisis f-k ([[2D Fourier Transform|2D FFT]]) que permite aplicar ventanas espaciales (tapering) para reducir los lóbulos laterales del espectrograma. En su forma más simple (pesos iguales $w_j = 1/N$), el beamformer es idéntico al análisis f-k estándar de [[MASW Method|MASW]]. Con pesos Hamming o Hann (*spatial tapering*), mejora la separación de modos a costa de reducir la resolución pico. Para arrays **2D** (no lineales), el beamformer estima el vector [[Wavenumber|número de onda]] $\mathbf{k}$ completo, permitiendo separar contribuciones de diferentes direcciones de propagación — clave en [[Seismic Interferometry|interferometría pasiva]] y en [[SPAC Method|SPAC]] con geometrías arbitrarias.
>
> — Foti et al. (2018), Cap. 4, §4.2, pp. 195–215; Lacoss et al. (1969).

## Formulación

### Beamformer convencional (Delay-and-Sum)

Para un array lineal con $N$ receptores en posiciones $x_j$, la respuesta del beamformer para una onda de [[Wavenumber|número de onda]] $k$ y frecuencia $\omega$ es:

$$B(\omega, k) = \left|\sum_{j=1}^{N} w_j\, U(x_j, \omega)\, e^{i k x_j}\right|^2$$

donde $U(x_j, \omega) = \text{FFT}[u(x_j, \cdot)]$ y $w_j$ son los pesos espaciales (ventana).

Con $w_j = 1/N$ (pesos uniformes): $B(\omega, k) = |U(\omega, k)|^2/N^2$ — el espectrograma f-k estándar.

### Función de respuesta del array (Array Response Function, ARF)

Para una señal de [[Wavenumber|número de onda]] verdadero $k_0$, el beamformer produce un pico a $k_0$ con ancho:

$$\Delta k \approx \frac{2\pi}{D} \quad \text{(ventana uniforme)}, \quad \Delta k \approx \frac{4\pi}{D} \quad \text{(ventana Hann)}$$

Los lóbulos laterales (aliasing espacial) aparecen a $k = k_0 \pm 2\pi n/\Delta x$ para $n \in \mathbb{Z}$.

## Beamformer de alta resolución (CAPON/MVDR)

El beamformer de **varianza mínima** (Capon 1969) maximiza la potencia en la dirección de interés mientras suprime otras contribuciones:

$$B_{MVDR}(\omega, k) = \frac{1}{\mathbf{e}^H(\omega, k)\, \mathbf{C}^{-1}(\omega)\, \mathbf{e}(\omega, k)}$$

donde $\mathbf{C}(\omega)$ es la matriz de covarianza espectral cruzada entre receptores y $\mathbf{e}$ es el vector de dirección. Ofrece mejor resolución modal que el beamformer convencional pero requiere invertir la matriz de covarianza — más costoso computacionalmente.

## Aplicación en arrays 2D (métodos pasivos)

Para arrays 2D (triángulo, espiral, aleatorio), el beamformer estima el vector 2D de [[Wavenumber|número de onda]] $(k_x, k_y)$:

$$B(\omega, k_x, k_y) = \left|\sum_j w_j\, U(\mathbf{x}_j, \omega)\, e^{i(k_x x_j + k_y y_j)}\right|^2$$

El máximo del mapa 2D da la [[Phase Velocity|velocidad de fase]] y la dirección de propagación dominante. Esto es más informativo que los métodos 1D ([[MASW Method|MASW]], [[ReMi Method|ReMi]]) pero requiere más receptores y cobertura espacial.

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — beamforming 2D en InterPACIFIC para arrays pasivos
> **Papers 006+007 (Garofalo et al. 2016a/b)** incluyen resultados de beamforming 2D aplicado a arrays pasivos en los sitios InterPACIFIC (Grenoble, Mirandola, Cadarache). El beamforming 2D permite estimar la anisotropía del campo de ruido ambiental: en Grenoble, el mapa $(k_x, k_y)$ muestra una fuente de ruido dominante en una dirección (montañas cercanas), lo que explica los sesgos de velocidad aparente observados con [[ReMi Method|ReMi]] en ese sitio. En los sitios con ruido más isotrópico (Mirandola, Cadarache), el beamforming 2D y el [[MASW Method|MASW]] activo producen [[Dispersion Curve|curvas de dispersión]] consistentes en el rango de frecuencias compartido. El beamforming 2D es el diagnóstico estándar para validar si el campo de ruido pasivo es suficientemente isotrópico para métodos como [[SPAC Method|SPAC]] o [[ReMi Method|ReMi]].
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a/b), *Near Surface Geophysics*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2, pp. 195–215 — beamforming en [[MASW Method|MASW]] |
| Lacoss et al. (1969), *Geophysics* | Beamforming convencional y de alta resolución para arrays sísmicos |
| Capon (1969), *Proc. IEEE* | Beamformer MVDR (Capon) |
| Garofalo et al. (2016a/b) | Papers 006, 007 — beamforming 2D en InterPACIFIC |
