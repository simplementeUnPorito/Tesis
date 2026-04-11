---
name: Material Dispersion
description: Dispersión debida a propiedades constitutivas frecuencia-dependientes del material (viscoelasticidad, saturación, porosidad) — distinta de la dispersión geométrica por estratificación
type: reference
---

# Material Dispersion — Dispersión Material

> [!CONCEPT] Definición
> La **dispersión material** (o intrínseca) ocurre cuando la velocidad de propagación depende de la frecuencia a causa de las **propiedades constitutivas del material**, no de la estratificación geométrica del medio. Es la contraparte de la [[Wave Dispersion|dispersión geométrica]]: mientras la dispersión geométrica surge de la estratificación vertical y es el observable central del [[MASW Method|MASW]], la dispersión material surge de la viscoelasticidad, la saturación o el acoplamiento fluido-esqueleto. En medios [[Viscoelastic Media|viscoelásticos]], los módulos complejos $\tilde{\mu}(\omega) = \mu_R(\omega)(1 + 2iD_s)$ son frecuencia-dependientes → distintas componentes espectrales "ven" rigideces efectivas distintas. En suelos típicos con $D_s < 10\%$, el efecto sobre la velocidad de fase es de **segundo orden en $D_s$** (despreciable para la inversión de $V_S$), pero la dispersión material produce un gradiente de velocidad de fase adicional que puede confundirse con la dispersión geométrica si no se modela correctamente.
>
> — Foti et al. (2018), Cap. 2, §2.1.1, pp. 40–41; §2.5 — medios disipativos.

## Fundamento físico

En un medio elástico lineal ideal, las velocidades de fase de ondas P y S son independientes de la frecuencia (no-dispersivas). La dispersión material aparece cuando:

- El medio es **viscoelástico** (fricción interna entre partículas → módulo complejo $\tilde{\mu}(\omega)$)
- El medio es **poroso saturado** (acoplamiento fluido-esqueleto de Biot → velocidad de onda P frecuencia-dependiente; por encima de la frecuencia de Biot, la onda P pasa de "lenta" a "rápida")
- El medio es **multicomponente** (mezcla de materiales con respuesta mecánica diferente)

## Distinción de la dispersión geométrica

| Tipo | Origen | Observable en MASW | Magnitud típica |
|---|---|---|---|
| [[Wave Dispersion|Dispersión geométrica]] | Estratificación vertical | Variación $c_R(f)$ — principal observable | Dominante (50–200%) |
| Dispersión material | Propiedades constitutivas | Gradiente residual en $c_R(f)$ | Secundario (<5% para $D_s < 10\%$) |

## Cuando la dispersión material es relevante en ondas superficiales

En ensayos near-surface, la dispersión observada está **dominada por la estratificación** (dispersión geométrica). La dispersión material puede volverse apreciable cuando:

1. **Alto amortiguamiento**: $D_s > 5\%$ (arcillas blandas, rellenos contaminados) → el gradiente de velocidad de fase tiene contribución viscoelástica no despreciable.
2. **Saturación parcial**: la transición zona no saturada / zona saturada introduce variaciones de $V_P$ y $\nu$ que afectan la velocidad de Rayleigh (ver [[Poisson Ratio]]).
3. **Medios porosos con alta frecuencia de Biot**: en arenas limpias con frecuencias sísmicas elevadas (>100 Hz), la dispersión de Biot puede contribuir.
4. **Atenuación de sitio marcada**: si la fuente es muy próxima, la curva de atenuación $\alpha_R(f)$ contiene dispersión material del [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s(z)$.

## Implicación práctica

No se debe atribuir **toda** la dispersión observada a la estratificación vertical. En sitios con suelos altamente atenuantes o saturados, la dispersión material introduce un sesgo sistemático en la curva de dispersión si no se corrige. La separación entre ambos tipos de dispersión requiere un modelo físico explícito — no es posible por inspección visual de la curva. En práctica estándar, se asume dispersión material despreciable y se modela la curva de dispersión con medios elásticos; esto es válido cuando $D_s < 5\%$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — dispersión material vs geométrica en sitio de Pisa
> Foti et al. (2018, §7.3) realizan la inversión simultánea de la curva de dispersión y la curva de atenuación en la Torre de Pisa (arcilla de alta plasticidad con $D_s \sim 3$–$5\%$). Al modelar solo la dispersión geométrica (medio elástico), el ajuste de la curva de dispersión es bueno — el efecto de $D_s$ sobre $c_R(f)$ es de segundo orden y menor que la incertidumbre experimental (~1%). Sin embargo, la curva de atenuación $\alpha_R(f)$ solo se ajusta correctamente cuando se incluye el modelo viscoelástico (dispersión material del amortiguamiento). El resultado confirma que para estimación de $V_S$ se puede despreciar la dispersión material, pero para estimación de $D_s$ es imprescindible incluirla.
>
> — Foti et al. (2018), §7.3, pp. 375–380; §2.1.1, pp. 40–41.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.1.1, pp. 40–41 — dos categorías de dispersión |
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.5 — propagación en medios disipativos |
| Foti et al. (2018), *Surface Wave Methods* | §7.3 — inversión simultánea VS y DS en Pisa |
