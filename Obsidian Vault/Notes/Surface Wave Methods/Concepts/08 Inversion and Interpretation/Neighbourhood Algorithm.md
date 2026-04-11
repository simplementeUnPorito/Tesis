---
name: Neighbourhood Algorithm
description: Algoritmo de búsqueda global que subdivide el espacio de modelos en celdas de Voronoi y concentra el muestreo en las regiones de mejor misfit — eficiente para inversión de dispersión
type: reference
---

# Neighbourhood Algorithm — Algoritmo de Vecindad (NA)

> [!CONCEPT] Definición
> El **Neighbourhood Algorithm (NA)** es un método de [[Inversión|inversión]] de búsqueda global propuesto por Sambridge (1999) que busca el mínimo global de la función de misfit en el espacio de modelos sin calcular derivadas. Opera dividiendo el espacio de modelos en **celdas de Voronoi** asignadas a los modelos ya evaluados, y concentrando el nuevo muestreo en las celdas con mejor misfit (mínimo misfit de la celda). A diferencia del [[Monte Carlo Methods|Monte Carlo]] puro (muestreo uniforme aleatorio), el NA es **adaptativo**: aprende dónde está el mínimo y concentra recursos computacionales en esa región. A diferencia del [[Genetic Algorithm|Algoritmo Genético]], no requiere parámetros de control complejos (tasa de mutación, cruce) — solo el número de modelos por iteración ($n_s$) y el número de celdas a re-muestrear ($n_r \leq n_s$). En [[MASW Method|MASW]], el NA explora eficientemente el espacio de modelos $V_S(z)$ encontrando el mínimo global del misfit entre la [[Dispersion Curve|curva de dispersión]] teórica y la experimental, con un costo computacional significativamente menor que el Monte Carlo puro para la misma precisión.
>
> — Sambridge (1999), *Geophys. J. Int.*; Foti et al. (2018), §6.4.3; Wathelet et al. (2004).

## Principio del algoritmo

### Iteración básica

1. **Inicialización**: muestrear $n_s$ modelos aleatoriamente → evaluar misfit → construir diagrama de Voronoi
2. **En cada iteración**:
   - Identificar las $n_r$ celdas con menor misfit
   - Dentro de cada celda seleccionada, muestrear $n_s/n_r$ nuevos modelos aleatoriamente
   - Evaluar misfit de los nuevos modelos
   - Actualizar el diagrama de Voronoi con todos los modelos evaluados hasta ahora
3. **Criterio de parada**: número total de modelos evaluados o convergencia del misfit mínimo

### Parámetros de control

- $n_s$: número de nuevos modelos por iteración (típicamente 20–50)
- $n_r$: número de celdas a re-muestrear (típicamente $n_r = n_s/2$)
- Iteraciones totales: 50–200 (costo total = $n_s \times \text{iteraciones}$ evaluaciones)

## Ventajas sobre otros métodos de búsqueda global

| Propiedad | [[Monte Carlo Methods\|Monte Carlo]] | [[Genetic Algorithm\|GA]] | NA |
|-----------|------|----|----|
| Muestreo | Uniforme (ciego) | Dirigido por aptitud | Dirigido por Voronoi |
| Parámetros de control | Ninguno | Muchos ($p_m$, $p_c$, población) | Pocos ($n_s$, $n_r$) |
| Eficiencia | Baja | Media | Alta |
| Análisis de incertidumbre | Requiere postprocesado | Requiere postprocesado | Integrado (NA-Bayes) |

## Aplicación al análisis de incertidumbre

Sambridge (1999b) extiende el NA a la **etapa de estimación** (*appraisal stage*) mediante el **NA-Bayes**: los modelos evaluados y sus misfits se usan para estimar la distribución posterior del modelo $p(\mathbf{m}|\mathbf{d})$ sin necesidad de muestreo adicional. Esto permite:
- Estimar la **media aposteriori** y la **covarianza** de los parámetros
- Cuantificar la [[Non-uniqueness|no-unicidad]] del problema inverso
- Obtener intervalos de confianza para $V_{S,30}$ y otros parámetros derivados

> [!EXAMPLE] Evidencia empírica: Wathelet et al. (2004) — NA en inversión de datos de MASW y arrays pasivos
> Wathelet, Jongmans & Ohrnberger (2004) aplican el Neighbourhood Algorithm a la inversión de curvas de dispersión de MASW y arrays pasivos (SPAC/beamforming) en el software **Geopsy/Dinver** — que implementa el NA de Sambridge (1999). En el sitio de Grenoble (depósitos aluviales profundos), el NA evalúa 50,000 modelos $V_S(z)$ en ~10 minutos en hardware de la época (vs. semanas equivalentes con Monte Carlo). El conjunto de modelos aceptables (misfit < umbral) reproduce el perfil de referencia (Cross-Hole) dentro de ±15% en todo el perfil de 50 m, con incertidumbre $\sigma_{V_{S,30}} \approx 8\%$. La implementación en Geopsy/Dinver se convirtió en el estándar de facto para la inversión de datos de ondas superficiales en Europa, adoptada también en los estudios InterPACIFIC (Papers 006, 007).
>
> — Wathelet, Jongmans & Ohrnberger (2004), *Near Surface Geophysics* 2(4); Sambridge (1999a/b), *Geophys. J. Int.* 138/139.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.3 — comparación de métodos de inversión global |
| Sambridge (1999a), *Geophys. J. Int.* 138 | Formulación del Neighbourhood Algorithm (búsqueda) |
| Sambridge (1999b), *Geophys. J. Int.* 139 | NA-Bayes para análisis de incertidumbre |
| Wathelet et al. (2004), *Near Surface Geophysics* | Aplicación del NA a inversión de dispersión — Geopsy/Dinver |
