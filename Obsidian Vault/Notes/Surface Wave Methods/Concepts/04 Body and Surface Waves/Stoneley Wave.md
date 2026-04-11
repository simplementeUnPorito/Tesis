---
name: Stoneley Wave
description: Onda interfacial que se propaga a lo largo de la frontera entre dos semiespacios sólidos o sólido-fluido — variante submarina de las ondas de Scholte — relevante en perfilaje de pozos y sísmica marina de fondo
type: reference
---

# Stoneley Wave — Onda de Stoneley

> [!CONCEPT] Definición
> Las **ondas de Stoneley** son ondas interfaciales que se propagan a lo largo de la frontera entre **dos semiespacios elásticos sólidos** (o sólido-fluido), con amplitud que decae exponencialmente en ambos medios desde la interfaz. Son la generalización de las [[Rayleigh Waves|ondas de Rayleigh]] para una interfaz enterrada (no superficie libre). La [[Phase Velocity|velocidad de fase]] $c_{St}$ es menor que las velocidades de onda de corte de ambos medios:
> $$c_{St} < \min(V_{S1}, V_{S2})$$
> En el caso de una interfaz **sólido-fluido** (como el fondo marino), las ondas de Stoneley se denominan también [[Scholte Waves|ondas de Scholte]]. En el contexto de **perfilaje de pozos** (*borehole logging*), las ondas de Stoneley son la respuesta interfacial del fluido de perforación (agua) contra la formación rocosa: se propagan a lo largo del pozo con velocidad $c_{St} \approx V_{fluid} \cdot (1 + V_{fluid}/V_S)^{-1/2}$, siendo sensibles a la permeabilidad y al módulo de corte del suelo adyacente. Las ondas de Stoneley no se usan directamente en [[MASW Method|MASW]] convencional, pero son relevantes en el análisis de datos de sondeos sísmicos verticales (VSP) y en la caracterización multi-método de sitios complejos.
>
> — Foti et al. (2018), §8.5.2, pp. 438–445; Stoneley (1924), *Proc. R. Soc. London A* 106, 416–428; Scholte (1947).

## Comparación: Stoneley vs. Scholte vs. Rayleigh

| Tipo | Interfaz | Condición de existencia | Velocidad |
|------|---------|------------------------|-----------|
| Rayleigh | Superficie libre (vacío-sólido) | Siempre existe | $c_R \approx 0.92 V_S$ |
| Stoneley | Sólido-sólido | Siempre existe (si densidades compatibles) | $c_{St} < \min(V_{S1}, V_{S2})$ |
| Scholte | Sólido-fluido (fondo marino) | Siempre existe | $c_{Sc} < \min(V_{S,sed}, c_{agua})$ |
| Love | Capa sobre semiespacio ($V_{S2} > V_{S1}$) | Requiere contraste de velocidad | $V_{S1} < c_L < V_{S2}$ |

## Propiedades físicas

- **Decaimiento evanescente** a ambos lados de la interfaz: la amplitud decae como $e^{-\kappa_i z}$ donde $\kappa_i = k\sqrt{1 - c_{St}^2/V_{Si}^2}$ en cada medio
- **Sin dispersión** en medios homogéneos (velocidad independiente de la frecuencia) — a diferencia de [[Rayleigh Waves]] en medios estratificados
- **Partícula elíptica** en el plano vertical (similar a Rayleigh), con retrograde motion en el medio más rígido
- **Sensibilidad al fluido**: en interfaces sólido-fluido, $c_{St}$ depende fuertemente de $K_f$ del fluido y la permeabilidad

## Aplicación en perfilaje de pozos

En un pozo lleno de fluido, la onda de Stoneley de tubo (*tube wave*) tiene velocidad:
$$c_{tube} = V_f \left(1 + \frac{\rho_f V_f^2}{K_{sk}}\right)^{-1/2}$$

La atenuación de la onda de tubo es proporcional a la permeabilidad $k_0$ del suelo circundante (flujo de Poiseuille oscilatorio en los poros). Esta propiedad se usa en la evaluación hidráulica de formaciones.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — ondas de Stoneley en sísmica marina de fondo
> Foti et al. (2018, §8.5.2) presentan el análisis de ondas de Stoneley registradas con una línea de OBS (*ocean bottom seismometers*) en sedimentos marinos blandos del Mar del Norte. La velocidad de Stoneley medida es $c_{St} \approx 120$ m/s — menor que $V_S \approx 150$ m/s de los sedimentos superficiales, confirmando la condición $c_{St} < V_S$. La dispersión observada (variación de $c_{St}$ de 100 a 145 m/s entre 5 y 50 Hz) refleja la estratificación de los sedimentos en los primeros 15 m. La [[Joint Inversion|inversión conjunta]] con las [[Scholte Waves|ondas de Scholte]] (modo de Rayleigh de fondo) mejora la determinación del $V_S$ en la capa superficial saturada: las ondas de Stoneley son más sensibles a $V_S$ en los primeros 2–3 m mientras que las ondas de Scholte penetran hasta 15–20 m, complementando el perfil.
>
> — Foti et al. (2018), §8.5.2, pp. 438–445; Stoneley (1924), *Proc. R. Soc. London A* 106, 416–428.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §8.5.2 — Stoneley en sísmica marina |
| Stoneley, R. (1924), *Proc. R. Soc. London A* 106, 416–428 | Descubrimiento y análisis original |
| Scholte, J.G. (1947), *Geophys. J. Int.* | Generalización para interfaz sólido-fluido |
