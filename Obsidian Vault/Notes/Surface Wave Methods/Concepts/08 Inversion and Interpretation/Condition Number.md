---
name: Condition Number
description: Razón κ = σmax/σmin entre el mayor y menor valor singular de la [[Jacobian Matrix|matriz Jacobiana]] — mide el mal condicionamiento del sistema inverso y la amplificación de errores en la inversión de [[Dispersion Curve|curvas de dispersión]] [[MASW Method|MASW]]
type: reference
---

# Condition Number — Número de Condición

> [!CONCEPT] Definición
> El **número de condición** $\kappa(\mathbf{A})$ de una matriz $\mathbf{A}$ cuantifica la sensibilidad de la solución $\mathbf{x}$ de un sistema lineal $\mathbf{A}\mathbf{x} = \mathbf{b}$ a perturbaciones en $\mathbf{b}$:
> $$\kappa(\mathbf{A}) = \|\mathbf{A}\| \cdot \|\mathbf{A}^{-1}\| = \frac{\sigma_{\max}}{\sigma_{\min}}$$
> donde $\sigma_{\max}$ y $\sigma_{\min}$ son el mayor y menor valor singular de $\mathbf{A}$ (obtenidos de la [[Singular Value Decomposition|SVD]]). El significado físico es directo: una perturbación relativa $\|\delta\mathbf{b}\|/\|\mathbf{b}\|$ en los datos produce un error relativo $\|\delta\mathbf{x}\|/\|\mathbf{x}\| \leq \kappa \cdot \|\delta\mathbf{b}\|/\|\mathbf{b}\|$ en la solución. En la inversión de [[Dispersion Curve|curvas de dispersión]] de ondas superficiales, la [[Jacobian Matrix|matriz Jacobiana]] $\mathbf{J} = \partial \mathbf{c}_R/\partial \mathbf{V}_S$ tiene número de condición típico $\kappa \sim 10^3$–$10^5$ — lo que significa que errores del 1% en los datos pueden producir errores del 10³% en el perfil $V_S(z)$ sin [[Regularization|regularización]]. Esto es la manifestación cuantitativa del [[Ill-Posed Problem|mal condicionamiento]] del problema inverso de ondas superficiales y justifica la necesidad de [[Regularization|regularización]] (Tikhonov, Occam) o métodos de búsqueda global ([[Monte Carlo Methods|Monte Carlo]], [[Genetic Algorithm|algoritmos genéticos]]).
>
> — Foti et al. (2018), §6.2.2, pp. 276–283; Menke (2012), *Geophysical Data Analysis*, §5; Golub & Van Loan (2013).

## Interpretación geofísica

Para la [[Jacobian Matrix|Jacobiana]] de [[MASW Method|MASW]] con $N$ puntos de dispersión y $M$ parámetros $V_S$:

$$\kappa(\mathbf{J}) = \frac{\sigma_1}{\sigma_M} \qquad \text{donde } \sigma_1 \geq \sigma_2 \geq \ldots \geq \sigma_M$$

- $\sigma_1$ corresponde a la combinación de parámetros más observable en los datos (capas superficiales, frecuencias altas)
- $\sigma_M$ corresponde a la combinación menos observable (capas profundas, bajas frecuencias)
- $\kappa \gg 1$: el sistema es **mal condicionado** — pequeños errores en datos o en el modelo forward se amplifican $\kappa$ veces en la solución

## Relación con la resolución del modelo

El número de condición determina cuántos parámetros son resolubles:
- Si $\kappa < 10^p$: solo los primeros $p \cdot \log_{10}(\sigma_1/\sigma_\epsilon)$ valores singulares son significativos (donde $\sigma_\epsilon$ es el nivel de ruido)
- Valores singulares con $\sigma_i < \sigma_\epsilon \cdot \kappa$ son dominados por el ruido y deben truncarse (TSVD)

## Efecto de la [[Regularization|regularización]] en $\kappa$

La [[Regularization|regularización de Tikhonov]] modifica el sistema:
$$(\mathbf{J}^T\mathbf{J} + \lambda^2 \mathbf{L}^T\mathbf{L})\delta\mathbf{m} = \mathbf{J}^T\mathbf{r}$$

reduciendo efectivamente el número de condición a:
$$\kappa_{reg} = \frac{\sigma_1^2 + \lambda^2 \lambda_L^2}{\sigma_M^2 + \lambda^2 \lambda_M^2} \approx \frac{\sigma_1^2}{\lambda^2 \lambda_M^2} \quad (\lambda \to \infty)$$

donde $\lambda_L^2$ son los valores propios del operador de suavizado. El parámetro $\lambda$ controla el número de condición efectivo del sistema regularizado.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — número de condición en inversión La Salle
> Foti et al. (2018, §6.2.2, Fig. 6.10) calculan el espectro de valores singulares de $\mathbf{J}$ para la inversión del sitio La Salle (15 capas, 30 puntos de dispersión). El número de condición es $\kappa \approx 3 \times 10^3$: $\sigma_1 = 1.2 \times 10^3$ (sensibilidad a $V_S$ en las primeras capas) vs. $\sigma_{15} \approx 0.4$ (sensibilidad a las capas más profundas). Sin [[Regularization|regularización]], el sistema amplifica el 2% de incertidumbre de los datos hasta un 60% de error en $V_S$ de las capas profundas. Con [[Regularization|regularización]] de Occam ($\lambda^* = 0.15$ por el criterio $\chi^2 = N$), el número de condición efectivo se reduce a $\kappa_{reg} \approx 50$ — error de inversión reducido a < 5% en todas las capas.
>
> — Foti et al. (2018), §6.2.2, pp. 276–283, Fig. 6.10.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.2 — número de condición en inversión [[MASW Method|MASW]] |
| Menke, W. (2012), *Geophysical Data Analysis* | §5 — SVD y número de condición en geofísica |
| Golub & Van Loan (2013), *Matrix Computations* | §2.7 — definición y propiedades del número de condición |
