---
name: Archie's Law
description: Relación empírica ρ=a·ρw·φ⁻ᵐ·S⁻ⁿ entre la resistividad eléctrica del suelo saturado, la porosidad φ y la saturación S — usada para convertir datos ERT a propiedades petrofísicas en inversión conjunta con [[MASW Method|MASW]]
type: reference
---

# Archie's Law — Ley de Archie

> [!CONCEPT] Definición
> La **Ley de Archie** (Archie 1942) es la relación empírica fundamental que conecta la **resistividad eléctrica** $\rho_t$ de una roca o suelo poroso saturado con sus propiedades petrofísicas:
> $$\rho_t = a \, \rho_w \, \phi^{-m} \, S_w^{-n}$$
> donde:
> - $\rho_w$: resistividad del fluido intersticial (agua) [Ω·m]
> - $\phi$: porosidad (fracción volumétrica de poros)
> - $S_w$: saturación en agua (fracción de poros con agua, $0 \leq S_w \leq 1$)
> - $a$: factor de tortuosidad (~0.8–1.0 para arenas limpias)
> - $m$: exponente de cementación (~1.3–2.0 para arenas, mayor para calizas)
> - $n$: exponente de saturación (~2.0)
> En el contexto de la inversión conjunta [[MASW Method|MASW]] + ERT ([[Cross-Gradient Function|método de cross-gradients]] o acoplamiento petrofísico), la Ley de Archie proporciona el vínculo entre la resistividad medida eléctricamente y la porosidad — que a su vez se correlaciona con la velocidad sísmica $V_S$ mediante relaciones como la [[Wyllie Equation|ecuación de Wyllie]] o empíricas locales. Esto permite convertir modelos de resistividad en modelos de $V_S$ y viceversa, transformando la inversión conjunta en un problema de estimación petrofísica conjunta.
>
> — Archie (1942), *Trans. AIME* 146, 54–62; Foti et al. (2018), §8.6.1, pp. 447–450; Sheriff & Geldart (1995).

## Interpretación física

Para suelos completamente saturados ($S_w = 1$): $\rho_t = a \, \rho_w \, \phi^{-m}$ — la resistividad aumenta al disminuir la porosidad (menos vías de conducción iónica). El **factor de formación** $F = \rho_t/\rho_w = a\phi^{-m}$ mide cuánto más resistivo es el suelo que el agua intersticial.

### Casos límite geotécnicos relevantes

| Condición | $\rho_t$ typical |
|-----------|-----------------|
| Arcilla saturada ($\phi = 0.5$, $\rho_w = 0.5$ Ω·m) | ~0.5–2 Ω·m |
| Arena saturada ($\phi = 0.35$, $\rho_w = 10$ Ω·m) | ~15–50 Ω·m |
| Arena seca ($S_w = 0.1$) | ~500–5000 Ω·m |
| Roca no saturada | ~1000–10000 Ω·m |

La transición de arena saturada a seca (tabla de agua) produce un salto de 2 órdenes de magnitud en $\rho_t$ — visible en ERT como contraste nítido — mientras que $V_S$ permanece prácticamente invariante (ver [[Biot Theory]]).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Archie en acoplamiento ERT+[[MASW Method|MASW]] para sitio de dique del Po
> Foti et al. (2018, §8.6.1, pp. 447–450) aplican la Ley de Archie para convertir el modelo de resistividad ERT del dique del río Po en un modelo de porosidad $\phi(\mathbf{x})$, usando $\rho_w = 15$ Ω·m (medido en muestras de agua de poros) y parámetros de Archie $a = 0.9$, $m = 1.5$ calibrados en 3 sondeos CPT. La porosidad derivada de ERT varía entre 0.28 (grava compacta, capas profundas) y 0.48 (arcilla blanda, zona superficial) — rango consistente con las correlaciones $\phi$-$V_S$ de Robertson & Cabal 2015 para los tipos de suelos identificados en [[MASW Method|MASW]]. La correlación $r^2 = 0.73$ entre $\phi$(ERT) y $\phi$([[MASW Method|MASW]]-inferred) valida el uso de Archie como vínculo petrofísico en la inversión conjunta.
>
> — Foti et al. (2018), §8.6.1, pp. 447–450; Archie (1942), *Trans. AIME* 146, 54–62.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Archie, G.E. (1942), *Trans. AIME* 146, 54–62 | Ley empírica original de resistividad-porosidad |
| Foti et al. (2018), *Surface Wave Methods* | §8.6.1 — Archie en inversión conjunta [[MASW Method|MASW]]+ERT |
| Sheriff & Geldart (1995), *Exploration Seismology* | §5 — petrofísica eléctrica |
