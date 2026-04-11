# MOPA (Multi-Offset Phase Analysis)

> [!CONCEPT] Definición
> El **MOPA** (*Multi-Offset Phase Analysis*) es la extensión multicanal del [[SASW Method|método SASW]]: usa el array completo de receptores en una sola adquisición para estimar la [[Dispersion Curve|curva de dispersión]] mediante ajuste de mínimos cuadrados a la relación lineal entre fase y posición de receptor $\varphi_i(\omega) = -k(\omega)x_i + \varphi_0(\omega)$. El [[Wavenumber|número de onda]] $k(\omega)$ y su incertidumbre $\sigma_k$ se obtienen directamente del ajuste — sin necesidad de repetir disparos. Un **test $\chi^2$ de linealidad** permite detectar objetivamente: (1) receptores en campo cercano (desviación de la tendencia lineal), (2) variaciones laterales de impedancia (cambio de pendiente), y (3) contaminación por modos superiores. MOPA asume modo único de propagación; en sitios con modos múltiples significativos, el [[MASW Method|análisis f-k]] proporciona mejor resolución modal.
>
> — Foti et al. (2018), Cap. 4.4, pp. 220–230.

## Principio

**MOPA** (*Multi-Offset Phase Analysis*) es la extensión multicanal del método [[SASW Method|SASW]]. Mientras [[SASW Method|SASW]] usa solo dos receptores y requiere múltiples adquisiciones, MOPA emplea todo el array lineal en una sola adquisición para estimar la [[Dispersion Relation|curva de dispersión]].

Bajo la hipótesis de **un único modo de propagación** y **campo lejano**, la fase del espectro en el receptor $i$ ubicado a posición $x_i$ es una función lineal de la posición:

$$\varphi_i(\omega) = -k(\omega) \cdot x_i + \varphi_0(\omega)$$

donde $k(\omega)$ es el [[Wavenumber|número de onda]] de la onda superficial y $\varphi_0(\omega)$ es la fase en el origen (incluye la fase de la fuente).

## Formulación matricial

El sistema de ecuaciones para todos los receptores $i = 1, \ldots, N$ se escribe en forma matricial:

$$\boldsymbol{\Phi} = \mathbf{G} \cdot \mathbf{M}$$

donde:
- $\boldsymbol{\Phi} = [\varphi_1, \ldots, \varphi_N]^T$ es el vector de fases observadas,
- $\mathbf{M} = [k(\omega),\ \varphi_0(\omega)]^T$ contiene las incógnitas,
- $\mathbf{G}$ es la matriz de diseño que contiene las posiciones $x_i$ y unos.

La solución por **mínimos cuadrados ponderados** (ponderada por las incertidumbres de fase) entrega el [[Wavenumber|número de onda]] estimado $\hat{k}(\omega)$ y su desviación estándar $\sigma_k$. La [[Phase Velocity|velocidad de fase]] y su incertidumbre son:

$$V(\omega) = \frac{2\pi f}{k}, \qquad \sigma_V = \frac{2\pi f}{k^2}\,\sigma_k$$

La incertidumbre $\sigma_V$ es **directamente estimada** a partir de la dispersión de las fases del array, lo que constituye una ventaja respecto a los métodos de transformada (f-k, τ-p) donde la incertidumbre debe estimarse por repetición de shots.

## Test de linealidad (chi-cuadrado)

Una contribución central de MOPA es ofrecer un **criterio estadístico objetivo** para evaluar la validez de la hipótesis de modo único y campo lejano. Si la fase es lineal en posición (hipótesis válida), el residual del ajuste sigue una distribución $\chi^2$. El test $\chi^2$ de linealidad (Foti Ecs. 4.26–4.27) permite:

- **Detectar automáticamente** bandas de frecuencia donde la hipótesis se viola.
- Identificar los receptores afectados por **efectos de campo cercano** (los receptores más cercanos a la fuente exhiben desviaciones de la tendencia lineal de fase).
- Detectar **variaciones laterales**: un cambio de pendiente en la distribución fase-offset a lo largo de la posición del array indica la presencia de una discontinuidad lateral.

