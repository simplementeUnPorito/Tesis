---
name: Group Velocity
description: Velocidad de propagación de la envolvente de un paquete de ondas; controla la llegada de energía en registros dispersivos y es observable en sismología de ondas superficiales de largo período
type: reference
---

# Velocidad de Grupo (Group Velocity)

> **Contexto:** La velocidad de grupo $c_g = d\omega/dk$ describe la velocidad a la que se propaga la envolvente (paquete de energía) de una onda dispersiva. En sismología, es directamente observable como la velocidad de llegada del tren de ondas; en métodos MASW, es menos utilizada que la [[Phase Velocity|velocidad de fase]] pero fundamental para entender el comportamiento temporal de los registros.
> **Fuente:** Foti et al. (2014), Cap. 2.1.2, pp. 41–43; Cap. 4.1, pp. 206–208.

## Intuición física

Cuando un paquete de ondas con contenido espectral finito se propaga en un medio dispersivo, sus componentes de frecuencia viajan a velocidades de fase diferentes y el paquete se deforma: el tren de ondas se "estira" o "dispersa" en el tiempo. La envolvente del tren de ondas — el contorno de amplitud que envuelve las oscilaciones rápidas — se mueve con la velocidad de grupo.

La velocidad de grupo es la velocidad de *transporte de energía* en el paquete. Si la velocidad de fase $c_p > c_g$, la cresta de la onda parece avanzar desde la parte trasera del paquete hacia el frente (los frentes de fase superan a la energía). Si $c_p < c_g$, ocurre lo contrario. En medios no dispersivos, $c_p = c_g$ y el paquete no se deforma.

## Formulación matemática

La velocidad de grupo se define como:

$$c_g = \frac{d\omega}{dk}$$

En términos de la [[Phase Velocity|velocidad de fase]] $c_p = \omega/k$:

$$c_g = c_p + k\frac{dc_p}{dk} = c_p - \lambda\frac{dc_p}{d\lambda}$$

La segunda forma muestra que $c_g < c_p$ cuando la velocidad de fase crece con la longitud de onda (medio normalmente dispersivo). Para [[Rayleigh Waves]] en medios estratificados normalmente dispersivos, es habitual que $c_g < c_p$.

## Derivación para superposición de dos ondas

Para dos ondas de igual amplitud con frecuencias y números de onda cercanos:

$$\phi(x,t) = A\sin(k_1 x - \omega_1 t) + A\sin(k_2 x - \omega_2 t)$$

La suma se puede escribir como:

$$\phi(x,t) = 2A\cos\!\left(\frac{k_1-k_2}{2}x - \frac{\omega_1-\omega_2}{2}t\right)\cdot\sin\!\left(\frac{k_1+k_2}{2}x - \frac{\omega_1+\omega_2}{2}t\right)$$

- El **seno** oscila con la frecuencia media → portadora, viaja a $c_p$
- El **coseno** forma la envolvente → viaja a $\Delta\omega/\Delta k \to d\omega/dk = c_g$

## Relación con la curva de dispersión

Tanto $c_p$ como $c_g$ pueden extraerse de la misma [[Dispersion Relation|relación de dispersión]] $\omega(k)$:

- $c_p(k) = \omega(k)/k$ — pendiente del vector desde el origen hasta el punto en la curva $\omega(k)$
- $c_g(k) = d\omega/dk$ — pendiente tangente a la curva en ese punto

En un medio normalmente dispersivo (velocidad crece con profundidad), la curva $\omega(k)$ es cóncava: $c_g < c_p$ en todas las frecuencias.

## Rol en sismología vs. métodos de sitio

| Contexto | Uso de $c_g$ vs. $c_p$ |
|---|---|
| Sismología global (períodos largos) | $c_g$ observable como velocidad del tren de ondas; usada en tomografía de ondas superficiales |
| Métodos MASW/SASW (near-surface) | $c_p$ es el observable primario; $c_g$ es de importancia secundaria en inversión |
| Análisis de registros dispersivos | $c_g$ controla la llegada temporal de las componentes de energía |

En métodos MASW estándar, el análisis f-k extrae $c_p$. La velocidad de grupo aparece implícitamente en el *moveout* temporal del tren de ondas visible en el sismograma: en un medio dispersivo, las componentes de baja frecuencia (longitud de onda larga, mayor profundidad de penetración) llegan antes que las de alta frecuencia. Esta "dispersión temporal" del ground-roll es la firma visual de la heterogeneidad del subsuelo.

## Implicaciones para el diseño experimental

- En registros de arreglos sísmicos, la **forma del tren de ondas de Rayleigh** (su estiramiento temporal) depende de $c_g$. Si el tren de ondas es muy corto en tiempo, puede haber interferencia entre diferentes modos.
- Para métodos que analizan la **forma de onda** directamente (como la inversión de forma de onda completa), $c_g$ es tan relevante como $c_p$.
- En el método de análisis MASW con ventana temporal de análisis, conviene asegurarse de que la ventana capture el tren completo de ondas superficiales — cuyo tamaño temporal depende de $c_g$ y la dispersión del arreglo.

## Referencias

- Foti et al. (2014), Cap. 2.1.2, pp. 41–43, Ec. 2.13 — derivación de $c_g$ para superposición de dos ondas.
- Foti et al. (2014), Cap. 4.1, pp. 206–208 — relación entre $c_p$ y $c_g$ en el contexto de métodos de ondas superficiales.
