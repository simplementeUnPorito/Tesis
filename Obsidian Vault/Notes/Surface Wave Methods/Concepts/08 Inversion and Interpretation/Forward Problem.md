---
name: Forward Problem
description: Cálculo de la curva de dispersión teórica dado un perfil de velocidades VS(z) — núcleo del proceso de inversión de ondas superficiales; implementado mediante la matriz de Thomson-Haskell o el eigenproblem de Rayleigh
type: reference
---

# Forward Problem — Problema Directo

> [!CONCEPT] Definición
> El **problema directo** (*forward problem*) en el contexto de [[Surface Waves|ondas superficiales]] consiste en calcular la **respuesta sintética del modelo** — principalmente la [[Dispersion Curve|curva de dispersión]] de velocidades de fase teóricas $c_R(\omega)$ — dado un modelo de parámetros del subsuelo $\mathbf{m}$ (velocidades $V_S(z)$, $V_P(z)$, densidades $\rho(z)$ y espesores $h_i$ de cada capa). El forward problem es el inverso lógico del [[Inversión|problema inverso]]: mientras la inversión busca el modelo dado los datos, el problema directo calcula los datos dados el modelo. Es la operación fundamental que debe ejecutarse en cada iteración del proceso de inversión para comparar los datos sintéticos con los observados y calcular el residual (función de desajuste o *misfit*).
>
> $$\mathbf{d}_{calc} = \mathcal{F}(\mathbf{m})$$
>
> donde $\mathbf{d}_{calc}$ es el vector de datos calculados (velocidades de fase a cada frecuencia) y $\mathcal{F}$ es el operador del problema directo que mapea el espacio de modelos al espacio de datos. La calidad y eficiencia del forward solver determinan en gran parte el costo computacional de la inversión: en métodos de búsqueda global como [[Monte Carlo Methods|Monte Carlo]] o [[Neighbourhood Algorithm|algoritmo de vecindad]], el forward problem se evalúa miles o millones de veces.
>
> — Foti et al. (2018), §6.1, pp. 277–280; Thomson (1950); Haskell (1953).

## Implementación numérica

El forward problem para [[Layered Media|medios estratificados]] horizontalmente se resuelve mediante dos formulaciones equivalentes:

### 1. Matriz de Thomson-Haskell

La [[Thomson-Haskell Matrix|matriz de Thomson-Haskell]] (o matriz de transferencia) relaciona el estado del campo de ondas en la superficie de cada capa con el estado en la siguiente interfaz. El **problema de dispersión** se reduce a encontrar los valores de [[Phase Velocity|velocidad de fase]] $c$ para los cuales el determinante del sistema es cero (condición de borde libre en la superficie y de radiación en la base):

$$\Delta(c, \omega) = \det[\mathbf{T}(c, \omega)] = 0$$

El barrido de valores de $c$ en un rango de interés (por ejemplo, $c \in [0.1, 2.0]$ km/s) para cada frecuencia $\omega$ permite identificar los modos de propagación ([[Surface Wave Modes|modos de ondas superficiales]]).

### 2. Eigenproblem de Rayleigh

El [[Rayleigh Eigenproblem|eigenproblem de Rayleigh]] formula el problema de dispersión como un problema de autovalores de una matriz cuyas entradas dependen de los parámetros del modelo. Este enfoque es numéricamente más estable que la matriz de Thomson-Haskell para perfiles con capas de alta velocidad (donde pueden producirse desbordamientos numéricos), y es la base de los algoritmos modernos como el método de elementos de película delgada (*thin-layer method*).

### 3. Modelos viscoelásticos

Para medios [[Viscoelastic Media|viscoelásticos]], los módulos elásticos $\mu$ y $\lambda$ se reemplazan por módulos complejos frecuencia-dependientes $\tilde{\mu}(\omega)$ mediante el [[Correspondence Principle|principio de correspondencia]]. El forward problem devuelve en este caso una velocidad de fase compleja $\tilde{c}(\omega) = c_R(\omega) + ic_I(\omega)$, cuya parte imaginaria está relacionada con el coeficiente de atenuación $\alpha(\omega) = \omega c_I / c_R^2$.

## Relación con la Jacobiana

La [[Jacobian Matrix|matriz Jacobiana]] (o de sensibilidad) del problema directo es la derivada del vector de datos calculados respecto a los parámetros del modelo:

$$J_{ij} = \frac{\partial d_i}{\partial m_j}$$

