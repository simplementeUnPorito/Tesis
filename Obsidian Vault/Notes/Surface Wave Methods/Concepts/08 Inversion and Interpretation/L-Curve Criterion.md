---
name: L-Curve Criterion
description: Criterio gráfico para seleccionar el parámetro de regularización óptimo λ en inversión de Tikhonov — basado en la curva log||Jm-d|| vs log||Lm|| cuyo punto de máxima curvatura ("esquina de la L") balancea ajuste y suavidad
type: reference
---

# L-Curve Criterion — Criterio de la Curva-L

> [!CONCEPT] Definición
> El **criterio de la curva-L** es un método gráfico para seleccionar el **parámetro de regularización** $\lambda$ óptimo en la [[Regularization|inversión regularizada de Tikhonov]]:
> $$\min_{\mathbf{m}} \|\mathbf{J}\mathbf{m} - \mathbf{d}\|^2 + \lambda^2 \|\mathbf{L}\mathbf{m}\|^2$$
> donde $\mathbf{L}$ es el operador de regularización (diferencias finitas de primer o segundo orden). La **curva-L** es el gráfico paramétrico en escala log-log:
> $$\left(\log \|\mathbf{J}\mathbf{m}(\lambda) - \mathbf{d}\|, \; \log \|\mathbf{L}\mathbf{m}(\lambda)\|\right) \quad \text{para } \lambda \in [0, \infty)$$
> Esta curva tiene forma de "L": el brazo vertical corresponde a modelos bien ajustados pero muy irregulares ($\lambda \to 0$), y el brazo horizontal a modelos muy suavizados con mal ajuste ($\lambda \to \infty$). La **esquina de la L** (*corner*) — punto de máxima curvatura — representa el $\lambda$ óptimo que balancea el ajuste a los datos con la suavidad del modelo. Es una alternativa al criterio de [[Chi-Squared Test|chi-cuadrado]] cuando las incertidumbres de los datos son desconocidas. En inversión de [[Dispersion Curve|curvas de dispersión]] de ondas superficiales, la curva-L permite seleccionar $\lambda$ sin necesidad de estimar $\sigma_i$ individualmente para cada punto de dispersión.
>
> — Foti et al. (2018), §6.2.3, pp. 283–287; Hansen (1992), *SIAM Review* 34(4), 561–580; Aster et al. (2013).

## Identificación de la esquina

La curvatura de la curva-L en función de $\lambda$ se calcula como:

$$\kappa(\lambda) = \frac{\xi' \eta'' - \xi'' \eta'}{[(\xi')^2 + (\eta')^2]^{3/2}}$$

donde $\xi = \log \|\mathbf{r}(\lambda)\|$, $\eta = \log \|\mathbf{L}\mathbf{m}(\lambda)\|$, y las primas denotan derivadas respecto a $\log\lambda$. El $\lambda$ óptimo corresponde al máximo de $\kappa(\lambda)$.

## Limitaciones del criterio

- La curva-L puede no tener una esquina bien definida para ciertos problemas (curva suave sin inflexión clara)
- Para datos con ruido heterocedástico, la curva-L puede sobreestimar $\lambda$ respecto al criterio $\chi^2$
- El método asume que $\lambda$ está en el rango donde el compromiso ajuste-suavidad es relevante — si la curva es monotónica, otro criterio es más apropiado

## Comparación con criterios alternativos

| Criterio | Requiere $\sigma_i$ | Computacional | Robustez |
|----------|--------------------|--------------|---------  |
| L-Curve | No | Media (barrido en λ) | Media |
| [[Chi-Squared Test|Chi-cuadrado]] | Sí | Baja | Alta (con datos) |
| Validación cruzada (GCV) | No | Alta | Alta |
| Discrepancy principle | Sí (nivel de ruido) | Baja | Alta |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — curva-L en inversión del sitio Pisa
> Foti et al. (2018, §6.2.3, Fig. 6.12) aplican el criterio de la curva-L a la inversión regularizada de la [[Dispersion Curve|curva de dispersión]] del sitio de Torre de Pisa. El barrido de $\lambda$ de $10^{-3}$ a $10^3$ genera la curva-L en el espacio log-log con esquina bien definida en $\lambda^* \approx 0.1$. El modelo correspondiente reproduce los datos con misfit $\phi \approx 1.8 \phi_{\min}$ — dentro del rango aceptable del [[Fisher Test|test F de Fisher]]. Para $\lambda < 0.01$, el modelo muestra oscilaciones paramétricas artificiales (underfitting regularización); para $\lambda > 10$, el perfil $V_S$ es casi uniforme (overdamping). El $\lambda^*$ seleccionado por la curva-L es consistente con el valor obtenido por el criterio chi-cuadrado cuando se usan $\sigma_i$ estimadas de la variabilidad de la [[Dispersion Curve|curva de dispersión]] entre shots — confirmando la validez del criterio de la curva-L cuando los errores no son conocidos a priori.
>
> — Foti et al. (2018), §6.2.3, pp. 283–287, Fig. 6.12; Hansen (1992), *SIAM Review* 34(4), 561–580.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.3 — criterio L-Curve en inversión [[MASW Method|MASW]] |
| Hansen, P.C. (1992), *SIAM Review* 34(4), 561–580 | Definición formal del criterio de la curva-L |
| Aster, Borchers & Thurber (2013), *Parameter Estimation and Inverse Problems* | §4 — criterios de selección de λ |
