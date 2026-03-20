---
name: P-waves
description: Ondas de cuerpo de compresión (longitudinales); las más rápidas en sólidos; su velocidad en suelos saturados es dominada por la compresibilidad del agua, limitando su utilidad geotécnica
type: reference
---

# Ondas P (P-waves / Compressional Waves)

> **Contexto:** Las ondas P (Primary / Pressure / Compressional) son ondas de cuerpo donde el movimiento de la partícula es paralelo a la dirección de propagación. Son las ondas más rápidas en medios sólidos y viajan también en fluidos. En el contexto de ondas superficiales, su velocidad $V_P$ es un parámetro a priori necesario (aunque de sensibilidad limitada) en la inversión de la curva de dispersión de Rayleigh.
> **Fuente:** Foti et al. (2014), Cap. 2.1.3, pp. 43–50.

## Intuición física

Las ondas P producen una secuencia alterna de compresión y dilatación del medio en la dirección de propagación. Es análogo al sonido en el aire: la perturbación se transmite como una variación de presión que viaja hacia adelante, comprimiendo y expandiendo el volumen local del material.

En sólidos, la energía se transmite tanto por la rigidez de corte $\mu$ como por la rigidez volumétrica $K = \lambda + 2\mu/3$. En fluidos, donde $\mu = 0$, solo existe la componente compresional: las ondas P viajan en agua y aire, mientras que las ondas S no lo hacen.

## Formulación matemática

La velocidad de propagación de las ondas P en un medio elástico isótropo es:

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}} = \sqrt{\frac{M}{\rho}}$$

donde:
- $\lambda$, $\mu$ — constantes de Lamé
- $M = \lambda + 2\mu$ — módulo confinado (P-wave modulus)
- $\rho$ — densidad

En términos del [[Poisson Ratio|coeficiente de Poisson]] $\nu$:

$$\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

Para $\nu = 0.25$: $V_P/V_S = \sqrt{3} \approx 1.73$.

## Polarización y movimiento de partícula

Las ondas P tienen **polarización longitudinal**: el vector de desplazamiento de las partículas es paralelo al vector de propagación $\hat{k}$. No existe componente transversal. Esto contrasta con las [[S-Waves|ondas S]] (polarización transversal).

Consecuencia: las ondas P no producen deformación de corte pura. Son sensibles al módulo volumétrico del material.

## Comportamiento en geomateriales saturados

En suelos saturados bajo carga no drenada, la compresibilidad del material está dominada por la compresibilidad del agua poral ($K_{agua} \approx 2.2\,\text{GPa}$). Esto hace que $V_P$ aumente fuertemente y tienda a la velocidad del sonido en agua (~1500 m/s), independientemente de la rigidez del esqueleto sólido.

**Consecuencia crítica**: en suelos saturados, $V_P$ no es un buen indicador de la rigidez geotécnica del suelo. La [[S-Waves|velocidad de onda S]] ($V_S$) sí refleja la rigidez del esqueleto y tiene mejor correlación con propiedades geotécnicas. Esto es la razón fundamental por la que los métodos de caracterización geotécnica se centran en $V_S$.

## Valores típicos

| Material | $V_P$ (m/s) | $V_S$ (m/s) |
|---|---|---|
| Arcilla blanda saturada | 1400–1600 | 50–200 |
| Arena suelta seca | 200–500 | 100–300 |
| Arena densa saturada | 1500–2000 | 200–400 |
| Roca sedimentaria | 2000–4000 | 1000–2000 |
| Roca cristalina | 4000–7000 | 2000–4000 |

## Relevancia en métodos de ondas superficiales

En la inversión de la curva de dispersión de [[Rayleigh Waves]], $V_P$ (o equivalentemente $\nu$) es un **parámetro a priori** — se fija basándose en información independiente (refracción P, nivel freático, ensayos SPT) y no se invierte directamente. La sensibilidad de la curva de dispersión a $V_P$ es baja comparada con $V_S$, pero no despreciable: un $V_P$ incorrecto (especialmente ignorar el nivel freático) puede introducir errores sistemáticos en el perfil $V_S$ invertido.

En el método de **refracción sísmica**, las ondas P son el observable primario: los tiempos de llegada de los primeros arrivals se usan para inferir el contraste de $V_P$ entre capas, incluyendo la detección de la tabla de agua.

## Referencias

- Foti et al. (2014), Cap. 2.1.3, pp. 43–50 — derivación desde ecuaciones de Navier.
- Foti et al. (2014), Cap. 7.1.3, pp. 361–363 — impacto del nivel freático (VP) en la inversión.
