---
name: Fisher Test
description: Test estadístico F para determinar si el desajuste de un modelo es estadísticamente aceptable — usado en inversión de Monte Carlo [[MASW Method|MASW]] para seleccionar el ensemble de modelos equivalentes
type: reference
---

# Fisher Test — Test F de Fisher

> [!CONCEPT] Definición
> El **Test F de Fisher** (o *F-test*) es una prueba de hipótesis estadística que compara dos varianzas o determina si el desajuste de un modelo dado es estadísticamente compatible con el desajuste mínimo — usado en [[Monte Carlo Methods|inversión de Monte Carlo]] de [[Dispersion Curve|curvas de dispersión]] para seleccionar el **ensemble de modelos equivalentes**. En el contexto de ondas superficiales, el test F de Fisher establece el umbral de aceptación $\phi_{acc}$:
> $$\phi_{acc} = \phi_{min} \left[1 + \frac{N_p}{N - N_p} F_{N_p, N-N_p, \alpha}\right]$$
> donde $\phi_{min}$ es el misfit mínimo del mejor modelo, $N_p$ es el número de parámetros del modelo, $N$ es el número de datos de dispersión, y $F_{N_p, N-N_p, \alpha}$ es el valor crítico de la distribución F con $(N_p, N - N_p)$ grados de libertad al nivel de significancia $\alpha$ (típicamente $\alpha = 0.05$ → 95% de confianza). Un modelo es **aceptable** si $\phi \leq \phi_{acc}$ — es decir, si su desajuste no es estadísticamente peor que el del mejor modelo al nivel de confianza especificado. El conjunto de modelos aceptables define el **espacio de soluciones equivalentes**, que cuantifica la [[Non-uniqueness|no-unicidad]] del problema inverso. Está estrechamente relacionado con el [[Chi-Squared Test|test chi-cuadrado]], que es la versión normalizada del mismo criterio cuando los errores de los datos son gaussianos independientes.
>
> — Foti et al. (2018), §7.2.4; Menke (2012), *Geophysical Data Analysis*; Socco & Boiero (2008).

## Relación con el chi-cuadrado

Para errores gaussianos independientes con varianzas $\sigma_i^2$, el misfit normalizado es:
$$\phi = \chi^2 = \sum_{i=1}^N \frac{(c_R^{obs}(f_i) - c_R^{calc}(f_i))^2}{\sigma_i^2}$$

El test F compara si $\phi/\phi_{min}$ excede el umbral crítico de la distribución F — equivalente a comparar $\chi^2$ del modelo con $\chi^2_{crit}$.

## Aplicación práctica en Monte Carlo [[MASW Method|MASW]]

Para la inversión de Monte Carlo del sitio La Salle (Foti et al. 2018):
- $N = 30$ puntos de dispersión
- $N_p = 15$ parámetros ($V_S$ de 15 capas)
- $\alpha = 0.05$: $F_{15, 15, 0.05} \approx 2.40$
- $\phi_{acc} = \phi_{min} \cdot (1 + 15/15 \cdot 2.40) = 3.40 \cdot \phi_{min}$

Modelos con misfit hasta ~3.4× el del mejor modelo son estadísticamente aceptables al 95% de confianza.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — test F para ensemble de modelos en La Salle
> Foti et al. (2018, §7.2.4) aplican el test F de Fisher para seleccionar el subconjunto de modelos aceptables del Monte Carlo de inversión del sitio La Salle. De 100,000 modelos generados aleatoriamente, ~500 (0.5%) satisfacen $\phi \leq \phi_{acc}$ con $\alpha = 0.05$. La dispersión del $V_{S,30}$ entre los 500 modelos aceptables es 480–505 m/s (CV ~2.5%), confirmando que el $V_{S,30}$ está bien determinado pese a la [[Non-uniqueness|no-unicidad]] del perfil $V_S(z)$ completo. El test F es equivalente al [[Chi-Squared Test]] cuando los errores son gaussianos e independientes — diferencia técnica: el F-test compara $\phi_{modelo}$ con $\phi_{min}$ (referencia relativa), mientras que el $\chi^2$ compara $\phi$ con el valor esperado bajo la hipótesis nula (referencia absoluta).
>
> — Foti et al. (2018), §7.2.4, pp. 363–374; Socco & Boiero (2008), *Geophysics*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.2.4 — test F en Monte Carlo La Salle |
| Socco & Boiero (2008), *Geophysics* | Inversión Monte Carlo de ondas superficiales con test F |
| Menke (2012), *Geophysical Data Analysis* | §7 — estadística del test F en geofísica |