Se usa en los métodos de inversión de gradiente local ([[Gauss-Newton Method|Gauss-Newton]], [[Levenberg-Marquardt|Levenberg-Marquardt]]) para linealizar iterativamente el problema inverso. Puede calcularse analíticamente (más eficiente) o numéricamente por diferencias finitas:

$$J_{ij} \approx \frac{\mathcal{F}(\mathbf{m} + \epsilon\mathbf{e}_j)_i - \mathcal{F}(\mathbf{m})_i}{\epsilon}$$

## Consideraciones prácticas

- **Costo computacional**: la evaluación de $\mathcal{F}(\mathbf{m})$ requiere raíces de la ecuación de dispersión; para $N$ frecuencias y $L$ capas, la complejidad es $\mathcal{O}(NL^2)$
- **Modo fundamental vs. modos superiores**: el solver debe ser capaz de distinguir los diferentes [[Surface Wave Modes|modos de propagación]] para inversión multimodal
- **Resolución**: la sensibilidad de los datos al modelo (Jacobiana) determina qué parámetros son resolvibles — capas poco sensibles generan [[Non-uniqueness|no-unicidad]] en la inversión

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — forward problem en el flujo de inversión MASW
> Foti et al. (2018, §6.1, pp. 277–280) describen el forward problem como el núcleo del proceso iterativo de inversión en [[MASW Method|MASW]]: partiendo de un modelo inicial $\mathbf{m}_0$ (perfil de velocidades por capas), se evalúa $\mathcal{F}(\mathbf{m}_0)$ para obtener la [[Dispersion Curve|curva de dispersión]] teórica, se compara con la experimental mediante la función de desajuste $\phi(\mathbf{m}) = ||\mathbf{d}_{obs} - \mathcal{F}(\mathbf{m})||^2$, y se actualiza $\mathbf{m}$ usando el gradiente de $\phi$. La [[Thomson-Haskell Matrix|matriz de Thomson-Haskell]] es el solver estándar implementado en SurfSeis, Geopsy y MASWaves. En el ejemplo del sitio La Salle (Fig. 6.3–6.5), el forward solver evaluado en el perfil óptimo reproduce la [[Dispersion Curve|curva de dispersión]] experimental con un ajuste de 2.5% RMS en el rango 5–50 Hz, mientras que la Jacobiana (calculada por diferencias finitas) muestra que la resolución decrece abruptamente para capas a profundidades >30 m (bajas frecuencias con escasa energía). Esto justifica la estrategia de regularización mediante [[Regularization|algoritmo de Occam]] para estabilizar la inversión en profundidad.
>
> — Foti et al. (2018), §6.1, pp. 277–280; Thomson (1950), *J. Appl. Phys.* 21(9); Haskell (1953), *BSSA* 43(1).

> [!EXAMPLE] Evidencia empírica: Thomson-Haskell vs. eigenproblem — Paper 003 (Xia et al. 1999)
> **Paper 003 (Xia, Miller & Park 1999, *Geophysics* 64(3):691–700)** implementa el forward problem para [[Rayleigh Waves|ondas de Rayleigh]] en medios estratificados horizontalmente usando la [[Thomson-Haskell Matrix|matriz de Thomson-Haskell]] con estabilización numérica (división por factores exponenciales para evitar desbordamientos en capas profundas). La eficiencia del solver permite iterar el proceso [[Gauss-Newton Method|Gauss-Newton]] hasta convergencia en <1 segundo para perfiles de 10–15 capas. El forward problem se evalúa en 64 frecuencias (5–50 Hz) para cada iteración; la Jacobiana se calcula analíticamente aprovechando las propiedades de la matriz de dispersión. Los perfiles Vs resultantes en el sitio de Kansas concuerdan con sondeos de refraccción sísmica dentro del 15% en los primeros 10 m. Este trabajo estableció el estándar del flujo MASW activo: forward problem → Jacobiana → actualización del modelo → convergencia.
>
> — Research Database, entrada 003 (core); Xia et al. (1999), *Geophysics* 64(3):691–700.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.1, pp. 277–280 — forward problem en inversión MASW |
| Thomson (1950), *J. Appl. Phys.* 21(9):89–93 | Matriz de transferencia (formulación original) |
| Haskell (1953), *BSSA* 43(1):17–34 | Matriz de Thomson-Haskell — estabilidad numérica |
| Xia et al. (1999), *Geophysics* 64(3):691–700 | Paper 003 — inversión iterativa con Jacobiana analítica |
| Aki & Richards (2002), *Quantitative Seismology* | §7.2 — eigenproblem de Rayleigh para medios estratificados |
