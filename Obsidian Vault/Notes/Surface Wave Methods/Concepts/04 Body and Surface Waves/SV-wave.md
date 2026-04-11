---
name: SV-wave
description: Onda de corte vertical; polarización en el plano vertical de propagación; se acopla con ondas P en interfaces y es el componente de corte que, con P, forma las ondas de Rayleigh
type: reference
---

# Ondas SV (Shear Vertical Waves)

> [!CONCEPT] Definición
> Las **ondas SV** (Shear Vertical) son ondas de corte cuya polarización ocurre en el **plano vertical sagital** (el plano que contiene la dirección de propagación y la vertical). Junto con las [[P-waves|ondas P]], las ondas SV están matemáticamente acopladas en cualquier interfaz plana horizontal — una onda SV incidente genera conversiones P↔SV en reflexión y transmisión (ver [[Mode Conversion]]). Este acoplamiento P–SV es el mecanismo físico que da lugar a las [[Rayleigh Waves|ondas de Rayleigh]] en la superficie libre.
>
> — Foti et al. (2018), §2.1.3, pp. 43–50.

## Intuición física

Imagina una onda S que se propaga horizontalmente en la dirección $x$. El movimiento de las partículas es transversal a $x$ — puede ser vertical (dirección $z$: onda SV) u horizontal perpendicular (dirección $y$: onda [[SH-wave|SH]]). La onda SV mueve las partículas **arriba y abajo** mientras la perturbación avanza horizontalmente.

La distinción entre SV y SH no es arbitraria: tiene consecuencias dinámicas profundas. En una interfaz horizontal, la condición de continuidad de esfuerzo y desplazamiento mezcla las componentes normal ($z$) y tangencial ($x$) — estas involucran tanto P como SV. El componente $y$ (SH) satisface condiciones de frontera independientes. Por esto, el par P–SV está acoplado y el SH está desacoplado.

## Polarización y relación con el plano de propagación

Para una onda que se propaga en el plano $xz$ (plano sagital):

| Tipo | Movimiento de partículas | Plano |
|---|---|---|
| P | Paralelo a la dirección de propagación ($xz$) | Sagital |
| **SV** | Perpendicular a la propagación, en el plano sagital ($xz$) | Sagital |
| SH | Perpendicular al plano sagital (dirección $y$) | Transversal |

Las ondas SV se propagan en el plano sagital con movimiento de partículas en ese mismo plano, perpendicular a la dirección de propagación.

## Acoplamiento P–SV y formación de ondas de Rayleigh

El acoplamiento entre P y SV es la clave física de las ondas de Rayleigh. En la superficie libre ($z = 0$), las condiciones de esfuerzo libre son:

$$\sigma_{zz} = 0, \quad \sigma_{xz} = 0$$

$\sigma_{zz}$ involucra la componente P (variación de volumen) y $\sigma_{xz}$ involucra la componente SV (deformación de corte vertical). Para que ambas condiciones se satisfagan simultáneamente con una onda propagante, P y SV deben estar acopladas: la reflexión de una onda P en la superficie libre genera necesariamente una SV, y viceversa. Esta reflexión mutua, para velocidades de fase específicas, produce interferencia constructiva que se autoperpetúa a lo largo de la superficie: esto es la **onda de Rayleigh**.

En términos prácticos: una onda de Rayleigh es una superposición coherente de ondas P y SV que se refleja repetidamente en la superficie libre, con el movimiento de partículas resultante describiendo la elipse retrógrada característica en el plano sagital.

## Conversión de modos en interfaces

Cuando una onda SV incide en una interfaz entre dos medios con propiedades elásticas distintas, las condiciones de contorno (continuidad de desplazamiento y tracción) generan cuatro tipos de ondas:

| Onda incidente | Reflexiones | Transmisiones |
|---|---|---|
| SV | SV + P | SV + P |

Las amplitudes relativas de cada onda generada se calculan con las **ecuaciones de Zoeppritz** (versión P–SV). Este fenómeno es fuente de contaminación en registros [[MASW Method|MASW]]: las ondas SV convertidas de P pueden llegar al arreglo con moveouts distintos e interferir con el [[Ground Roll|ground-roll]] en frecuencias específicas.

## SV en el registro sísmico de superficie

Los geófonos verticales estándar registran la componente $z$ del movimiento. Las ondas SV incidentes desde el interior del suelo tienen componente vertical y son detectadas. Sin embargo, en el análisis f-k de [[MASW Method|MASW]], las ondas SV directas (generadas por la fuente con mayor amplitud en dirección vertical) llegan antes que el [[Ground Roll|ground-roll]] y se separan por su mayor [[Phase Velocity|velocidad de fase]].

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — acoplamiento P–SV como generador del [[Ground Roll|ground-roll]] en sismogramas de campo
> **Paper 001 (Park, Miller & Xia 1999)** documenta sismogramas de campo en Kansas donde el [[Ground Roll|ground-roll]] de Rayleigh emerge claramente del acoplamiento P–SV en la superficie libre. El tren de [[Surface Waves|ondas superficiales]] tiene amplitud mayor que las llegadas P y SV directas a distancias $> 5$ m, confirmando que la conversión de modos P↔SV en la superficie libre genera un modo de Rayleigh energéticamente dominante. La fuente vertical (maza) genera principalmente ondas P y SV, que se acoplan en la superficie libre y producen el [[Ground Roll|ground-roll]] observable.
>
> — Research Database, entrada 001 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.3, pp. 43–50 — polarización SV/SH y acoplamiento P–SV |
| Foti et al. (2018), *Surface Wave Methods* | §2.2, pp. 50–55 — formación de Rayleigh por acoplamiento P–SV |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — acoplamiento P–SV en sismogramas de campo |
