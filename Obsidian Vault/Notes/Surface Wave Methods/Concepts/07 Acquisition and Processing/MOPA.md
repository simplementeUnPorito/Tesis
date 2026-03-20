# MOPA (Multi-Offset Phase Analysis)

> **Contexto:** Método de análisis de fase multicanal para estimar la curva de dispersión a partir de un array lineal, con estimación directa de incertidumbre y detección de efectos de campo cercano.
> **Fuente:** Foti et al. (2014), Cap. 4.4, pp. 220–230.

## Principio

**MOPA** (*Multi-Offset Phase Analysis*) es la extensión multicanal del método [[SASW Method|SASW]]. Mientras SASW usa solo dos receptores y requiere múltiples adquisiciones, MOPA emplea todo el array lineal en una sola adquisición para estimar la [[Dispersion Relation|curva de dispersión]].

Bajo la hipótesis de **un único modo de propagación** y **campo lejano**, la fase del espectro en el receptor $i$ ubicado a posición $x_i$ es una función lineal de la posición:

$$\varphi_i(\omega) = -k(\omega) \cdot x_i + \varphi_0(\omega)$$

donde $k(\omega)$ es el número de onda de la onda superficial y $\varphi_0(\omega)$ es la fase en el origen (incluye la fase de la fuente).

## Formulación matricial

El sistema de ecuaciones para todos los receptores $i = 1, \ldots, N$ se escribe en forma matricial:

$$\boldsymbol{\Phi} = \mathbf{G} \cdot \mathbf{M}$$

donde:
- $\boldsymbol{\Phi} = [\varphi_1, \ldots, \varphi_N]^T$ es el vector de fases observadas,
- $\mathbf{M} = [k(\omega),\ \varphi_0(\omega)]^T$ contiene las incógnitas,
- $\mathbf{G}$ es la matriz de diseño que contiene las posiciones $x_i$ y unos.

La solución por **mínimos cuadrados ponderados** (ponderada por las incertidumbres de fase) entrega el número de onda estimado $\hat{k}(\omega)$ y su desviación estándar $\sigma_k$. La velocidad de fase y su incertidumbre son:

$$V(\omega) = \frac{2\pi f}{k}, \qquad \sigma_V = \frac{2\pi f}{k^2}\,\sigma_k$$

La incertidumbre $\sigma_V$ es **directamente estimada** a partir de la dispersión de las fases del array, lo que constituye una ventaja respecto a los métodos de transformada (f-k, τ-p) donde la incertidumbre debe estimarse por repetición de shots.

## Test de linealidad (chi-cuadrado)

Una contribución central de MOPA es ofrecer un **criterio estadístico objetivo** para evaluar la validez de la hipótesis de modo único y campo lejano. Si la fase es lineal en posición (hipótesis válida), el residual del ajuste sigue una distribución $\chi^2$. El test $\chi^2$ de linealidad (Foti Ecs. 4.26–4.27) permite:

- **Detectar automáticamente** bandas de frecuencia donde la hipótesis se viola.
- Identificar los receptores afectados por **efectos de campo cercano** (los receptores más cercanos a la fuente exhiben desviaciones de la tendencia lineal de fase).
- Detectar **variaciones laterales**: un cambio de pendiente en la distribución fase-offset a lo largo de la posición del array indica la presencia de una discontinuidad lateral.

## Ventajas respecto a SASW

| Aspecto | SASW | MOPA |
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
2. **Variaciones laterales de impedancia**: una discontinuidad lateral cambia el número de onda a lo largo del perfil. El método de Vignoli y Cassiani (2009) segmenta adaptativamente el array en zonas donde la hipótesis de propagación lateralmente homogénea se verifica, generando una sección 2D pseudo-lateral de velocidades.

Esta capacidad de detectar heterogeneidades laterales hace de MOPA una herramienta complementaria al análisis f-k del método [[MASW Method|MASW]], que asume implícitamente modelo 1D.

## Relación con otros métodos

- MOPA asume **modo único**: no puede resolver la contribución de modos superiores. Si la imagen f-k muestra múltiples ramas modales bien separadas, MASW proporciona mejor resolución modal.
- La estimación directa de $\sigma_V$ convierte a MOPA en el **método de referencia** para la cuantificación de incertidumbre en la curva de dispersión (Foti p. 227): otros métodos estiman la incertidumbre de forma empírica o por repetición de shots.
- En el contexto de la caracterización del sitio, MOPA se aplica típicamente sobre los mismos datos del [[MASW Method|MASW]] como análisis complementario o alternativo.

## Limitaciones

- La hipótesis de modo único puede no cumplirse en sitios con perfil de velocidad complejo (alta impedancia superficial, inversión de velocidad) donde varios modos tienen energía comparable.
- No proporciona imagen del campo de onda en el dominio $f$-$k$: la visualización de la curva de dispersión depende de la calidad del ajuste lineal por frecuencia, no de un espectro 2D.
- Sensible a ruido coherente (reflexiones, refracciones) que contamine la fase de la onda superficial directa.

## Referencias

- Foti et al. (2014), Cap. 4.4, pp. 220–230, Ecs. 4.12–4.27.
- Vignoli, G., Cassiani, G. (2009), *Near Surface Geophysics*.
