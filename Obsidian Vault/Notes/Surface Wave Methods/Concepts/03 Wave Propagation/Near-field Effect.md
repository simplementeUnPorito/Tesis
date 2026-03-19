---
name: Near-field Effect
description: Región cercana a la fuente donde las Rayleigh waves no se comportan como ondas planas y la velocidad aparente es distorsionada por contribuciones de ondas de cuerpo.
type: concept
---

# Near-field Effect

## Definición

Las [[Rayleigh Waves]] solo pueden tratarse como **ondas planas** a distancias suficientemente grandes de la fuente, denominadas **campo lejano** (*far-field*). La zona más cercana a la fuente, donde esta aproximación no es válida, se denomina **campo cercano** (*near-field*).

## Intuición física

Una fuente puntual en superficie genera simultáneamente ondas de cuerpo ([[P-waves]], [[S-Waves]]) y ondas superficiales. En el campo cercano, la amplitud de las ondas de cuerpo es comparable o mayor que la de las ondas superficiales. A medida que aumenta la distancia:
- Las ondas de cuerpo decaen como $r^{-2}$ (en superficie).
- Las [[Rayleigh Waves]] decaen como $r^{-0.5}$.

Por eso, más allá de cierta distancia, el campo queda dominado por las ondas superficiales y la aproximación de onda plana es válida.

## Consecuencia para la medición

Dentro del campo cercano, la velocidad de fase aparente medida **no corresponde a la velocidad de Rayleigh** del modo fundamental. La velocidad aparente puede estar sesgada hacia arriba o abajo según la frecuencia y la estratigrafía.

## Criterio cuantitativo

El umbral entre campo cercano y campo lejano depende de la longitud de onda de Rayleigh $\lambda_R$:

| Condición del sitio | Offset mínimo recomendado |
|---|---|
| Medio normalmente dispersivo | $r \gtrsim \lambda_R / 2$ (Stokoe et al. 1994) |
| Medio inversamente dispersivo | $r \gtrsim \lambda_R$ a $2\lambda_R$ |

Dado que $\lambda_R$ depende de la frecuencia (y la velocidad del subsuelo, que es desconocida), el criterio es frecuencia-dependiente: para frecuencias bajas (longitudes de onda largas), el campo cercano se extiende más lejos.

## Implicaciones para el diseño experimental

- El primer geófono debe ubicarse al menos a $\lambda_R/2$ de la fuente, idealmente a $\lambda_R$.
- Para frecuencias bajas esto impone offsets de fuente largos, que a su vez reducen el SNR.
- Algunas técnicas de procesamiento permiten identificar y enmudecer (*mute*) los receptores afectados por campo cercano a cada frecuencia (ver Sec. 4.4 de Foti).

## Relación con el problema de Lamb

El campo cercano / lejano fue estudiado en el contexto del [[Lamb's Problem]]. La solución exacta incluye tanto ondas superficiales como ondas de cuerpo; la aproximación de campo lejano retiene solo las ondas superficiales.

## Fuentes

- PDF: Sebastiano Foti Chapter 2, Sec. 2.4.2, p. 83–86
- PDF: Sebastiano Foti Chapter 3, Sec. 3.4.1.6, p. 160–162
