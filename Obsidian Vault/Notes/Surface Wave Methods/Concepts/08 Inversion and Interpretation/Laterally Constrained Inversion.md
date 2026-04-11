---
name: Laterally Constrained Inversion
description: Inversión que acopla lateralmente los modelos 1D adyacentes de una sección 2D de VS — produce secciones más suaves y geológicamente consistentes que la inversión independiente de cada ventana
type: reference
---

# Laterally Constrained Inversion (LCI) — Inversión Lateralmente Restringida

> [!CONCEPT] Definición
> La **Inversión Lateralmente Restringida** (*Laterally Constrained Inversion*, LCI) es una extensión de la inversión 1D de la [[Dispersion Curve|curva de dispersión]] al caso 2D ([[Sliding Window|MASW rolling]]): en lugar de invertir cada perfil 1D de forma independiente, el LCI acopla los parámetros de modelos adyacentes mediante una **penalización de la variación lateral**, produciendo secciones pseudo-2D de $V_S$ más continuas y geológicamente consistentes. La función objetivo del LCI es:
> $$\Phi_{LCI} = \sum_{j=1}^{N_{pos}} \|\mathbf{d}_j - F(\mathbf{m}_j)\|^2 + \lambda_v \sum_{j=1}^{N_{pos}} \|\mathbf{R}\mathbf{m}_j\|^2 + \lambda_l \sum_{j=1}^{N_{pos}-1} \|\mathbf{m}_{j+1} - \mathbf{m}_j\|^2$$
> donde el primer término es el misfit de los datos de dispersión en cada posición $j$, el segundo es la [[Regularization|regularización]] vertical ([[Tikhonov Regularization]]) que penaliza la rugosidad de cada perfil 1D, y el tercer término es la **[[Regularization|regularización]] lateral** que penaliza la diferencia entre perfiles adyacentes con peso $\lambda_l$. El LCI produce secciones con transiciones suavizadas entre perfiles, suprimiendo artefactos de la inversión independiente; su limitación es que puede suavizar heterogeneidades laterales abruptas reales.
>
> — Foti et al. (2018), §7.5; Auken & Christiansen (2004); Bergamo et al. (2016).

## Implementación práctica

### Sistema aumentado

El LCI se implementa como un problema de [[Inversión|inversión]] linealizado aumentado que combina todos los perfiles en un único sistema:

$$\begin{pmatrix} \mathbf{J}_1 & & \\ & \ddots & \\ & & \mathbf{J}_{N} \end{pmatrix} \begin{pmatrix} \delta\mathbf{m}_1 \\ \vdots \\ \delta\mathbf{m}_N \end{pmatrix} + \lambda_l \mathbf{L} \begin{pmatrix} \mathbf{m}_1 \\ \vdots \\ \mathbf{m}_N \end{pmatrix} = \begin{pmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_N \end{pmatrix}$$

donde $\mathbf{L}$ es el operador de diferencias laterales de primer orden y $\mathbf{J}_j$ es el Jacobiano de cada perfil.

### Selección del parámetro de acoplamiento lateral $\lambda_l$

- $\lambda_l \to 0$: sin restricción lateral → equivalente a inversiones independientes (sección ruidosa)
- $\lambda_l \to \infty$: máximo acoplamiento → todos los perfiles idénticos (sección constante lateralmente)
- Valor óptimo: balanceado por la variación geológica esperada — generalmente $\lambda_l \approx \lambda_v$ si la resolución lateral y vertical son comparables

## Comparación con inversión independiente

| Aspecto | Inversión 1D independiente | LCI |
|---------|---------------------------|-----|
| Continuidad lateral | No garantizada | Suavizada por $\lambda_l$ |
| Artefactos de salto | Posibles | Suprimidos |
| Resolución de fallas abruptas | Buena (por perfil) | Atenuada por suavizado |
| Costo computacional | Bajo ($N$ inversiones 1D) | Mayor (sistema aumentado) |
| Coherencia geológica | Baja | Alta |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — LCI en sección pseudo-2D del sitio La Salle
> Foti et al. (2018, §7.5, Figs. 7.35–7.36) aplican la LCI a los datos de [[Ground Roll|ground-roll]] del sitio La Salle procesados con [[Sliding Window|ventana deslizante]] de ~50 m y paso de 5 m. La sección pseudo-2D de $V_S$ resultante (Fig. 7.35) muestra variaciones laterales suaves entre 200–400 m/s en los primeros 30 m, con mayor detalle en las heterogeneidades laterales respecto a una sección de inversión 1D sin restricciones. La comparación con la sección de reflexión sísmica (Fig. 7.36) confirma que las variaciones de $V_S$ correlacionan con las unidades estratigráficas visibles en los reflectores — validando que el LCI reproduce la geología real sin suprimir las variaciones significativas (las heterogeneidades laterales en La Salle son de escala > 50 m, mayor que la longitud de ventana, por lo que el LCI no las suprime).
>
> — Foti et al. (2018), §7.5, pp. 384–392, Figs. 7.35–7.36.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.5 — LCI en secciones pseudo-2D [[MASW Method|MASW]] rolling |
| Auken & Christiansen (2004), *Geophysics* | Formulación original del LCI para métodos EM |
| Bergamo et al. (2016), *Near Surface Geophysics* | Aplicación del LCI a [[MASW Method|MASW]] rodante con grupos de geófonos |
