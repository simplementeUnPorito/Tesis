# No-unicidad (Non-uniqueness)

> [!CONCEPT] Definición
> La **no-unicidad** del problema inverso de ondas superficiales es la propiedad por la cual **múltiples perfiles de $V_S(z)$ producen [[Dispersion Curve|curvas de dispersión]] prácticamente idénticas**. No es una limitación del algoritmo de inversión sino una propiedad intrínseca del operador físico. El problema es *ill-posed* (Hadamard 1923): viola las condiciones de unicidad y estabilidad. Causas: resolución finita en profundidad, equivalencia espesor–velocidad entre capas, e insensibilidad de $c_R$ a $V_P$. Se mitiga con (1) **información a priori** (boreholes, nivel freático, geología), (2) [[Tikhonov Regularization|regularización]], (3) [[Monte Carlo Methods|búsqueda global]] para cuantificar el ensemble de soluciones equivalentes, y (4) **[[Joint Inversion|inversión conjunta]]** con otros datos ([[HVSR]], refracción). La no-unicidad raramente impide la clasificación de sitio porque el parámetro de ingeniería $[[Vs30|Vs,30]]$ es robusto: varía solo ~5% dentro del conjunto de soluciones equivalentes.
>
> — Foti et al. (2018), Cap. 6.1.2, pp. 277–280; Cap. 6.4, pp. 305–310.

## Definición

La **no-unicidad** del problema inverso de ondas superficiales significa que **una misma [[Dispersion Curve|curva de dispersión]] experimental puede corresponder a más de un perfil de Vs**. No es una limitación del algoritmo de inversión elegido, sino una propiedad intrínseca del operador físico que relaciona el modelo del subsuelo con los datos observables.

En términos matemáticos, el problema es **ill-posed** según los criterios de Hadamard (1923): un problema bien puesto debe cumplir (1) existencia, (2) unicidad y (3) estabilidad de la solución. Los problemas inversos geofísicos violan habitualmente las condiciones de unicidad y estabilidad.

## Causas físicas

La no-unicidad en ondas superficiales tiene tres raíces físicas:

1. **Resolución en profundidad finita**: la [[Dispersion Curve|curva de dispersión]] mide velocidades de fase en un rango finito de frecuencias, que corresponde a un rango finito de profundidades de investigación. Más allá de la profundidad máxima de investigación, el modelo es completamente no constrenido.

2. **Equivalencia entre parámetros**: distintas combinaciones de espesor de capa y velocidad de corte pueden producir la misma respuesta cinemática. El efecto de una capa delgada rígida puede reproducirse con una capa gruesa de menor rigidez.

3. **Insensibilidad a Vp**: la [[Phase Velocity|velocidad de fase]] de Rayleigh es relativamente insensible a cambios en la velocidad compresional Vp (o equivalentemente a la razón de Poisson). Esto produce un "fondo plano" en la función de error cuando se intenta invertir Vp, de modo que Vp debe asumirse conocida a priori (Foti Fig. 6.11d, p. 308).

## Manifestación práctica

La función de desajuste (*misfit*) $E(\mathbf{m})$ puede tener **múltiples mínimos** con valores similares, correspondiendo a perfiles de Vs diferentes pero igualmente compatibles con los datos (Fig. 6.11, p. 308). Cuatro regímenes típicos de complejidad creciente son (Fig. 6.11a-d):

- **(a)** Mínimo único bien definido: inversión estable y unívoca.
- **(b)** Dos mínimos globales igualmente válidos: solución ambigua.
- **(c)** Múltiples mínimos periódicos: no-unicidad severa, típica de perfiles con inversión de velocidad.
- **(d)** "Fondo plano": rango continuo de soluciones con misfit similar; ill-conditioning extremo.

En la práctica, los perfiles con capas blandas intercaladas (*velocity inversion*) o con alto contraste de impedancia superficial presentan la mayor no-unicidad.

## Estrategias de mitigación

