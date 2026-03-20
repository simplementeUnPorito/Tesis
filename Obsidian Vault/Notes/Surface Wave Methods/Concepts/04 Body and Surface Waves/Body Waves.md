---
name: Body Waves
description: Ondas sísmicas que viajan a través del volumen del medio; comprenden ondas P (compresionales) y S (de corte); decaen 1/r en amplitud, más rápido que las ondas superficiales (1/√r)
type: reference
---

# Ondas de Cuerpo (Body Waves)

> **Contexto:** Las ondas de cuerpo son perturbaciones elásticas que se propagan a través del interior de un medio sólido, a diferencia de las [[Rayleigh Waves|ondas superficiales]] que se confinan cerca de una interfaz. Existen dos tipos: ondas P (compresionales) y ondas S (de corte). Su decaimiento geométrico más rápido (1/r en amplitud) respecto a las superficiales (1/√r) explica por qué los registros sísmicos a distancia están dominados por el ground-roll de ondas Rayleigh.
> **Fuente:** Foti et al. (2014), Cap. 2.1.3, pp. 43–50.

## Intuición física

Cuando una fuente sísmica perturba un punto del medio, la perturbación se propaga en todas las direcciones como un frente esférico: esto son las ondas de cuerpo. Su energía se distribuye sobre la superficie de una esfera de radio creciente, de modo que la intensidad (energía/área) cae como $1/r^2$ y la amplitud como $1/r$.

En contraste, las [[Rayleigh Waves]] están confinadas a la superficie y su energía se distribuye sobre el perímetro de un círculo ($2\pi r$), por lo que la amplitud decae solo como $1/\sqrt{r}$. Esta diferencia de decaimiento es la razón física por la que, a distancias mayores que unas pocas longitudes de onda, el ground-roll de ondas Rayleigh domina el registro sísmico de superficie.

## Los dos tipos de ondas de cuerpo

### Ondas P (Compresionales / Primarias)

Las [[P-waves|ondas P]] producen deformación volumétrica alternante (compresión–dilatación) en la dirección de propagación. El movimiento de partículas es **paralelo** al vector de propagación $\hat{k}$ — polarización longitudinal. Pueden propagarse en sólidos y fluidos.

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}} = \sqrt{\frac{M}{\rho}}$$

Son las ondas más rápidas: en roca, $V_P \sim 2000$–$6000$ m/s.

### Ondas S (De Corte / Secundarias)

Las [[S-Waves|ondas S]] producen deformación de corte puro. El movimiento de partículas es **perpendicular** al vector de propagación — polarización transversal. Solo pueden propagarse en sólidos (los fluidos no tienen rigidez de corte $\mu$).

$$V_S = \sqrt{\frac{\mu}{\rho}}$$

Las ondas S se subdividen en:
- **[[SH-wave|SV]]** (Shear Vertical): polarización en el plano vertical de propagación; se acopla con ondas P en interfaces.
- **[[SH-wave|SH]]** (Shear Horizontal): polarización horizontal perpendicular al plano de propagación; **no se acopla** con ondas P — matemáticamente independiente.

### Relación de velocidades

$$\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

Para $\nu = 0.25$ (material Poisson estándar): $V_P/V_S = \sqrt{3} \approx 1.73$. En suelos blandos saturados, $\nu \to 0.5$ y la razón puede superar 10, pues $V_P$ es controlado por la compresibilidad del agua poral mientras que $V_S$ refleja la rigidez del esqueleto.

## Decaimiento geométrico y partición de energía

| Tipo de onda | Decaimiento de amplitud | Causa física |
|---|---|---|
| Onda de cuerpo (volumen 3D) | $\propto 1/r$ | Frente esférico: área $\propto r^2$ |
| Onda superficial (superficie 2D) | $\propto 1/\sqrt{r}$ | Frente cilíndrico: perímetro $\propto r$ |

La solución del **[[Lamb's Problem|Problema de Lamb]]** (Lamb, 1904) cuantificó esta partición: en la superficie de un semiespacio, el ~67% de la energía de una fuente puntual vertical queda en las ondas Rayleigh, y el resto en ondas de cuerpo P y S. Esto valida el uso de ondas superficiales como el observable dominante en MASW.

## Ondas de cuerpo en MASW

Las ondas de cuerpo son **ruido** en los métodos de ondas superficiales. Aparecen como:

1. **Primeras llegadas P**: arrivan antes que el ground-roll; se eliminan con una ventana temporal o agente de mute.
2. **Ondas P refractadas**: en arreglos cortos, llegadas refractadas pueden solaparse con el inicio del ground-roll y contaminar las frecuencias altas.
3. **Reflexiones y conversiones**: en medios heterogéneos, las interfaces generan ondas convertidas P↔SV (ver [[Mode Conversion]]) que aparecen en el espectro f-k a velocidades más altas que las superficiales.

En el análisis f-k, las ondas de cuerpo tienen velocidades de fase mucho mayores que las ondas de Rayleigh y se separan fácilmente; sin embargo, si el arreglo es demasiado corto o el near-field no está excluido, pueden contaminar la curva de dispersión a frecuencias altas.

## Uso en métodos complementarios

En **refracción sísmica**, las primeras llegadas de ondas P son el observable primario: se mapea la distribución de $V_P$ con la profundidad, incluyendo la detección de la tabla de agua (donde $V_P$ salta a ~1500 m/s). Esto proporciona el parámetro $V_P$ (o el [[Poisson Ratio|coeficiente de Poisson]]) necesario como información a priori en la inversión de la curva de dispersión de Rayleigh.

## Referencias

- Foti et al. (2014), Cap. 2.1.3, pp. 43–50 — derivación de VP y VS desde ecuaciones de Navier.
- Foti et al. (2014), Cap. 2.2.1, pp. 52–55 — decaimiento geométrico y Problema de Lamb.
