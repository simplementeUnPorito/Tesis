---
name: Rayleigh Eigenproblem
description: Formulación matemática de la propagación de ondas de Rayleigh en medios estratificados como problema de valores propios; su solución produce la [[Dispersion Curve|curva de dispersión]] teórica usada en la inversión
type: reference
---

# Problema de Valores Propios de Rayleigh (Rayleigh Eigenproblem)

> [!CONCEPT] Definición
> El **Rayleigh Eigenproblem** es la formulación matemática de la propagación de [[Rayleigh Waves]] en medios verticalmente heterogéneos como un **problema de valores propios**: dada la frecuencia $\omega$, se buscan los números de onda $k_n(\omega)$ (eigenvalores) y las eigenfunciones de desplazamiento $r_n(z)$ que satisfacen simultáneamente las ecuaciones de onda en cada capa y las condiciones de frontera en todas las interfaces. Su solución produce la **[[Dispersion Relation|curva de dispersión]]** $c_n(\omega) = \omega/k_n(\omega)$ usada como dato teórico en la inversión para obtener $V_S(z)$.
>
> — Foti et al. (2018), §2.4–2.5, pp. 64–110.

## Formulación matricial (Thomson-Haskell)

Para un medio [[Layered Media|estratificado en capas]], las condiciones de continuidad de desplazamiento y esfuerzo en cada interfaz, junto con la condición de [[Elastic Wave Potentials|superficie libre]], se formulan como un sistema matricial. Para que existan soluciones de onda superficial (que decaigan con la profundidad), el determinante del sistema debe ser cero:

$$\det[\mathbf{M}(c_R, \omega)] = 0$$

Esto define las velocidades de fase de los [[Surface Wave Modes|modos]] $c_n(\omega)$ como raíces de la función secular. Las eigenfunciones $r_1^{(n)}(z)$ (horizontal) y $r_2^{(n)}(z)$ (vertical) describen el patrón de desplazamiento en profundidad de cada modo.

## Eigenvalores y eigenfunciones

| Cantidad | Símbolo | Significado físico |
|---|---|---|
| Eigenvalores | $k_n(\omega)$ o $c_n(\omega)$ | Velocidad de fase del modo $n$ |
| Eigenfunciones verticales | $r_2^{(n)}(z)$ | Desplazamiento vertical vs. profundidad |
| Eigenfunciones horizontales | $r_1^{(n)}(z)$ | Desplazamiento horizontal vs. profundidad |
| Kernels de sensibilidad | $\partial c_n/\partial V_S(z)$ | Derivadas parciales para inversión |

Los kernels de sensibilidad son las derivadas de la [[Phase Velocity|velocidad de fase]] respecto a los parámetros del modelo — son el Jacobiano del problema inverso y determinan qué profundidades puede resolver cada frecuencia.

## Extensión a medios disipativos

En [[Viscoelastic Media|medios viscoelásticos]], los módulos elásticos se reemplazan por módulos complejos dependientes de la frecuencia:

$$\tilde{\mu}(\omega) = \mu_R(\omega)(1 + 2iD_S)$$

La [[Phase Velocity|velocidad de fase]] y el número de onda se vuelven complejos. Para amortiguamiento débil ($D \ll 1$):
- La [[Phase Velocity|velocidad de fase]] cambia en orden $D^2$ (segundo orden)
- La atenuación espacial $\alpha_R$ es proporcional a $D$ (primer orden)

Esto permite estimar el perfil de amortiguamiento $D_S(z)$ a partir de la curva de atenuación $\alpha_R(f)$ medida experimentalmente.

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — Rayleigh Eigenproblem como núcleo del forward modeling
> **Paper 002 (Xia, Miller & Park 1999)** implementa el Rayleigh Eigenproblem mediante la formulación de Thomson-Haskell como núcleo del problema directo de [[MASW Method|MASW]]. El Jacobiano analítico $\partial c_R/\partial V_S$ — derivado de las eigenfunciones de Rayleigh — permite la inversión iterativa convergente en menos de 10 iteraciones para todos los sitios de Kansas ensayados. La estructura de eigenvalores del problema garantiza que la [[Dispersion Curve|curva de dispersión]] es una función suave de $V_S(z)$, lo que estabiliza la inversión y facilita la convergencia.
>
> — Research Database, entrada 002 (core).

## Relaciones con otros conceptos

- [[Elastic Wave Potentials]] — formulación de potenciales que conduce al sistema matricial
- [[Layered Media]] — el medio donde se formula el eigenproblem estratificado
- [[Surface Wave Modes]] — los eigenvalores del problema son los modos de propagación
- [[Dispersion Relation]] — la [[Dispersion Curve|curva de dispersión]] emerge de las raíces del determinante
- [[Rayleigh Waves]] — las ondas cuyo eigenproblem se formula
- [[Attenuation]] — extensión a medios disipativos con módulos complejos

## Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4–2.5, pp. 64–110 — eigenproblem y eigenfunciones |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — implementación Thomson-Haskell en [[MASW Method|MASW]] |
