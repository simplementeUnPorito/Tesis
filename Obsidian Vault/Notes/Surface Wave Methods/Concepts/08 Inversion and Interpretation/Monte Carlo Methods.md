# Métodos de Monte Carlo (Monte Carlo Methods)

> [!CONCEPT] Definición
> Los **métodos de Monte Carlo** son estrategias de **búsqueda global** para la [[Inversión|inversión]] de ondas superficiales: generan una gran población de modelos $\mathbf{m}$ ([[Layered Media|perfiles de capas]] con $V_S$, $V_P$, $\rho$, $h$), evalúan el desajuste $E(\mathbf{m})$ de cada uno respecto a la curva de dispersión experimental, y seleccionan como *soluciones aceptables* aquellos con $E(\mathbf{m}) \leq E_{thr}$ según un test de Fisher al nivel de confianza elegido. A diferencia de los métodos locales (gradiente, Levenberg-Marquardt), no requieren modelo inicial ni jacobiano — exploran el espacio completo de parámetros. Su principal valor es **cuantificar la [[Non-uniqueness|no-unicidad]]**: en lugar de un único perfil, producen un *ensemble* de perfiles equivalentes cuya dispersión caracteriza la incertidumbre del resultado. El costo computacional es alto (10³–10⁶ evaluaciones del problema directo por corrida).
>
> — Foti et al. (2018), Cap. 6.1.3, p. 280; Cap. 6.4.3, p. 308; Cap. 7.2.4, pp. 371–374.

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

> [!EXAMPLE] Evidencia empírica: Bergamo et al. (2011) — Inversión Monte Carlo multimodal en sitios con basamento superficial
> **Paper 037 (Bergamo, Comina, Foti & Maraschini 2011, SDEE 31(3):530–534)** aplica inversión Monte Carlo multimodal a sitios de la red acelerométrica italiana con basamento superficial (Liguria, Sicilia) a profundidades de 5–20 m. El método usa el paquete SWAT (MATLAB, análisis f-k) y una búsqueda Monte Carlo que incluye simultáneamente todos los modos de dispersión observados **sin asignarlos a priori** a un número de modo específico — ventaja crítica cuando modos superiores son visibles pero el analista no puede identificarlos con certeza. La inversión multimodal sin asignación previa de modos produce perfiles VS con menor [[Non-uniqueness|no-unicidad]] que la inversión en modo fundamental. Los perfiles se validan con razones espectrales H/V (frecuencia de resonancia f₀ observada vs predicha). Conexión directa con [[Monte Carlo Methods|Monte Carlo]] + [[Surface Wave Modes|modos superiores]]: la combinación es más robusta que el modo fundamental solo.
>
> — Research Database, entrada 037 (core); Bergamo et al. (2011), *Soil Dyn. Earthq. Eng.* 31(3):530–534.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Monte Carlo en La Salle, VS30 robusto ante no-unicidad
> Foti et al. (2018, §7.2.4) aplican el algoritmo de Monte Carlo global (Socco & Boiero 2008) al sitio La Salle con el dataset activo+pasivo (48 geófonos, espaciado 1.5 m, rango 5–55 Hz). Se generan **$10^5$ modelos** aleatorios; el test de Fisher al 95% selecciona ~500 modelos aceptables. Los perfiles seleccionados concuerdan en las capas superficiales (<15 m) — bien constrenidas por la alta frecuencia del dataset — pero divergen sustancialmente a mayor profundidad, demostrando la [[Non-uniqueness|no-unicidad]] real del problema. Sin embargo, los espectros de respuesta sísmica 1D calculados para cada perfil aceptable son **prácticamente indistinguibles** (Fig. 7.21), y los valores de $V_{S,30}$ caen en el rango estrecho de **480–505 m/s** (Fig. 7.22) — todos en la misma clase de sitio EC8. El resultado demuestra que la no-unicidad de la solución $V_S(z)$ raramente compromete las decisiones de ingeniería basadas en $V_{S,30}$.
>
> — Foti et al. (2018), §7.2.4, pp. 371–374, Figs. 7.19–7.22.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6.1.3 (local vs global), Cap. 6.4.3, Cap. 7.2.4, pp. 280–374 |
| Socco & Boiero (2008), *Near Surface Geophys* | Algoritmo de Monte Carlo global con propiedades de escala |
| Olafsdottir, Erlingsson & Bessason (2020), *Geosciences* 10(8):322 | Paper 013 — MASWaves: herramienta open-source MATLAB para inversión Monte Carlo MASW; CC BY 4.0 |
| Bergamo et al. (2011), *SDEE* 31(3):530–534 | Paper 037 — Monte Carlo multimodal sin asignación previa; sitios con basamento superficial |
