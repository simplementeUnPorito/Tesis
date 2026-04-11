---
name: Dispersion Relation
description: ω(k); función que relaciona frecuencia angular con [[Wavenumber|número de onda]]; codifica la física del medio; implícita y no analítica para Rayleigh en medios estratificados; obtenida de la condición de solución no trivial del sistema de transferencia matricial
type: reference
---

# Relación de Dispersión (Dispersion Relation)

> [!CONCEPT] Definición
> La **relación de dispersión** $\omega(k)$ codifica cómo las propiedades elásticas del medio restringen los pares $(\omega, k)$ posibles para una onda propagante. En medios homogéneos es lineal (no dispersiva); en medios [[Layered Media|estratificados]] es no lineal e implícita: se obtiene como la condición de que el determinante de la matriz de transferencia Thomson-Haskell sea cero. Su evaluación numérica produce la [[Dispersion Curve|curva de dispersión]] teórica que se compara con la experimental en la [[Inversión|inversión]].
>
> — Foti et al. (2018), §2.1.2, pp. 41–43; §2.2.2–2.2.3, pp. 55–62.

## Intuición física

El medio elástico actúa como un filtro que solo permite la existencia de ondas cuya combinación $(\omega, k)$ satisfaga las ecuaciones de movimiento y las condiciones de contorno. Si un par $(\omega, k)$ viola la relación de dispersión, la perturbación no puede propagarse coherentemente — se disipa o no se excita. La relación de dispersión es, por tanto, la "lista de frecuencias y velocidades permitidas" para el medio.

En un semiespacio homogéneo: $\omega = V_P k$ para ondas P y $\omega = V_S k$ para ondas S — relaciones lineales, [[Elastic Half Space|no dispersivas]]. En un medio estratificado, la mezcla de propiedades con la profundidad introduce una no-linealidad: la [[Phase Velocity|velocidad de fase]] $c_p = \omega/k$ depende de $\omega$ (o equivalentemente de $k$).

## Forma general y sus derivadas

La relación de dispersión:

$$\omega = \omega(k)$$

define dos velocidades características:

$$c_p(k) = \frac{\omega(k)}{k} \quad \text{([[Phase Velocity|velocidad de fase]])}$$

$$c_g(k) = \frac{d\omega}{dk} \quad \text{([[Group Velocity|velocidad de grupo]])}$$

El medio es **no dispersivo** si $\omega \propto k$ (lineal), en cuyo caso $c_p = c_g = \text{const}$. Es **dispersivo** si la relación es no lineal, con $c_p \neq c_g$.

## Relación de dispersión para ondas de Rayleigh: el semiespacio homogéneo

En un [[Elastic Half Space|semiespacio elástico homogéneo]], la relación de dispersión de Rayleigh se obtiene de la condición de esfuerzo libre en la superficie y el requisito de amplitud decreciente con la profundidad. Es la ecuación secular:

$$\left(2 - \frac{c_R^2}{V_S^2}\right)^2 - 4\sqrt{1 - \frac{c_R^2}{V_P^2}}\,\sqrt{1 - \frac{c_R^2}{V_S^2}} = 0$$

Esta ecuación es independiente de $k$: $c_R$ es constante (no depende de la frecuencia ni de $k$). El semiespacio homogéneo es **no dispersivo** para ondas de Rayleigh.

## Relación de dispersión en medios estratificados: Thomson-Haskell

En un [[Layered Media|medio estratificado]] (n capas sobre un semiespacio), la relación de dispersión ya no tiene forma analítica cerrada. Se obtiene numéricamente como la condición:

$$\det[\mathbf{T}(\omega, k)] = 0$$

donde $\mathbf{T}(\omega, k)$ es la **matriz de transferencia global** de Thomson-Haskell, que propaga las condiciones de contorno (continuidad de desplazamiento y tracción) desde el semiespacio inferior hasta la superficie libre. Para cada valor de $\omega$, se buscan los valores de $k$ (o equivalentemente $c_p = \omega/k$) que anulan el determinante.

Las soluciones discretas del determinante para cada $\omega$ son los **modos de propagación** (modo fundamental y modos superiores). Cada modo tiene su propia curva $c_p(f)$ — la [[Dispersion Curve|curva de dispersión]] modal.

## Dispersión normal vs. inversa

En un medio **normalmente dispersivo** (rigidez creciente con la profundidad), la [[Phase Velocity|velocidad de fase]] crece con la longitud de onda (y decrece con la frecuencia):

$$\frac{dc_p}{df} < 0$$

En un medio con **inversión de velocidades** (capa blanda intercalada), la relación $c_p(f)$ puede tener pendiente positiva en ciertos rangos de frecuencia — dispersión inversa. Esto causa formas inusuales en la curva experimental y puede indicar la presencia de una capa blanda subsuperficial.

## La relación de dispersión como función de misfit en la inversión

En la [[Inversión|inversión]], se define una función de misfit que compara la [[Dispersion Curve|curva de dispersión]] **experimental** $c_p^{\text{exp}}(f_i)$ con la **teórica** $c_p^{\text{teo}}(f_i; \mathbf{m})$ calculada para un modelo de suelo $\mathbf{m} = \{V_{Sj}, V_{Pj}, \rho_j, h_j\}$:

$$\chi^2(\mathbf{m}) = \sum_i \frac{\left[c_p^{\text{exp}}(f_i) - c_p^{\text{teo}}(f_i; \mathbf{m})\right]^2}{\sigma_i^2}$$

Minimizar $\chi^2$ equivale a encontrar el modelo $\mathbf{m}$ cuya relación de dispersión teórica mejor reproduce la curva experimental. Ver [[Non-uniqueness]] para las implicaciones del carácter no-único de esta inversión.

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) y Maraschini & Foti (2010) — uso del determinante en inversión
> **Paper 002 (Xia, Miller & Park 1999)** implementa el cálculo de la relación de dispersión teórica via Thomson-Haskell como núcleo del algoritmo de inversión [[MASW Method|MASW]]. El Jacobiano ∂V_R/∂Vs se calcula analíticamente a partir de la relación de dispersión, haciendo la inversión computacionalmente eficiente (< 10 iteraciones en convergencia).
>
> **Paper 034 (Maraschini & Foti 2010)** propone usar directamente el **determinante de Haskell-Thomson** $\det[\mathbf{T}(\omega,k)]$ como función de misfit alternativa, más robusta ante superposición modal que el misfit estándar sobre $c_p(f)$. Los resultados en el sitio La Salle muestran que el determinante identifica la solución global con mayor fiabilidad en perfiles con inversión de velocidad.
>
> — Research Database, entradas 002, 034 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.2, pp. 41–43 |
| Foti et al. (2018), *Surface Wave Methods* | §2.2.2, pp. 55–59 |
| Foti et al. (2018), *Surface Wave Methods* | §2.2.3, pp. 59–62 |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 |
| Maraschini & Foti (2010), *GJI* | Paper 034 |
