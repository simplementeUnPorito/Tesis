---
name: Variational Principles
description: Principios de extremo (Hamilton, Rayleigh-Ritz) que expresan la propagación de ondas como la minimización de un funcional — base teórica del cálculo de sensibilidades en métodos de [[Surface Waves|ondas superficiales]]
type: reference
---

# Variational Principles — Principios Variacionales

> [!CONCEPT] Definición
> Los **Principios Variacionales** son formulaciones de la mecánica y la física que expresan las leyes de movimiento como la condición de extremo (mínimo, máximo o punto de silla) de un **funcional** — una función de funciones. En la propagación de ondas elásticas y la teoría de [[Surface Waves|ondas superficiales]], el principio variacional más relevante es el **principio de Hamilton**: el movimiento real de un sistema es aquel que hace estacionario el funcional de acción $\mathcal{A} = \int_{t_1}^{t_2} (T - V) \, dt$ (diferencia entre energía cinética $T$ y potencial $V$). Para las ondas de Rayleigh en un [[Layered Media|medio estratificado]], el principio variacional se usa para derivar la **sensibilidad de la [[Phase Velocity|velocidad de fase]]** $c_R$ respecto a los parámetros del modelo $V_S(z)$: la variación de $c_R$ al perturbar ligeramente el perfil de velocidad se expresa como un **funcional lineal** de la perturbación, cuyo núcleo es el [[Sensitivity Kernel|kernel de sensibilidad]] $K(z)$. Esto permite calcular el Jacobiano $\partial c_R / \partial V_S(z)$ analíticamente sin diferencias finitas — base del cálculo eficiente de sensibilidades en [[Inversión|inversión]] de [[Dispersion Curve|curvas de dispersión]].
>
> — Foti et al. (2018), §5.2; Aki & Richards (2002), §7.3; Anderson & Dziewonski (1982).

## Principio de Rayleigh-Ritz para [[Surface Waves|ondas superficiales]]

### Velocidad de fase como cociente de Rayleigh

Para las ondas de Rayleigh en un semi-espacio estratificado, la [[Phase Velocity|velocidad de fase]] $c_R$ puede expresarse como el cociente de Rayleigh:

$$c_R^2 = \frac{\mathcal{V}[\mathbf{u}]}{\mathcal{K}[\mathbf{u}]} = \frac{\text{energía potencial del modo}}{\text{energía cinética del modo}}$$

donde $\mathbf{u}$ es el campo de desplazamiento del modo fundamental de Rayleigh. La condición de extremo de este cociente (variación igual a cero) reproduce las ecuaciones de movimiento de las ondas de Rayleigh.

### Derivada variacional (fórmula de sensibilidad)

La variación de $c_R^2$ respecto a una perturbación $\delta V_S(z)$ del perfil de velocidad:

$$\delta c_R^2 = \int_0^\infty K_{V_S}(z) \, \delta V_S(z) \, dz$$

donde el **kernel de sensibilidad** es:

$$K_{V_S}(z) = \frac{2}{I_2} \rho(z) V_S(z) \left[(\partial_z U_r)^2 + k^2 U_z^2 - k^2 U_z \partial_z U_r\right]_{z}$$

con $I_2 = \int_0^\infty \rho(z)(U_r^2 + U_z^2) dz$ el factor de normalización energética, $U_r$ y $U_z$ las autofunciones de desplazamiento horizontal y vertical, y $k = \omega/c_R$ el [[Wavenumber|número de onda]].

## Importancia en la inversión de [[MASW Method|MASW]]

Los principios variacionales permiten:
1. **Cálculo analítico del Jacobiano**: sin diferencias finitas → cálculo exacto y eficiente de $\partial c_R(f_i)/\partial V_S(z_j)$ para todas las capas $j$ simultáneamente
2. **Interpretación física de la sensibilidad**: el kernel $K_{V_S}(z)$ muestra qué profundidades contribuyen más a la velocidad de Rayleigh a cada frecuencia (pico a z ≈ λ/3)
3. **Fórmulas aproximadas**: expresiones simplificadas para el límite de largo período ($c_R \approx 0.92 V_S$ en semiespacio homogéneo) que son útiles para estimaciones rápidas

> [!EXAMPLE] Evidencia empírica: Aki & Richards (2002) — principio variacional para sensibilidad de [[Love Waves|ondas Love]] y Rayleigh
> Aki & Richards (2002, §7.3) derivan el kernel de sensibilidad de las ondas de Love y Rayleigh para un modelo de Tierra con capas usando el principio variacional de Rayleigh-Ritz. El resultado es que $\partial c_R/\partial V_S(z)$ tiene un pico a la profundidad $z \approx \lambda/3$ para el modo fundamental de Rayleigh (donde $\lambda = c_R/f$ es la [[Wavelength|longitud de onda]]), decayendo exponencialmente a mayor profundidad. Esta relación — conocida como la **regla del tercio de [[Wavelength|longitud de onda]]** — establece que la frecuencia $f$ del modo fundamental de Rayleigh "siente" principalmente el $V_S$ a la profundidad $z \approx c_R(f)/(3f)$. Es la base teórica del método [[MASW Method|MASW]]: para investigar hasta la profundidad $H$, se necesitan frecuencias $f \leq c_{R,min}/(3H)$ donde $c_{R,min}$ es la velocidad mínima en el perfil.
>
> — Aki & Richards (2002), §7.3, pp. 249–270; Foti et al. (2018), §5.2, pp. 215–225.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §5.2, pp. 215–225 — sensibilidades variacionales |
| Aki & Richards (2002), *Quantitative Seismology* | §7.3 — principio variacional para [[Surface Waves|ondas superficiales]] |
| Anderson & Dziewonski (1982), *Sci. Am.* | Principio variacional en sismología de la Tierra |
