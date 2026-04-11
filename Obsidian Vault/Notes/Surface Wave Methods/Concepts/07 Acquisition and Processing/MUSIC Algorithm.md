---
name: MUSIC Algorithm
description: MUltiple SIgnal Classification — algoritmo de subespacio de alta resolución que descompone la matriz espectral en subespacios de señal y ruido para estimar la [[Dispersion Curve|curva de dispersión]] con resolución super-Rayleigh — alternativa al análisis f-k convencional en [[MASW Method|MASW]] con arreglos cortos
type: reference
---

# MUSIC Algorithm — MUltiple SIgnal Classification

> [!CONCEPT] Definición
> El algoritmo **MUSIC** (*MUltiple SIgnal Classification*) es un método de estimación espectral de **alta resolución** basado en la descomposición en subespacios de la **matriz de coherencia espectral** (o matriz de covarianza espacial) del campo de ondas. Para un arreglo de $N$ geófonos con respuestas espectrales $\{U_i(f)\}$, se construye la matriz de covarianza espacial:
> $$\mathbf{R}(f) = \mathbb{E}[\mathbf{u}(f) \mathbf{u}^H(f)] \approx \frac{1}{L} \sum_{l=1}^L \mathbf{u}_l(f) \mathbf{u}_l^H(f)$$
> donde $\mathbf{u} = [U_1, \ldots, U_N]^T$ y $L$ es el número de realizaciones. La [[Singular Value Decomposition|SVD]] de $\mathbf{R}$ la descompone en subespacio de señal (primeros $K$ vectores propios, $K$ = número de modos de [[Surface Waves|ondas superficiales]]) y subespacio de ruido (vectores propios restantes). El **pseudoespectro MUSIC** es:
> $$P_{MUSIC}(f, k) = \frac{1}{\|\mathbf{E}_n^H \mathbf{a}(k)\|^2}$$
> donde $\mathbf{a}(k) = [e^{ikx_1}, \ldots, e^{ikx_N}]^T$ es el vector de dirección para [[Wavenumber|número de onda]] $k$ y $\mathbf{E}_n$ son los vectores propios del subespacio de ruido. Los **picos del pseudoespectro** corresponden a los [[Wavenumber|número de onda]] verdaderos de los modos de [[Surface Waves|ondas superficiales]], con resolución **super-Rayleigh**: puede separar modos con diferencia $\Delta k < 2\pi/D$ (límite del análisis $f$-$k$ convencional), a costa de mayor costo computacional y la necesidad de estimar $K$ correctamente.
>
> — Foti et al. (2018), §4.3.4, pp. 204–210; Schmidt (1986), *IEEE Trans. Antennas Propag.* 34(3); Zywicki & Rix (2005), *JGGE*.

## Comparación MUSIC vs. análisis f-k convencional

| Aspecto | f-k convencional | MUSIC |
|---------|-----------------|-------|
| Resolución | $\Delta k = 2\pi/D$ (Rayleigh) | Super-Rayleigh: puede ser $< \Delta k$ |
| Costo computacional | FFT 2D — muy rápido | SVD de $\mathbf{R}$ — más lento |
| Aplicabilidad multi-modal | Buena si modos bien separados | Excelente — diseñado para señales múltiples |
| Sensibilidad al ruido | Moderada | Alta — precisa estimación de $K$ |
| Longitud del arreglo | Requiere $D$ grande para buena resolución | Funciona con arreglos cortos |
| Software | Estándar (SurfSeis, Geopsy) | Implementaciones de investigación |

MUSIC es especialmente ventajoso en arreglos **cortos** (< 20 m) donde la resolución convencional no permite separar modos cercanos en [[Wavenumber|número de onda]].

## Estimación del número de modos K

La elección de $K$ (número de señales) es crítica. Criterios estándar:
- **MDL** (Minimum Description Length): basado en la probabilidad del modelo
- **AIC** (Akaike Information Criterion): penaliza modelos complejos
- **Brecha espectral**: $K$ = número de valores propios significativamente mayores que el nivel de ruido

Una elección incorrecta de $K$ produce picos espúreos (sobreestimación) o pérdida de modos (subestimación).

> [!EXAMPLE] Evidencia empírica: Zywicki & Rix (2005) — MUSIC para separación multimodal en [[MASW Method|MASW]]
> Zywicki & Rix (2005, *JGGE* 131(11), 1303–1314) aplican el algoritmo MUSIC para extraer [[Dispersion Curve|curvas de dispersión]] multimodal de datos [[MASW Method|MASW]] con un arreglo de solo 12 geófonos a $\Delta x = 1.5$ m (apertura $D = 16.5$ m, resolución $f$-$k$ convencional $\Delta V = V^2/fD \approx 15$ m/s a 20 Hz para $V = 100$ m/s). El pseudoespectro MUSIC resuelve el modo fundamental ($V_R = 95$ m/s a 20 Hz) y el primer modo superior ($V_R = 115$ m/s a 20 Hz) — separación de solo 20 m/s — mientras que el panel $f$-$k$ convencional los fusiona en un único pico de amplitud máxima. La [[Joint Inversion|inversión conjunta]] de ambos modos (MUSIC) reduce la incertidumbre en el perfil $V_S$ profundo en 35% respecto a la inversión del modo fundamental solo.
>
> — Zywicki & Rix (2005), *JGGE* 131(11), 1303–1314; Foti et al. (2018), §4.3.4.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §4.3.4 — métodos de alta resolución en [[MASW Method|MASW]] |
| Schmidt, R.O. (1986), *IEEE Trans. Antennas Propag.* 34(3) | Algoritmo MUSIC original |
| Zywicki & Rix (2005), *JGGE* 131(11), 1303–1314 | Aplicación MUSIC en [[MASW Method|MASW]] multimodal |
