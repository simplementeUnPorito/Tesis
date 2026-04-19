---
name: d'Alembert Solution
description: Solución general de la ecuación de onda 1D; superposición de dos ondas viajeras en sentidos opuestos; base pedagógica para entender propagación no dispersiva antes de [[Surface Waves|ondas superficiales]]
type: reference
---

# Solución de d'Alembert

> [!CONCEPT] Definición
> La **solución de d'Alembert** es la solución general de la [[1D Wave Equation|ecuación de onda 1D]] $\partial^2\phi/\partial x^2 = (1/c_0^2)\partial^2\phi/\partial t^2$. Expresa el campo como superposición de dos ondas viajeras en sentidos opuestos: $\phi(x,t) = f(x-c_0 t) + g(x+c_0 t)$, donde $f$ y $g$ son funciones arbitrarias determinadas por las condiciones iniciales. Es el caso no dispersivo fundamental: todas las frecuencias viajan a $c_0$ sin deformación del paquete — contraste directo con las [[Rayleigh Waves]] en [[Layered Media|medios estratificados]], que son dispersivas.
>
> — Foti et al. (2018), §2.1.1, pp. 38–39.

## Formulación matemática

La ecuación de onda 1D homogénea:

$$\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}$$

tiene como solución general:

$$\phi(x,t) = f(x - c_0 t) + g(x + c_0 t)$$

donde:
- $f(x - c_0 t)$ — onda viajando hacia la **derecha** (+x) a velocidad $c_0$
- $g(x + c_0 t)$ — onda viajando hacia la **izquierda** (-x) a velocidad $c_0$
- $f$ y $g$ — funciones arbitrarias; determinadas por condiciones iniciales $\phi(x,0)$ y $\partial_t\phi(x,0)$

El resultado clave: **cada función mantiene su forma** al propagarse — no hay deformación del paquete. Esto es la no-dispersividad.

## Interpretación física

La solución de d'Alembert es la [[Wave Superposition|superposición]] de dos ondas que no interactúan entre sí. En medios 1D sin reflexiones, la solución se reduce a una sola función viajera. En presencia de interfaces, las reflexiones introducen la función $g$: la señal registrada por un [[Geophone|geófono]] es la superposición de la onda directa ($f$) y las reflexiones ($g$).

## Limitaciones y contexto

La solución de d'Alembert aplica estrictamente a:
- Medios **homogéneos** (sin estratificación)
- Medios **no dispersivos** ($c_p = c_0$ = constante)
- Propagación **1D** (una dimensión espacial)

En medios estratificados ([[Layered Media]]), la [[Dispersion Relation|relación de dispersión]] $\omega(k)$ es no lineal y la solución de d'Alembert no aplica: diferentes frecuencias viajan a velocidades distintas y el paquete se deforma (ver [[Wave Dispersion]] y [[Fourier Integral]]). Las [[Rayleigh Waves]] son el ejemplo paradigmático.

> [!EXAMPLE] Evidencia empírica: contraste entre solución de d'Alembert y propagación dispersiva en sismogramas [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** ilustra visualmente la diferencia entre propagación hiperbólica (solución de d'Alembert) y propagación dispersiva en sismogramas de campo. Las primeras llegadas P llegan en un frente plano a velocidad constante — comportamiento de d'Alembert. El [[Ground Roll|ground-roll]] de Rayleigh, en contraste, muestra un gradiente temporal característico (frecuencias altas llegan antes que las bajas), evidenciando la dispersión geométrica. Esta diferencia visual en el sismograma es la base del análisis f-k que extrae la [[Dispersion Curve|curva de dispersión]] del campo sísmico.
>
> — Research Database, entrada 001 (core).

## Relaciones con otros conceptos

- [[1D Wave Equation]] — la EDP cuya solución general es d'Alembert
- [[Hyperbolic Waves]] — tipo de onda descrita por la ecuación de d'Alembert
- [[Wave Superposition]] — la solución es una superposición de dos ondas
- [[Wave Dispersion]] — contraste: dispersión vs. no-dispersividad de d'Alembert
- [[Fourier Integral]] — generalización a medios dispersivos
- [[Phase Velocity]] — en d'Alembert, $c_p = c_g = c_0$ (no dispersivo)

## Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–39 — categorías de propagación ondulatoria |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — contraste visual d'Alembert vs dispersión en sismogramas |
