---
name: Singular Value Decomposition
description: Factorización de la matriz Jacobiana J=UΣVᵀ usada en inversión de ondas superficiales para analizar la resolución, el número de condición y construir la pseudo-inversa de Moore-Penrose para inversión estabilizada
type: reference
---

# Singular Value Decomposition — Descomposición en Valores Singulares (SVD)

> [!CONCEPT] Definición
> La **Descomposición en Valores Singulares** (SVD) es la factorización de cualquier matriz real $\mathbf{J}$ (dimensiones $N \times M$) en tres matrices:
> $$\mathbf{J} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$$
> donde $\mathbf{U}$ ($N \times N$) y $\mathbf{V}$ ($M \times M$) son matrices ortogonales (cuyos columnas son los **vectores singulares** izquierdos y derechos, respectivamente) y $\boldsymbol{\Sigma}$ ($N \times M$) es diagonal con elementos $\sigma_1 \geq \sigma_2 \geq \ldots \geq \sigma_r > 0$ llamados **valores singulares**. En la inversión de [[Dispersion Curve|curvas de dispersión]] de ondas superficiales, $\mathbf{J}$ es la [[Jacobian Matrix|matriz Jacobiana]] $\partial \mathbf{c}_R / \partial \mathbf{V}_S$, y la SVD permite analizar la resolución del sistema inverso. Los valores singulares pequeños corresponden a combinaciones de parámetros que no son observables en los datos — su razón con el mayor valor singular define el **[[Condition Number|número de condición]]** $\kappa = \sigma_1/\sigma_r$, indicador de mal condicionamiento. La **[[Moore-Penrose Pseudoinverse|pseudo-inversa de Moore-Penrose]]** se construye invirtiendo solo los valores singulares superiores a un umbral, eliminando las componentes inestables:
> $$\mathbf{J}^+ = \mathbf{V} \boldsymbol{\Sigma}^+ \mathbf{U}^T$$
>
> — Foti et al. (2018), §6.2.2, pp. 276–283; Menke (2012), *Geophysical Data Analysis*; Tarantola (2005).

## Aplicación en inversión de ondas superficiales

### Número de condición y mal condicionamiento

El número de condición $\kappa(\mathbf{J}) = \sigma_{\max}/\sigma_{\min}$ mide la sensibilidad del sistema inverso a perturbaciones en los datos:
- $\kappa < 10$: bien condicionado — inversión estable
- $\kappa \sim 10^2$–$10^4$: moderadamente mal condicionado — requiere regularización
- $\kappa > 10^6$: muy mal condicionado — valores singulares pequeños dominan el error

Para [[MASW Method|MASW]] típico ($N = 30$ puntos de dispersión, $M = 15$ parámetros $V_S$), $\kappa \sim 10^3$–$10^5$ — justificando la necesidad de [[Regularization|regularización de Tikhonov]] o [[Occam Algorithm|algoritmo de Occam]].

### Truncation SVD como regularización

La inversión regularizada por truncamiento SVD (*TSVD*) conserva solo los $p < r$ valores singulares más grandes:
$$\mathbf{m}_{TSVD} = \sum_{i=1}^{p} \frac{1}{\sigma_i} (\mathbf{u}_i^T \mathbf{d}) \mathbf{v}_i$$

La elección de $p$ controla el trade-off resolución-estabilidad — equivalente conceptualmente al parámetro de regularización $\lambda$ en Tikhonov.

### Análisis de resolución

La matriz de resolución del modelo $\mathbf{R}_m = \mathbf{V}_p \mathbf{V}_p^T$ (con $\mathbf{V}_p$ la submatriz de los $p$ vectores singulares derechos) describe qué combinaciones de parámetros son resolubles. En [[MASW Method|MASW]], la diagonal de $\mathbf{R}_m$ muestra alta resolución en las capas más superficiales (frecuencias altas) y baja resolución en capas profundas (frecuencias bajas).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — SVD en inversión linealizada del sitio La Salle
> Foti et al. (2018, §6.2.2) aplican la SVD a la matriz Jacobiana de la inversión linealizada del sitio La Salle (Fig. 6.10). Para un modelo de 15 capas con datos a 4–40 Hz, los valores singulares decaen 3 órdenes de magnitud de $\sigma_1 \approx 10^3$ a $\sigma_{15} \approx 1$, dando $\kappa \approx 10^3$. El análisis de los vectores singulares muestra que los primeros 8 valores singulares corresponden a capas bien resolubles (0–15 m), mientras los últimos 7 son prácticamente inobservables (>20 m). La TSVD con $p = 10$ produce un modelo estable que reproduce los datos con $\chi^2 \approx N = 30$ — validando que 10 combinaciones lineales de $V_S$ son suficientes para explicar los datos a la calidad de medición.
>
> — Foti et al. (2018), §6.2.2, pp. 276–283, Figs. 6.10–6.11.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.2 — SVD en inversión de ondas superficiales |
| Menke, W. (2012), *Geophysical Data Analysis* | §3 — SVD en problemas inversos geofísicos |
| Tarantola, A. (2005), *Inverse Problem Theory* | §2 — SVD y resolución del modelo |
