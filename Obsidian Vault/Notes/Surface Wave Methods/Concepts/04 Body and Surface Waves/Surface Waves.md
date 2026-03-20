---
name: Surface Waves
description: Ondas elásticas confinadas cerca de una interfaz; decaimiento exponencial con profundidad; dispersión en medios estratificados; base de MASW para perfiles VS
type: reference
---

# Ondas Superficiales (Surface Waves)

> **Contexto:** Las ondas superficiales son perturbaciones elásticas cuya energía queda **confinada cerca de una interfaz** — típicamente la superficie libre del suelo. A diferencia de las [[Body Waves|ondas de cuerpo]] que se propagan por el interior del medio y decaen como $1/r$, las ondas superficiales decaen exponencialmente con la profundidad y geométricamente como $1/\sqrt{r}$ en la superficie — lo que las hace dominantes en registros sísmicos a distancia. En medios estratificados son **dispersivas**: su velocidad depende de la frecuencia, y este fenómeno es la base de los métodos de caracterización del subsuelo (MASW, SASW, ReMi, SPAC).
> **Fuente:** Foti et al. (2014), Cap. 2.2, pp. 50–68.

## Intuición física: confinamiento en la interfaz

La superficie libre impone una condición de esfuerzo nulo ($\sigma_{zz} = \sigma_{xz} = 0$ en $z = 0$). Esta condición fuerza a que las ondas P y SV reflejadas en la superficie interfieran constructivamente para velocidades de fase específicas, generando un modo de propagación que se autopropaga a lo largo de la interfaz sin necesidad de reflexiones adicionales. La energía queda atrapada en una capa superficial de espesor comparable a la longitud de onda.

Consecuencias observables:
- A mayor profundidad, las partículas casi no se mueven.
- En el sismograma superficial, las ondas superficiales llegan después de P y S pero con **mayor amplitud** (menor decaimiento geométrico).
- En medios estratificados, diferentes frecuencias "ven" diferentes profundidades del suelo: las ondas largas (baja frecuencia) penetran más y viajan más rápido en suelos normalmente dispersivos (más rígidos en profundidad).

## Tipos de ondas superficiales

### Ondas de Rayleigh

Las [[Rayleigh Waves]] surgen del acoplamiento entre ondas P y SV (ver [[Mode Conversion]]) en la superficie libre de un [[Elastic Half Space|semiespacio elástico]]. Existen en todo semiespacio elástico homogéneo, incluso sin estratificación. Las partículas describen una elipse retrógrada en el plano vertical de propagación. En un semiespacio homogéneo son no dispersivas; en medios estratificados ([[Layered Media]]) son dispersivas.

### Ondas de Love

Las [[Love Waves]] son ondas [[SH-wave|SH]] guiadas en una capa superficial más blanda que el semiespacio subyacente. Requieren estratificación: no existen en un semiespacio homogéneo. Las partículas se mueven horizontalmente en la dirección transversal a la propagación. Sus curvas de dispersión dependen únicamente de $V_S$ y las densidades — no de $V_P$.

### Ondas de Scholte

Las [[Scholte Waves]] son el análogo de las ondas de Rayleigh en la interfaz sólido–fluido (fondo marino). Tienen velocidad menor que las ondas de Rayleigh en el sólido y son especialmente relevantes en aplicaciones offshore.

## Decaimiento con profundidad

La amplitud de las ondas superficiales decrece exponencialmente con la profundidad. Para [[Rayleigh Waves]] en un semiespacio homogéneo, la componente vertical de desplazamiento decae aproximadamente como:

$$u_z(z) \propto e^{-\beta z}, \quad \beta \propto k = \frac{2\pi}{\lambda}$$

La mayor parte de la energía de deformación (~95%) está concentrada dentro de $z \lesssim \lambda_R$ (ver [[Skin Depth]]). La regla práctica para la **profundidad de investigación** en MASW es:

$$z_{\max} \approx \frac{\lambda_{\max}}{2} \quad \text{a} \quad \lambda_{\max}$$

## Dispersión en medios estratificados

En un semiespacio homogéneo, la velocidad de fase de Rayleigh es $c_R \approx 0.92\,V_S$ — constante, no dependiente de la frecuencia ([[Elastic Half Space|no dispersiva]]). En un medio estratificado ([[Layered Media]]), la velocidad de fase depende de la frecuencia: ondas de baja frecuencia (longitud de onda larga) penetran más profundo y son sensibles a las capas más rígidas en profundidad; ondas de alta frecuencia son sensibles solo a la capa superficial.

Esta variación de velocidad con la frecuencia — la **[[Dispersion Curve|curva de dispersión]]** $c(f)$ — es el observable que se invierte en MASW para obtener el perfil $V_S(z)$.

## Partición de energía y dominio en registros sísmicos

La solución del [[Lamb's Problem|Problema de Lamb]] (1904) muestra que para una fuente puntual vertical en la superficie de un semiespacio, las ondas de Rayleigh reciben ~67% de la energía total, mientras que las ondas de cuerpo solo reciben ~33% (repartido entre P y S). Combinado con el menor decaimiento geométrico ($1/\sqrt{r}$ vs $1/r$), esto explica por qué el **ground-roll** (tren de ondas superficiales) domina el sismograma en métodos sísmicos superficiales.

## Múltiples modos de propagación

En medios estratificados, las ondas superficiales se propagan en **múltiples modos** (ver [[Surface Wave Modes]]): modo fundamental y modos superiores. Cada modo tiene su propia curva de dispersión. En la mayoría de los registros MASW el modo fundamental es dominante, pero en presencia de inversiones de velocidad los modos superiores pueden ser energéticamente comparables o incluso dominantes.

## Referencias

- Foti et al. (2014), Cap. 2.2, pp. 50–68 — derivación de Rayleigh y Love en semiespacio y medio estratificado.
- Foti et al. (2014), Cap. 2.2.1, pp. 52–55 — decaimiento en profundidad y skin depth.
