---
name: Moore-Penrose Pseudoinverse
description: Generalización de la inversa matricial J⁺=VΣ⁺Uᵀ para matrices no cuadradas o singulares — solución de mínima norma al problema de mínimos cuadrados en inversión de [[Surface Waves|ondas superficiales]] — obtenida de la SVD truncando valores singulares pequeños
type: reference
---

# Moore-Penrose Pseudoinverse — Pseudo-inversa de Moore-Penrose

> [!CONCEPT] Definición
> La **pseudo-inversa de Moore-Penrose** $\mathbf{J}^+$ de una matriz $\mathbf{J}$ (dimensiones $N \times M$, con $N > M$ típicamente en inversión geofísica) es la **única** matriz que satisface las cuatro condiciones de Moore-Penrose y entrega la **solución de mínima norma** al problema de mínimos cuadrados $\min_{\mathbf{m}} \|\mathbf{J}\mathbf{m} - \mathbf{d}\|^2$. Se construye directamente a partir de la [[Singular Value Decomposition|SVD]] $\mathbf{J} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T$:
> $$\mathbf{J}^+ = \mathbf{V} \boldsymbol{\Sigma}^+ \mathbf{U}^T$$
> donde $\boldsymbol{\Sigma}^+$ es la transpuesta de $\boldsymbol{\Sigma}$ con cada valor singular no nulo $\sigma_i$ reemplazado por su recíproco $1/\sigma_i$ (y ceros donde $\sigma_i = 0$ o $\sigma_i < \sigma_{threshold}$). La solución de mínima norma es:
> $$\mathbf{m}^+ = \mathbf{J}^+ \mathbf{d} = \sum_{i=1}^{r} \frac{1}{\sigma_i} (\mathbf{u}_i^T \mathbf{d}) \, \mathbf{v}_i$$
> donde $r$ es el rango de $\mathbf{J}$. En la inversión de [[Dispersion Curve|curvas de dispersión]], los valores singulares pequeños de $\mathbf{J}$ corresponden a parámetros $V_S$ mal determinados (capas profundas); incluirlos en $\mathbf{J}^+$ amplifica el ruido de medición. La **TSVD** (Truncated SVD) reemplaza $\mathbf{J}^+$ con una versión truncada que incluye solo los $p$ valores singulares más grandes, equivalente a [[Regularization|regularización]] suave del sistema inverso.
>
> — Foti et al. (2018), §6.2.2, pp. 276–283; Menke (2012), *Geophysical Data Analysis*, §3; Penrose (1955), *Proc. Cambridge Phil. Soc.* 51.

## Propiedades clave

Las cuatro condiciones de Moore-Penrose que definen $\mathbf{J}^+$ de forma única:
1. $\mathbf{J} \mathbf{J}^+ \mathbf{J} = \mathbf{J}$
2. $\mathbf{J}^+ \mathbf{J} \mathbf{J}^+ = \mathbf{J}^+$
3. $(\mathbf{J} \mathbf{J}^+)^T = \mathbf{J} \mathbf{J}^+$
4. $(\mathbf{J}^+ \mathbf{J})^T = \mathbf{J}^+ \mathbf{J}$

Para matrices de rango completo ($r = M$): $\mathbf{J}^+ = (\mathbf{J}^T\mathbf{J})^{-1}\mathbf{J}^T$ (pseudo-inversa por la izquierda). Para matrices de rango deficiente: solo la SVD garantiza la solución correcta.

## Relación con la inversión regularizada

La pseudo-inversa regularizada de Tikhonov tiene la forma SVD:
$$\mathbf{m}_{Tikh} = \sum_{i=1}^{r} \frac{\sigma_i}{\sigma_i^2 + \lambda^2} (\mathbf{u}_i^T \mathbf{d}) \, \mathbf{v}_i$$

Los factores $f_i = \sigma_i^2/(\sigma_i^2 + \lambda^2)$ son los **filtros de [[Regularization|regularización]] de Tikhonov**: $f_i \to 1$ cuando $\sigma_i \gg \lambda$ (parámetro bien resuelto) y $f_i \to 0$ cuando $\sigma_i \ll \lambda$ (parámetro mal resuelto). La TSVD usa $f_i = 1$ para $i \leq p$ y $f_i = 0$ para $i > p$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — TSVD en inversión de Rayleigh con 15 capas
> Foti et al. (2018, §6.2.2) aplican la TSVD con $p = 10$ a la inversión del sitio La Salle (15 capas, $\kappa \approx 3\times10^3$). La pseudo-inversa truncada $\mathbf{J}_{TSVD}^+$ omite los 5 valores singulares más pequeños ($\sigma_{11}$ a $\sigma_{15}$, todos < 5 veces el nivel de ruido estimado $\epsilon/\|\mathbf{d}\| \approx 2\%$). El modelo recuperado reproduce los datos con $\chi^2 = 31 \approx N = 30$ (ajuste estadísticamente aceptable) y muestra perfil $V_S$ consistente con el SCPT en las primeras 15 m. Para capas > 20 m (controladas por $\sigma_{11}$–$\sigma_{15}$), la TSVD fuerza $\delta V_S \to 0$ — reconociendo explícitamente la falta de sensibilidad de los datos de dispersión a esas profundidades.
>
> — Foti et al. (2018), §6.2.2, pp. 276–283; Menke (2012), *Geophysical Data Analysis*, §3.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.2 — TSVD en inversión [[MASW Method|MASW]] |
| Penrose, R. (1955), *Proc. Cambridge Phil. Soc.* 51 | Definición original de la pseudo-inversa |
| Menke, W. (2012), *Geophysical Data Analysis* | §3 — SVD, TSVD y [[Regularization|regularización]] |
