---
name: Chi-Squared Test
description: Test estadístico para evaluar el ajuste de la [[Dispersion Curve|curva de dispersión]] calculada vs observada — criterio de aceptación/rechazo de modelos VS en inversión [[MASW Method|MASW]]
type: reference
---

# Chi-Squared Test — Test Chi-Cuadrado ($\chi^2$)

> [!CONCEPT] Definición
> El **Test Chi-Cuadrado ($\chi^2$)** es la prueba estadística que evalúa si el ajuste entre los datos observados y los datos calculados por un modelo es consistente con la incertidumbre experimental — es decir, si el modelo es estadísticamente aceptable. En la [[Inversión|inversión]] de [[Dispersion Curve|curvas de dispersión]] de [[MASW Method|MASW]], el estadístico chi-cuadrado se define como:
> $$\chi^2 = \sum_{i=1}^{N} \left(\frac{c_R^{obs}(f_i) - c_R^{calc}(\mathbf{m}, f_i)}{\sigma_{c_R}(f_i)}\right)^2$$
> donde $N$ es el número de puntos de la [[Dispersion Curve|curva de dispersión]], $\sigma_{c_R}(f_i)$ es la incertidumbre (desviación estándar) del [[Picking|picking]] a la frecuencia $f_i$, y $\mathbf{m}$ es el modelo $V_S(z)$ candidato. Bajo la hipótesis de que el modelo es correcto y los errores son gaussianos independientes, $\chi^2$ sigue una distribución chi-cuadrado con $N$ grados de libertad, con valor esperado $E[\chi^2] = N$. El **chi-cuadrado reducido** $\tilde{\chi}^2 = \chi^2/N \approx 1$ para un ajuste óptimo. El test $\chi^2$ es el criterio de aceptación en los métodos de búsqueda global ([[Monte Carlo Methods]], [[Neighbourhood Algorithm]]): un modelo es **aceptable** si $\chi^2 \leq \chi^2_{crit}$ donde $\chi^2_{crit}$ se fija con el [[First-Order Second-Moment Method|nivel de confianza]] deseado (p.ej., $\chi^2_{crit} = \chi^2_{N, 0.05}$ para 95% de confianza).
>
> — Foti et al. (2018), §6.5; Tarantola (2005), §3.5; Park et al. (1999).

## Uso en inversión estocástica

### Criterio de Fisher (F-test)

Para [[Monte Carlo Methods|inversión de Monte Carlo]], el modelo de referencia $\mathbf{m}_{ref}$ (mejor ajuste, misfit mínimo $\phi_{min}$) define el umbral de aceptación mediante el **F-test**:

$$\phi_{acc} = \phi_{min} \left[1 + \frac{N_p}{N - N_p} F_{N_p, N-N_p, \alpha}\right]$$

donde $N_p$ es el número de parámetros del modelo y $F_{N_p, N-N_p, \alpha}$ es el valor crítico de la distribución F al nivel de significancia $\alpha$. Para $\alpha = 0.05$ (95% de confianza), el umbral $\phi_{acc}$ es ligeramente mayor que $\phi_{min}$, permitiendo un **ensemble de modelos aceptables** que cuantifican la [[Non-uniqueness|no-unicidad]] del problema.

### Chi-cuadrado vs misfit absoluto

| Criterio | Fórmula | Dependencia de $\sigma_{c_R}$ | Uso |
|---------|---------|------|-----|
| $\chi^2$ | $\sum(r_i/\sigma_i)^2$ | Sí (normalizado) | Comparación estadística rigurosa |
| RMSE | $\sqrt{\sum r_i^2 / N}$ | No | Comparación de ajuste absoluto |
| Misfit relativo | $\sum|r_i/c_R^{obs}(f_i)|$ | No | Peso uniforme por frecuencia |

## Implicaciones para el número de modelos aceptables

El número de modelos $\mathbf{m}$ que satisfacen $\chi^2 \leq \chi^2_{crit}$ define el **ensemble de modelos equivalentes** — el conjunto de perfiles $V_S(z)$ que son indistinguibles estadísticamente dada la incertidumbre de los datos. La dispersión de este ensemble (su varianza) cuantifica la incertidumbre del perfil invertido.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — chi-cuadrado en [[Monte Carlo Methods|Monte Carlo]] La Salle
> Foti et al. (2018, §7.2.4) aplican el criterio chi-cuadrado al [[Monte Carlo Methods|Monte Carlo]] de inversión del sitio La Salle. Con $N$ = 30 puntos de dispersión y $\sigma_{c_R}$ = 5–15 m/s (estimada del [[Picking|picking]] de múltiples disparos), el umbral de aceptación es $\chi^2_{crit}(30, 0.05) \approx 43.8$. De 100,000 modelos [[Monte Carlo Methods|Monte Carlo]] muestreados, ~500 (0.5%) satisfacen $\chi^2 \leq 43.8$. La dispersión del $[[Vs30|Vs,30]]$ entre los 500 modelos aceptables es 480–505 m/s (coeficiente de variación ~2.5%), confirmando que el $[[Vs30|Vs,30]]$ es bien determinado pese a la [[Non-uniqueness|no-unicidad]] del perfil $V_S(z)$ completo. Los modelos con $\chi^2$ cerca del mínimo son el mode fundamental; los modelos con $\chi^2$ mayor pero aún aceptable tienen estructuras de capas más complejas (inversiones de velocidad, capas delgadas) que no se pueden distinguir con los datos disponibles.
>
> — Foti et al. (2018), §7.2.4, pp. 363–371, Figs. 7.20–7.23.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.5, §7.2.4 — chi-cuadrado en inversión [[MASW Method|MASW]] |
| Tarantola (2005), *Inverse Problem Theory* | §3.5 — test estadístico en inversión |
| Park, Miller & Xia (1999), *Geophysics* | Paper 001 — ajuste de [[Dispersion Curve|curva de dispersión]] [[MASW Method|MASW]] |
