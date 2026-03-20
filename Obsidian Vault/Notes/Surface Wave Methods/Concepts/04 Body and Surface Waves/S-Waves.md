---
name: S-Waves
description: Ondas de cuerpo de corte (transversales); velocidad VS = √(μ/ρ) refleja la rigidez del esqueleto sólido; parámetro objetivo en la caracterización geotécnica mediante métodos de ondas superficiales
type: reference
---

# Ondas S (S-Waves / Shear Waves)

> **Contexto:** Las ondas S (Secondary / Shear / Transversal) son ondas de cuerpo en las que el movimiento de la partícula es **perpendicular** a la dirección de propagación, produciendo deformación de corte puro sin cambio de volumen. Su velocidad $V_S = \sqrt{\mu/\rho}$ depende únicamente de la rigidez de corte $\mu$ del esqueleto sólido y de la densidad $\rho$ — haciéndola el **parámetro objetivo fundamental** de todos los métodos de caracterización geotécnica basados en ondas, incluyendo MASW.
> **Fuente:** Foti et al. (2014), Cap. 2.1.3, pp. 43–50.

## Intuición física

Las ondas S deforman el medio por cizallamiento: capas adyacentes del material se deslizan entre sí en la dirección transversal a la propagación. Esto contrasta con las [[P-waves|ondas P]], que comprimen y dilatan el medio en la dirección de propagación. La deformación de corte es puramente deviatórica (no cambia el volumen); esto significa que las ondas S no interactúan con la compresibilidad del fluido intersticial.

**Consecuencia crítica en suelos saturados**: en un suelo saturado, el agua poral domina la rigidez volumétrica pero no contribuye en absoluto a la rigidez de corte $\mu$ (los fluidos no resisten esfuerzos de corte). Por tanto, $V_S$ refleja exclusivamente la rigidez del esqueleto mineral del suelo, con independencia del grado de saturación o del nivel freático. Esto hace a $V_S$ un indicador geotécnico mucho más limpio que $V_P$.

## Formulación matemática

La velocidad de propagación de las ondas S en un medio elástico isótropo:

$$V_S = \sqrt{\frac{\mu}{\rho}} = \sqrt{\frac{G}{\rho}}$$

donde $\mu = G$ es el módulo de corte (rigidez de corte) y $\rho$ es la densidad. En términos de las [[Strain Tensor|constantes de Lamé]] $\lambda, \mu$:

$$\frac{V_P}{V_S} = \sqrt{\frac{\lambda + 2\mu}{\mu}} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

Esta relación vincula $V_S$ con $V_P$ a través del [[Poisson Ratio|coeficiente de Poisson]] $\nu$. Para $\nu = 0.25$: $V_P/V_S = \sqrt{3} \approx 1.73$.

## Polarización y tipos de ondas S

Las ondas S tienen **polarización transversal**: el vector de desplazamiento es perpendicular al vector de propagación. Pero "perpendicular" define un plano, y según la orientación de la polarización dentro de ese plano, las ondas S se clasifican en:

| Tipo | Polarización | Acoplamiento con P |
|---|---|---|
| **SV** (Shear Vertical) | En el plano vertical de propagación | Sí — ver [[Mode Conversion]] |
| **[[SH-wave\|SH]]** (Shear Horizontal) | Horizontal, ⊥ al plano de propagación | No — matemáticamente desacoplada |

Esta distinción es fundamental: las ondas SV participan en la formación de [[Rayleigh Waves]] por acoplamiento con P, mientras que las ondas SH son la base de las [[Love Waves]].

## Relación con propiedades geotécnicas

La importancia de $V_S$ en geotecnia deriva de su relación directa con el **módulo de corte a pequeñas deformaciones** $G_{\max}$:

$$G_{\max} = \rho\, V_S^2$$

$G_{\max}$ es la propiedad mecánica del suelo para deformaciones de corte en el rango elástico (deformaciones $< 10^{-5}$). Es la base para:
- **Amplificación sísmica del sitio**: $V_S$ controla la velocidad y amortiguación de la respuesta sísmica del suelo.
- **Código sísmico (VS,30)**: el promedio ponderado de $V_S$ en los primeros 30 m clasifica el tipo de suelo (clases A–E en Eurocódigo 8 y normativas equivalentes). Ver [[Vs30]].
- **Rigidez de cimentaciones**: $G_{\max}$ es la entrada para análisis de interacción suelo–estructura.
- **Licuefacción**: $V_S$ correlaciona con la resistencia a la licuefacción en suelos granulares saturados.

## Por qué VS y no VP

En suelos saturados bajo carga no drenada, $V_P$ salta a ~1500 m/s (velocidad del sonido en agua), independientemente de la rigidez del esqueleto. Esto hace que $V_P$ no sea representativo de las propiedades mecánicas del suelo. $V_S$, en cambio, es insensible a la presencia del agua poral y refleja fielmente la rigidez del esqueleto. Por esta razón, todos los métodos de ondas superficiales (MASW, SASW, ReMi, SPAC) apuntan a medir el **perfil de $V_S$ con la profundidad**.

## Valores típicos en suelos

| Material | $V_S$ (m/s) |
|---|---|
| Arcilla blanda | 50–150 |
| Arcilla media/dura | 150–350 |
| Arena suelta | 100–250 |
| Arena densa | 250–500 |
| Grava | 300–700 |
| Roca blanda (marga) | 600–1200 |
| Roca dura | 1200–3500 |

## Referencias

- Foti et al. (2014), Cap. 2.1.3, pp. 43–50 — derivación de VS desde ecuaciones de Navier; polarización SV/SH.
- Foti et al. (2014), Cap. 1.1, pp. 1–10 — importancia de VS en caracterización geotécnica.