## Ventajas respecto a [[SASW Method|SASW]]

| Aspecto | [[SASW Method|SASW]] | MOPA |
|---|---|---|
| Número de receptores | 2 | Array completo (N receptores) |
| Adquisiciones necesarias | Múltiples (distintos espaciados) | Una sola |
| Estimación de incertidumbre | No directa | Directa ($\sigma_V$) |
| Detección de campo cercano | No | Sí (desviación lineal) |
| Detección de variaciones laterales | No | Sí (cambio de pendiente) |
| Test de validez de hipótesis | No | Sí (test $\chi^2$) |

## Detección de heterogeneidades laterales

Cuando las fases observadas presentan una **no-linealidad sistemática** a lo largo del array, las causas pueden ser:

1. **Receptores en campo cercano**: los receptores más próximos a la fuente reciben ondas con curvatura significativa del frente; la hipótesis de onda plana no se cumple. La solución es excluir los receptores afectados del ajuste.
2. **Variaciones laterales de impedancia**: una discontinuidad lateral cambia el [[Wavenumber|número de onda]] a lo largo del perfil. El método de Vignoli y Cassiani (2009) segmenta adaptativamente el array en zonas donde la hipótesis de propagación lateralmente homogénea se verifica, generando una sección 2D pseudo-lateral de velocidades.

Esta capacidad de detectar heterogeneidades laterales hace de MOPA una herramienta complementaria al análisis f-k del método [[MASW Method|MASW]], que asume implícitamente modelo 1D.

## Relación con otros métodos

- MOPA asume **modo único**: no puede resolver la contribución de modos superiores. Si la imagen f-k muestra múltiples ramas modales bien separadas, [[MASW Method|MASW]] proporciona mejor resolución modal.
- La estimación directa de $\sigma_V$ convierte a MOPA en el **método de referencia** para la cuantificación de incertidumbre en la [[Dispersion Curve|curva de dispersión]] (Foti p. 227): otros métodos estiman la incertidumbre de forma empírica o por repetición de shots.
- En el contexto de la caracterización del sitio, MOPA se aplica típicamente sobre los mismos datos del [[MASW Method|MASW]] como análisis complementario o alternativo.

## Limitaciones

- La hipótesis de modo único puede no cumplirse en sitios con perfil de velocidad complejo (alta impedancia superficial, inversión de velocidad) donde varios modos tienen energía comparable.
- No proporciona imagen del campo de onda en el dominio $f$-$k$: la visualización de la [[Dispersion Curve|curva de dispersión]] depende de la calidad del ajuste lineal por frecuencia, no de un espectro 2D.
- Sensible a ruido coherente (reflexiones, refracciones) que contamine la fase de la onda superficial directa.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — MOPA como referencia de incertidumbre en [[Dispersion Curve|curva de dispersión]]
> Foti et al. (2018, §4.4) aplican MOPA a datos de campo [[MASW Method|MASW]] y demuestran que la incertidumbre estimada directamente por el ajuste de mínimos cuadrados ($\sigma_V$ como función de $f$) es coherente con la variabilidad empírica observada entre disparos repetidos. En el ejemplo del sitio de referencia, el test $\chi^2$ identifica automáticamente las frecuencias donde los receptores del extremo cercano (campo cercano a la fuente) producen desviaciones sistemáticas de la tendencia lineal de fase — eliminando la necesidad de determinar el offset mínimo de fuente por reglas empíricas. La incertidumbre MOPA propagada a través de la inversión produce bandas de confianza en $V_S(z)$ equivalentes a las obtenidas por Monte Carlo con un costo computacional mínimo. MOPA se recomienda como análisis complementario al espectrograma f-k para cuantificar la incertidumbre de la [[Dispersion Curve|curva de dispersión]].
>
> — Foti et al. (2018), §4.4, pp. 220–230.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4.4, pp. 220–230, Ecs. 4.12–4.27 |
| Vignoli & Cassiani (2009), *Near Surface Geophysics* | Segmentación adaptativa del array para variaciones laterales |
