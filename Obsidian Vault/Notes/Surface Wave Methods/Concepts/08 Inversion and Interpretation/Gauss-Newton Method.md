---
name: Gauss-Newton Method
description: Algoritmo de inversión no lineal iterativo que aproxima el Hessiano como JᵀJ — base del método de Levenberg-Marquardt para inversión de [[Dispersion Curve|curvas de dispersión]] [[MASW Method|MASW]] con convergencia cuadrática
type: reference
---

# Gauss-Newton Method — Método de Gauss-Newton

> [!CONCEPT] Definición
> El **método de Gauss-Newton** es un algoritmo iterativo para resolver problemas de mínimos cuadrados no lineales de la forma $\min_{\mathbf{m}} \|\mathbf{d} - \mathbf{f}(\mathbf{m})\|^2$. En cada iteración $k$, la función forward $\mathbf{f}(\mathbf{m})$ se linealiza alrededor del modelo actual $\mathbf{m}_k$:
> $$\mathbf{f}(\mathbf{m}_k + \delta\mathbf{m}) \approx \mathbf{f}(\mathbf{m}_k) + \mathbf{J}_k \, \delta\mathbf{m}$$
> donde $\mathbf{J}_k = \partial \mathbf{f}/\partial \mathbf{m}|_{\mathbf{m}_k}$ es la [[Jacobian Matrix|matriz Jacobiana]]. La actualización $\delta\mathbf{m}$ se obtiene resolviendo el sistema normal:
> $$(\mathbf{J}_k^T \mathbf{J}_k) \, \delta\mathbf{m} = \mathbf{J}_k^T \mathbf{r}_k$$
> donde $\mathbf{r}_k = \mathbf{d} - \mathbf{f}(\mathbf{m}_k)$ es el residuo. La aproximación clave es que el Hessiano $\nabla^2 F \approx \mathbf{J}^T \mathbf{J}$ (se ignoran los términos de segundo orden en el residuo). En la inversión de [[Dispersion Curve|curvas de dispersión]], el modelo actualizado es $\mathbf{m}_{k+1} = \mathbf{m}_k + \delta\mathbf{m}$. El método converge cuadráticamente cerca del mínimo pero puede divergir si el modelo inicial está lejos de la solución. El [[Levenberg-Marquardt|método de Levenberg-Marquardt]] lo estabiliza agregando un término de regularización $\lambda \mathbf{I}$:
> $$(\mathbf{J}^T \mathbf{J} + \lambda \mathbf{I}) \, \delta\mathbf{m} = \mathbf{J}^T \mathbf{r}$$
>
> — Foti et al. (2018), §6.2.1, pp. 272–276; Nocedal & Wright (2006), *Numerical Optimization*, §10.

## Versión con pesos (datos con incertidumbre)

Cuando los datos tienen incertidumbres $\sigma_i$ no uniformes, se usa la forma ponderada:

$$(\mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{J}) \, \delta\mathbf{m} = \mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{r}$$

donde $\mathbf{C}_d = \text{diag}(\sigma_1^2, \ldots, \sigma_N^2)$ es la matriz de covarianza de los datos. Esta forma aparece en el [[First-Order Second-Moment Method|método FOSM]] para propagación de incertidumbre.

## Convergencia y limitaciones

- **Convergencia cuadrática** cerca del mínimo (si $\nabla^2 F \approx \mathbf{J}^T \mathbf{J}$)
- **Inestabilidad** lejos del mínimo: la aproximación del Hessiano puede ser indefinida
- **Dependencia del modelo inicial**: problemas con múltiples mínimos locales (ver [[Non-uniqueness]])
- **Costo computacional**: requiere evaluar $\mathbf{J}$ en cada iteración — $O(NM)$ evaluaciones del forward por iteración

En la práctica de inversión [[MASW Method|MASW]], se requieren tipicamente 5–20 iteraciones de Gauss-Newton para convergencia a $\chi^2 \approx N$ (Foti et al. 2018).

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — Gauss-Newton para inversión [[MASW Method|MASW]] en superficie
> Xia et al. (1999, *Geophysics* 64(3), 691–700) presentan el primer algoritmo completo de inversión [[MASW Method|MASW]] basado en Gauss-Newton para obtener $V_S(z)$ a partir de la [[Dispersion Curve|curva de dispersión]] de Rayleigh. Utilizan la formulación de matrices de transferencia (Thomson-Haskell) para el forward y derivadas parciales analíticas para la Jacobiana. La inversión de modelos sintéticos con ruido muestra convergencia en < 10 iteraciones para modelos iniciales dentro del 20% del modelo real. Para el sitio de campo en Kansas (suelos aluviales), el perfil $V_S$ converge de un modelo inicial homogéneo a un perfil con $V_S$ creciente de 180 m/s (superficie) a 350 m/s (5 m) — consistente con el log de un sondeo SPT adyacente (correlación > 85%). Este trabajo establece el Gauss-Newton como el algoritmo estándar de inversión lineal local para [[MASW Method|MASW]].
>
> — Research Database (Paper 002 — Xia et al. 1999); Foti et al. (2018), §6.2.1, pp. 272–276.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.1 — inversión linealizada iterativa |
| Xia et al. (1999), *Geophysics* 64(3), 691–700 | Implementación Gauss-Newton para [[MASW Method|MASW]] |
| Nocedal & Wright (2006), *Numerical Optimization* | §10 — método de Gauss-Newton y Levenberg-Marquardt |
