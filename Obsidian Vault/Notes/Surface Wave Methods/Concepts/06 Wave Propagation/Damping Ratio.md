---
aliases: [razón de amortiguamiento, factor de amortiguamiento, D, damping ratio]
tags: [viscoelasticity, attenuation, material-properties]
---

# Damping Ratio (Razón de Amortiguamiento)

La **razón de amortiguamiento** $D$ (o *damping ratio*) es un parámetro adimensional que cuantifica la fracción de energía elástica disipada por ciclo de deformación en un material [[Viscoelastic Media|viscoelástico]]. Se define como:

$$
D = \frac{\Delta W}{4\pi W}
$$

donde $\Delta W$ es la energía disipada por ciclo y $W$ es la energía de deformación máxima almacenada. En términos del **módulo dinámico complejo** $G^* = G_{(1)} + iG_{(2)}$:

$$
D = \frac{G_{(2)}}{2G_{(1)}} = \frac{\tan\delta}{2}
$$

donde $\delta$ es el **ángulo de pérdida** (phase lag) entre esfuerzo y deformación, y $\tan\delta$ es el **factor de pérdida**.

## Relación con el factor de calidad Q

El factor de calidad $Q$ (muy usado en sismología) es el inverso de dos veces el amortiguamiento:

$$
Q = \frac{1}{2D}, \qquad D = \frac{1}{2Q}
$$

Para medios con bajo amortiguamiento ($D \ll 1$), el decaimiento espacial de amplitud de una onda monocromática es:

$$
A(x) = A_0\,e^{-\alpha x}, \qquad \alpha = \frac{\omega D}{V_\chi(\omega)}
$$

donde $\alpha$ es el coeficiente de atenuación espacial y $V_\chi$ la velocidad de fase.

## Valores típicos en geomateriales

| Material | $D_S$ (corte) | Condición |
|----------|--------------|-----------|
| Roca sana | 0.5–2% | Pequeña deformación |
| Suelo arenoso denso | 1–3% | Pequeña deformación |
| Arcilla consolidada | 2–5% | Pequeña deformación |
| Suelo blando saturado | 3–8% | Pequeña deformación |
| Suelos en estado plástico | 10–20%+ | Grandes deformaciones |

Para la hipótesis de **disipación débil** ($D \leq 5\%$), el [[Correspondence Principle|principio de correspondencia]] permite tratar el problema viscoelástico como perturbación del elástico.

## Distinción: $D_S$ vs. $D_P$

- **$D_S$** (amortiguamiento de corte): controla la atenuación de [[S-Waves|ondas S]] y [[Rayleigh Waves|ondas de Rayleigh]]. Es el parámetro relevante para la ingeniería geotécnica sísmica.
- **$D_P$** (amortiguamiento compresional): controla la atenuación de [[P-waves|ondas P]]. En geomateriales saturados está dominado por el mecanismo de Biot (flujo poral), no por el esqueleto sólido.

Los métodos de [[MASW Method|ondas superficiales]] permiten estimar $D_S(z)$ in situ midiendo el decaimiento espacial de la amplitud de las [[Rayleigh Waves|ondas de Rayleigh]] — esto se desarrolla en detalle en el Capítulo 5 de Foti et al. (2014). El parámetro $D_S$ equivale a la razón de amortiguamiento en corte del material en condiciones de pequeña deformación (*linear threshold shear strain*).

## Nota: relación con [[Shear Damping Ratio]]

La nota [[Shear Damping Ratio]] es un concepto más específico que se refiere a $D_S$ medido con ondas superficiales en el contexto de la [[Inversión|inversión]] de atenuación. Esta nota describe la definición general del parámetro adimensional $D$.

## Véase también

- [[Shear Damping Ratio]] — $D_S$ específicamente para ondas de corte en caracterización de sitio
- [[Quality Factor]] — inverso: $Q = 1/(2D)$
- [[Attenuation Coefficient]] — coeficiente $\alpha$ que cuantifica el decaimiento espacial
- [[Viscoelastic Media]] — marco constitutivo donde $D$ es un parámetro del material
- [[Correspondence Principle]] — permite tratar $D$ como perturbación al caso elástico para $D \leq 5\%$
- [[Kramers-Kronig Relations]] — vinculan $D(\omega)$ con $V(\omega)$ — no son independientes

*Fuente: Foti et al. (2014), Sec. 2.5.1–2.5.2, pp. 96–110.*
