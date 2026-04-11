---
name: Levenberg-Marquardt
description: Algoritmo de optimización no-lineal que combina el método de Gauss-Newton con el gradiente descendente — estándar para la inversión local de curvas de dispersión MASW
type: reference
---

# Levenberg-Marquardt — Algoritmo de Levenberg-Marquardt (LM)

> [!CONCEPT] Definición
> El **Algoritmo de Levenberg-Marquardt (LM)** es un método de optimización no-lineal de mínimos cuadrados que combina la convergencia rápida del **método de Gauss-Newton** cerca del mínimo con la robustez del **gradiente descendente** lejos del mínimo. Se usa ampliamente en la [[Inversión|inversión]] de [[Dispersion Curve|curvas de dispersión]] de [[MASW Method|MASW]] como el algoritmo de búsqueda local más eficiente. La actualización iterativa del modelo es:
> $$\mathbf{m}_{k+1} = \mathbf{m}_k - (\mathbf{J}^T\mathbf{J} + \lambda_k \mathbf{I})^{-1} \mathbf{J}^T \mathbf{r}_k$$
> donde $\mathbf{J}$ es el Jacobiano (matriz de [[Sensitivity Kernel|sensibilidad]]), $\mathbf{r}_k = \mathbf{d} - F(\mathbf{m}_k)$ es el vector de residuos, y $\lambda_k$ es el **parámetro de amortiguamiento** que controla el balance entre Gauss-Newton ($\lambda_k \to 0$, paso completo en dirección Newton) y gradiente descendente ($\lambda_k \to \infty$, paso pequeño en dirección más pronunciada). Si la iteración reduce el misfit, $\lambda_k$ se reduce (más Gauss-Newton); si lo aumenta, $\lambda_k$ se incrementa (más gradiente). **Convergencia**: típicamente 5–20 iteraciones para problemas de dispersión de Rayleigh bien condicionados. **Limitación**: converge al mínimo local más cercano al modelo inicial — vulnerable a la [[Non-uniqueness|no-unicidad]] si el modelo inicial es pobre.
>
> — Levenberg (1944); Marquardt (1963); Xia et al. (1999), *Geophysics*; Foti et al. (2018), §6.4.2.

## Formulación para inversión de dispersión

### Jacobiano de la curva de dispersión

El Jacobiano es la matriz de derivadas parciales:

$$J_{if} = \frac{\partial c_R(f_i)}{\partial m_j}$$

donde $c_R(f_i)$ es la velocidad de Rayleigh a la frecuencia $f_i$ y $m_j$ es el $j$-ésimo parámetro del modelo (tipicamente $V_{S,j}$ de la capa $j$). El Jacobiano se calcula analíticamente para el modelo de capas planas o numéricamente por diferencias finitas.

### Selección del parámetro $\lambda_k$

Estrategia de Marquardt (1963):
- Si $\phi(\mathbf{m}_{k+1}) < \phi(\mathbf{m}_k)$: $\lambda_{k+1} = \lambda_k / 10$ (más Gauss-Newton)
- Si $\phi(\mathbf{m}_{k+1}) \geq \phi(\mathbf{m}_k)$: $\lambda_{k+1} = \lambda_k \times 10$ (más gradiente, descartar $\mathbf{m}_{k+1}$)

### Regularización combinada

En práctica, el LM se combina con [[Tikhonov Regularization|regularización]]:

$$\mathbf{m}_{k+1} = \mathbf{m}_k - (\mathbf{J}^T\mathbf{W}\mathbf{J} + \lambda_k \mathbf{I} + \mu \mathbf{R}^T\mathbf{R})^{-1} (\mathbf{J}^T\mathbf{W}\mathbf{r}_k + \mu \mathbf{R}^T\mathbf{R}\mathbf{m}_k)$$

donde $\mu$ controla la regularización y $\mathbf{W}$ pondera los datos por su incertidumbre.

## Comparación con otros optimizadores locales

| Método | Usa Hessiano | Convergencia | Robustez | Costo por iteración |
|--------|-------------|------------|---------|-----|
| Gradiente descendente | No | Lenta | Alta | Bajo |
| Gauss-Newton | Aproximado | Cuadrática (cerca mínimo) | Baja | Medio |
| **Levenberg-Marquardt** | Aproximado + amortiguado | Cuadrática-lineal | Media | Medio |
| Newton completo | Exacto | Cuadrática | Media | Alto |

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — LM como motor de inversión MASW estándar
> **Paper 002 (Xia, Miller & Park 1999)** implementa el Algoritmo de Levenberg-Marquardt como el motor de inversión del método MASW. En el sitio de Kansas (perfil VS de 150–400 m/s en 20 m), el LM converge en 5–10 iteraciones partiendo de un modelo inicial de velocidad constante. El paper reporta que: (1) la velocidad de onda S ($V_S$) domina la [[Sensitivity Kernel|sensibilidad]] de la velocidad de Rayleigh (80–95% vs VP y densidad combinados), lo que hace al problema bien condicionado para el LM; (2) el error entre el perfil VS invertido y el de referencia (sondeo sísmico) es < 15% en todo el perfil; (3) el parámetro de amortiguamiento LM $\lambda_0 = 0.1$ proporciona convergencia estable sin divergencia. Este paper estableció el LM como el estándar de facto para inversión local de MASW.
>
> — Research Database, entrada 002 (core); Xia, Miller & Park (1999), *Geophysics* 64(3):691–700.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.2, pp. 298–308 — inversión por gradiente MASW |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — implementación LM en inversión MASW |
| Levenberg (1944), *Quart. Appl. Math.* | Formulación original del método |
| Marquardt (1963), *SIAM J. Appl. Math.* | Algoritmo moderno de Levenberg-Marquardt |
