# Métodos de Monte Carlo (Monte Carlo Methods)

> **Contexto:** Familia de métodos de búsqueda global para la inversión de ondas superficiales que exploran estadísticamente el espacio de parámetros y cuantifican la no-unicidad.
> **Fuente:** Foti et al. (2014), Cap. 6.1.3, p. 280; Cap. 6.4.3, p. 308; Cap. 7.2.4, pp. 371–374; Cap. 8.3.2.3, p. 423.

## Principio

Los **métodos de Monte Carlo** son estrategias de búsqueda global que exploran el espacio de parámetros del modelo mediante **muestreo aleatorio**. En el contexto de la inversión de ondas superficiales, generan una gran población de modelos (perfiles de Vs) y evalúan el desajuste (*misfit*) de cada uno respecto a la curva de dispersión experimental. La distribución de misfit sobre la población permite:

1. Identificar el mejor modelo (mínimo global del misfit).
2. Cuantificar la [[Non-uniqueness|no-unicidad]]: identificar todos los modelos cuyo misfit es estadísticamente compatible con la incertidumbre experimental.
3. Obtener una **caracterización probabilística** del perfil de Vs: bandas de confianza, percentiles, distribución de parámetros derivados como Vs,30.

## Formulación

El desajuste (*misfit*) entre la curva de dispersión teórica $\mathbf{d}^{cal}(\mathbf{m})$ y la experimental $\mathbf{d}^{obs}$ se define como (Foti Ec. 6.34):

$$E(\mathbf{m}) = \frac{1}{N} \sum_{i=1}^{N} \left(\frac{d_i^{cal}(\mathbf{m}) - d_i^{obs}}{\sigma_i}\right)^2$$

donde $\sigma_i$ es la incertidumbre del dato $i$-ésimo. Un modelo se considera **aceptable** si $E(\mathbf{m}) \leq E_{thr}$, donde el umbral $E_{thr}$ se determina mediante un **test de Fisher** al nivel de confianza elegido (p.ej., 95%).

## Implementación en inversión de ondas superficiales

El algoritmo de Monte Carlo global de **Socco y Boiero (2008)** genera $10^5$ modelos de perfil Vs y aplica las propiedades de escala de las curvas modales para guiar el muestreo de manera eficiente:

1. Generar una población de modelos aleatorios dentro de los rangos físicamente plausibles.
2. Calcular la curva de dispersión teórica de cada modelo (problema directo).
3. Evaluar el misfit $E(\mathbf{m})$ para cada modelo.
4. Seleccionar los modelos aceptables con el test de Fisher.
5. Visualizar la distribución de perfiles aceptables (en escala de grises por misfit, más oscuro = menor misfit).

El resultado es un **conjunto de perfiles equivalentes** que representan la solución del problema inverso bajo la incertidumbre de los datos (Foti Fig. 7.19, p. 372).

## Ejemplo: La Salle (Cap. 7.2.4)

- $10^5$ modelos generados; dataset activo+pasivo (48 geófonos, 1.5 m), rango 5–55 Hz.
- Test de Fisher al 95%: selección de ~500 modelos aceptables.
- Capas superficiales bien constrenidas: pequeño rango de variación de Vs.
- Capas profundas (>20 m): mayor incertidumbre — el rango de Vs aceptable se amplía (Foti Fig. 7.19).
- **Resultado práctico**: aunque los perfiles difieren, los espectros de respuesta 1D calculados con cada perfil son prácticamente idénticos (Fig. 7.21, p. 373). La no-unicidad no se traduce en incertidumbre práctica para la respuesta sísmica.
- **Vs,30**: varía entre ~480 y 505 m/s para todos los perfiles aceptables (Fig. 7.22, p. 374) — variación estrecha y gestionable para aplicaciones normativas.

## Ventajas respecto a la búsqueda local

| Aspecto | Búsqueda local (LS) | Monte Carlo (GS) |
|---|---|---|
| Exploración del espacio | Local (desde modelo inicial) | Global (aleatorio) |
| Riesgo de mínimos locales | Alto | Bajo |
| Coste computacional | Bajo | Alto |
| Cuantificación de no-unicidad | No | Sí (conjunto de soluciones) |
| Resultado | Perfil único | Familia de perfiles aceptables |

## Variantes y métodos relacionados

- **Multistart Monte Carlo**: lanzar múltiples búsquedas LS desde modelos iniciales generados aleatoriamente.
- **Neighbourhood Algorithm** (Sambridge 1999): búsqueda global guiada por la geometría del espacio de parámetros.
- **Algoritmos genéticos**: mimetizan la evolución natural para explorar eficientemente el espacio de soluciones.
- **Simulated annealing**: permite aceptar soluciones peores temporalmente (con probabilidad decreciente con la temperatura) para escapar de mínimos locales.

Todos comparten el objetivo de explorar el espacio de parámetros globalmente y cuantificar la [[Non-uniqueness|no-unicidad]], a diferencia de los métodos LS que convergen a una sola solución.

## Limitaciones

- Costo computacional elevado: $10^4$–$10^6$ evaluaciones del problema directo.
- La cobertura del espacio de parámetros depende de la parametrización del modelo (número de capas, rangos de búsqueda): una parametrización inadecuada puede sesgar la distribución de soluciones.
- El test estadístico de aceptación requiere conocer la incertidumbre de los datos $\sigma_i$; si ésta no está bien estimada, el número de modelos aceptables puede estar sesgado.

## Referencias

- Socco, L.V., Boiero, D. (2008), *Near Surface Geophysics*.
- Foti et al. (2014), Cap. 6.1.3 (estrategias local vs global), Cap. 6.4.3 (búsqueda global), Cap. 7.2.4 (ejemplo La Salle), pp. 280–310, 371–374.