### Información a priori
Incorporar datos externos restringe el espacio de soluciones admisibles:
- **Registros de pozo** (boreholes, SPT): fijan espesor o velocidad de algunas capas.
- **Posición del nivel freático**: permite estimar Vp en la zona saturada mediante la razón de Poisson de fluido saturado (Vp ≈ 1500 m/s).
- **Conocimiento geológico**: limitar el número de capas, fijar rangos de Vs plausibles por litología.

### [[Regularization|Regularización]]
Los métodos de [[Tikhonov Regularization|regularización de Tikhonov]] transforman el problema ill-posed en una familia de problemas mejor condicionados, añadiendo penalizaciones a la función de error por complejidad excesiva del modelo.

### Búsqueda global
Los [[Monte Carlo Methods|métodos de búsqueda global]] ([[Monte Carlo Methods|Monte Carlo]], algoritmos genéticos, simulated annealing) exploran el espacio completo de soluciones y permiten identificar y cuantificar la multiplicicidad de soluciones compatibles con los datos, en lugar de converger a un solo mínimo local.

### [[Joint Inversion|inversión conjunta]]
Combinar la [[Dispersion Curve|curva de dispersión]] con otros datos (refracción de ondas P, H/V, resistividad eléctrica) reduce la no-unicidad porque distintos datasets tienen diferente sensibilidad a los parámetros del modelo (ver [[HVSR|HVSR]], Cap. 8.3 de Foti).

## Implicación para la práctica

La no-unicidad no invalida el método: **el rango de variación de las propiedades de ingeniería** (como [[Vs30|Vs,30]]) dentro del conjunto de soluciones equivalentes suele ser estrecho, aunque los perfiles individuales de Vs difieran. El ejemplo del Capítulo 7 (La Salle, Foti Fig. 7.22, p. 374) muestra que [[Vs30|Vs,30]] varía entre ~480 y 505 m/s para 10⁵ modelos igualmente aceptables. Griffiths et al. (2016) confirman en dos sitios InterPACIFIC que los perfiles VS directos de inversión [[MASW Method|MASW]] producen una variabilidad más realista en la respuesta sísmica de sitio que los métodos estadísticos indirectos (perfiles bounding o percentiles), justificando el uso del ensemble de soluciones [[Monte Carlo Methods|Monte Carlo]] en lugar de un único perfil determinístico.

> [!EXAMPLE] Evidencia empírica: Maraschini & Foti (2010) — misfit de determinante elimina la no-unicidad modal
> **Paper 034 (Maraschini & Foti 2010)** propone reemplazar la función de misfit estándar (diferencia entre [[Dispersion Curve|curvas de dispersión]] modales calculadas y observadas) por el **misfit de determinante**: mínimo de $|\det[\mathbf{M}(c, f)]|$ donde $\mathbf{M}$ es la matriz de estratificación. El misfit de determinante es independiente de la identificación de modos porque incluye automáticamente todos los modos en la función objetivo. En los experimentos sintéticos del paper (modelos con inversión de velocidad severa), el misfit de determinante converge a perfiles $V_S$ correctos desde modelos iniciales muy distintos, mientras que el misfit modal estándar queda atrapado en mínimos locales asociados a confusión de modos. La no-unicidad residual se reduce sustancialmente al no tener que elegir qué modo comparar.
>
> — Research Database, entrada 034 (core); Maraschini & Foti (2010), *Geophysics* 75(3), pp. G1–G11.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6.1.2 (ill-posedness), Cap. 6.4.3 (búsqueda global), pp. 277–310 |
| Hadamard, J. (1923), *Lectures on Cauchy's Problem* | Condiciones de bien-posedness |
| Maraschini & Foti (2010), *Geophysics* 75(3) | Paper 034 — misfit de determinante vs. misfit modal |
| Griffiths et al. (2016), *JGGE/ASCE* 142 | Paper 047 — impacto de incertidumbre VS en respuesta sísmica de sitio |
