---
name: SH-wave
description: Onda de corte horizontal; polarización transversal en plano horizontal; no se acopla con ondas P; base física de las ondas de Love en medios estratificados
type: reference
---

# Ondas SH (Shear Horizontal Waves)

> **Contexto:** Las ondas SH son un tipo de [[S-Waves|onda de corte]] cuya polarización ocurre enteramente en el plano horizontal, perpendicular tanto a la dirección de propagación como al plano vertical. Su propiedad más importante es que **están matemáticamente desacopladas de las ondas P y SV**: en una interfaz, una onda SH solo genera ondas SH reflejadas y transmitidas. Este desacoplamiento es la base física de las [[Love Waves]], que son ondas SH guiadas en una capa superficial.
> **Fuente:** Foti et al. (2014), Cap. 2.1.3, pp. 43–50; Cap. 2.3, pp. 60–64.

## Intuición física

Considera una onda que viaja horizontalmente en la dirección $x$. El movimiento de las partículas puede ser:
- **Paralelo a $x$**: onda P (compresión/dilatación).
- **En el plano vertical $xz$**: onda SV (corte vertical) — se acopla con P.
- **Perpendicular al plano $xz$, en dirección $y$**: onda SH (corte horizontal) — **no** se acopla con P.

La razón del desacoplamiento es geométrica: las condiciones de contorno en una interfaz plana horizontal mezclan los esfuerzos normales (relacionados con P y SV) pero el esfuerzo de corte en dirección $y$ es independiente. Un frente de onda SH que incide en una interfaz solo necesita satisfacer la continuidad del desplazamiento en $y$ y el esfuerzo de corte $\sigma_{yz}$ — ambas condiciones solo involucran componentes SH, sin acoplar con P ni SV.

## Formulación matemática

En un medio isótropo homogéneo, el campo de desplazamiento de una onda SH plana que viaja en la dirección $x$ es:

$$u_y(x,t) = A\,e^{i(k x - \omega t)}, \quad u_x = u_z = 0$$

La ecuación de onda que gobierna $u_y$ es independiente de $u_x$ y $u_z$:

$$\frac{\partial^2 u_y}{\partial t^2} = V_S^2 \nabla^2 u_y, \quad V_S = \sqrt{\frac{\mu}{\rho}}$$

Esta es la separación del problema SH del sistema P–SV. Las ondas P y SV satisfacen un sistema acoplado de ecuaciones, mientras que SH satisface una ecuación escalar independiente.

## Condiciones de frontera en interfaz

Para una interfaz horizontal entre dos medios (densidades $\rho_1, \rho_2$; módulos $\mu_1, \mu_2$):

| Condición de continuidad | Involucra |
|---|---|
| $u_y^{(1)} = u_y^{(2)}$ | Solo SH |
| $\mu_1 \partial u_y^{(1)}/\partial z = \mu_2 \partial u_y^{(2)}/\partial z$ | Solo SH |

No aparecen $u_x$ ni $u_z$: el problema SH está completamente desacoplado. Compare con las condiciones P–SV, que involucran simultáneamente los desplazamientos vertical y horizontal (ver [[Mode Conversion]]).

## Reflexión total y guía de ondas SH: Love Waves

La condición de reflexión total de ondas SH en la interfaz capa–semiespacio requiere que el ángulo de incidencia supere el ángulo crítico. En términos de velocidades:

$$\sin\theta_c = \frac{V_{S1}}{V_{S2}}$$

donde $V_{S1}$ es la velocidad en la capa superficial y $V_{S2} > V_{S1}$ es la velocidad en el semiespacio. Cuando se cumple la reflexión total, la energía SH queda atrapada en la capa: esto es una **onda de Love**.

Las [[Love Waves]] son, en esencia, la superposición constructiva de ondas SH que rebotan entre la superficie libre (donde la condición de esfuerzo libre actúa como reflector perfecto para SH) y la interfaz capa–semiespacio (donde hay reflexión total). La condición de interferencia constructiva en la capa de espesor $h$ conduce a la [[Dispersion Relation|relación de dispersión]] de Love:

$$\tan\left(k\sqrt{(V_{S2}/V_{S1})^2 - 1}\,k h\right) = \frac{\mu_2 \sqrt{1 - (V_{S1}/V_{S2})^2 c^{-2}}}{\mu_1 \sqrt{(c/V_{S1})^{-2} - 1}}$$

donde $c$ es la velocidad de fase de Love. Esta ecuación tiene múltiples soluciones para cada frecuencia: son los [[Surface Wave Modes|modos de Love]].

## Excitación en campo

Las ondas SH se excitan con fuentes de tipo horizontal (golpe lateral, vibrador horizontal). Las fuentes verticales estándar (martillo, peso) generan principalmente ondas P y SV, con mínima energía SH. Esto tiene implicaciones para la adquisición:

- **Adquisición de Love waves**: requiere fuentes y geófonos horizontales orientados perpendicularmente a la línea del arreglo.
- **Geófonos verticales** (los más comunes en MASW) no registran SH: son insensibles al movimiento horizontal transversal.
- **Ventaja de Love vs. Rayleigh**: al no involucrar ondas P, la inversión de Love es más limpia y su curva de dispersión solo depende del perfil $V_S$ y las densidades — no requiere $V_P$ como parámetro a priori.

## SH en medios estratificados: método de la matriz de transferencia

El análisis de propagación SH en medios estratificados es más simple que el P–SV porque las condiciones de contorno son escalares. La solución en cada capa es:

$$u_y^{(j)}(z) = A_j e^{i k_{z,j} z} + B_j e^{-i k_{z,j} z}, \quad k_{z,j} = \sqrt{(\omega/V_{Sj})^2 - k^2}$$

Las amplitudes $A_j, B_j$ se conectan entre capas mediante una matriz de transferencia $2\times 2$ (vs. $4\times 4$ para el caso P–SV del método de [[Layered Media|Thomson-Haskell]]). Esto hace que el cálculo de curvas de dispersión de Love sea computacionalmente más eficiente.

## Referencias

- Foti et al. (2014), Cap. 2.1.3, pp. 43–50 — polarización y separación P/SV/SH.
- Foti et al. (2014), Cap. 2.3, pp. 60–64 — derivación de la relación de dispersión de Love desde reflexión total SH.
