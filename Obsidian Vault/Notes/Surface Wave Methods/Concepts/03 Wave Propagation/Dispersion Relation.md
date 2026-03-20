---
name: Dispersion Relation
description: ω(k); función que relaciona frecuencia angular con número de onda; codifica la física del medio; implícita y no analítica para Rayleigh en medios estratificados; obtenida de la condición de solución no trivial del sistema de transferencia matricial
type: reference
---

# Relación de Dispersión (Dispersion Relation)

> **Contexto:** La relación de dispersión $\omega(k)$ es la función que codifica cómo las propiedades elásticas del medio restringen los pares $(\omega, k)$ posibles para una onda propagante. En medios homogéneos es lineal (no dispersiva); en medios estratificados ([[Layered Media]]) es no lineal e implícita: se obtiene como la condición de que el determinante de la matriz de transferencia de Thomson-Haskell sea cero. Su evaluación numérica produce la [[Dispersion Curve|curva de dispersión]] teórica que se compara con la experimental en la [[Inversión|inversión]].
> **Fuente:** Foti et al. (2014), Cap. 2.1.2, pp. 41–43; Cap. 2.2.2–2.2.3, pp. 55–62.

## Intuición física

El medio elástico actúa como un filtro que solo permite la existencia de ondas cuya combinación $(\omega, k)$ satisfaga las ecuaciones de movimiento y las condiciones de contorno. Si un par $(\omega, k)$ viola la relación de dispersión, la perturbación no puede propagarse coherentemente — se disipa o no se excita. La relación de dispersión es, por tanto, la "lista de frecuencias y velocidades permitidas" para el medio.

En un semiespacio homogéneo: $\omega = V_P k$ para ondas P y $\omega = V_S k$ para ondas S — relaciones lineales, [[Elastic Half Space|no dispersivas]]. En un medio estratificado, la mezcla de propiedades con la profundidad introduce una no-linealidad: la velocidad de fase $c_p = \omega/k$ depende de $\omega$ (o equivalentemente de $k$).

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

En un medio **normalmente dispersivo** (rigidez creciente con la profundidad), la velocidad de fase crece con la longitud de onda (y decrece con la frecuencia):

$$\frac{dc_p}{df} < 0$$

En un medio con **inversión de velocidades** (capa blanda intercalada), la relación $c_p(f)$ puede tener pendiente positiva en ciertos rangos de frecuencia — dispersión inversa. Esto causa formas inusuales en la curva experimental y puede indicar la presencia de una capa blanda subsuperficial.

## La relación de dispersión como función de misfit en la inversión

En la [[Inversión|inversión]], se define una función de misfit que compara la curva de dispersión **experimental** $c_p^{\text{exp}}(f_i)$ con la **teórica** $c_p^{\text{teo}}(f_i; \mathbf{m})$ calculada para un modelo de suelo $\mathbf{m} = \{V_{Sj}, V_{Pj}, \rho_j, h_j\}$:

$$\chi^2(\mathbf{m}) = \sum_i \frac{\left[c_p^{\text{exp}}(f_i) - c_p^{\text{teo}}(f_i; \mathbf{m})\right]^2}{\sigma_i^2}$$

Minimizar $\chi^2$ equivale a encontrar el modelo $\mathbf{m}$ cuya relación de dispersión teórica mejor reproduce la curva experimental. Ver [[Non-uniqueness]] para las implicaciones del carácter no-único de esta inversión.

## Referencias

- Foti et al. (2014), Cap. 2.1.2, pp. 41–43 — relación de dispersión general, $c_p$ y $c_g$.
- Foti et al. (2014), Cap. 2.2.2, pp. 55–59 — relación de dispersión de Rayleigh en semiespacio homogéneo.
- Foti et al. (2014), Cap. 2.2.3, pp. 59–62 — Thomson-Haskell y condición de determinante para medio estratificado.
