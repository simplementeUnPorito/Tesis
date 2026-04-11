---
name: Gardner Relations
description: Relación empírica ρ=0.31·VP^0.25 entre densidad bulk y velocidad VP — usada para estimar densidad a partir de perfiles sísmicos en [[Joint Inversion|inversión conjunta]] y en la conversión de perfiles [[MASW Method|MASW]] a módulo de corte G=ρVS²
type: reference
---

# Gardner Relations — Relaciones de Gardner

> [!CONCEPT] Definición
> Las **relaciones de Gardner** (Gardner et al. 1974) son las correlaciones empíricas entre la **densidad bulk** $\rho$ y la **velocidad de onda P** $V_P$ de rocas y suelos sedimentarios:
> $$\rho = a \, V_P^b$$
> con los parámetros empíricos de Gardner: $a = 0.31$ (con $V_P$ en m/s y $\rho$ en g/cm³) y $b = 0.25$. La relación potencial refleja la covarianza general entre densidad y rigidez en materiales sedimentarios: litologías más compactas y de mayor rigidez tienden también a ser más densas. En el contexto de los métodos de [[Surface Waves|ondas superficiales]], las relaciones de Gardner son útiles en dos aplicaciones principales:
> (1) **Conversión $V_S \to G_{max}$**: el módulo de corte máximo $G_{\max} = \rho V_S^2$ requiere estimar $\rho$ cuando no hay mediciones directas de densidad — las relaciones de Gardner permiten estimarla a partir del perfil $V_P$ (obtenido por [[Seismic Refraction|refracción sísmica]]) sin necesidad de sondeos adicionales; (2) **[[Joint Inversion|inversión conjunta]]**: en problemas de inversión multi-parámetro ($V_S$, $V_P$, $\rho$), la relación de Gardner actúa como vínculo petrofísico que reduce los grados de libertad del modelo, mejorando la estabilidad de la inversión.
>
> — Gardner et al. (1974), *Geophysics* 39(6), 770–780; Foti et al. (2018), §8.6.1; Sheriff & Geldart (1995).

## Precisión y limitaciones

La relación de Gardner es una correlación promedio sobre muchas litologías — la dispersión es considerable:

| Litología | $\rho$ (g/cm³) | $V_P$ (km/s) | Error típico Gardner |
|-----------|---------------|--------------|---------------------|
| Arena limpia saturada | 2.0–2.1 | 1.5–2.5 | ±5% |
| Arenisca consolidada | 2.2–2.5 | 3.0–5.0 | ±8% |
| Caliza | 2.4–2.7 | 4.0–6.5 | ±10% |
| Suelo aluvial saturado | 1.9–2.1 | 1.5–1.8 | ±12% |
| Arcilla blanda | 1.6–1.9 | 1.5–1.7 | ±15% |

Para suelos geotécnicos superficiales (la mayoría con $V_P \approx 1500$ m/s saturados), la relación predice $\rho \approx 1.9$ g/cm³ — razonable para la mayoría de suelos sedimentarios, pero con error > 10% en arcillas blandas.

## Uso en la estimación de G_max

La secuencia completa para obtener $G_{\max}$ sin densímetro:
1. [[MASW Method|MASW]] → $V_S(z)$
2. [[Seismic Refraction|Refracción]] → $V_P(z)$
3. Gardner: $\rho(z) = 0.31 \cdot V_P(z)^{0.25}$
4. $G_{\max}(z) = \rho(z) \cdot V_S(z)^2$

La incertidumbre en $G_{\max}$ combinando errores de [[MASW Method|MASW]] (~5%) y Gardner (~10%) es ~11% — aceptable para diseño geotécnico preliminar.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Gardner para estimación de densidad en inversión multi-parámetro
> Foti et al. (2018, §8.6.1) aplican las relaciones de Gardner para estimar $\rho(z)$ en el sitio La Salle usando el perfil $V_P$ de refracción (1.5–1.7 km/s). La densidad estimada es $\rho = 0.31 \times (1600)^{0.25} = 1.95$ g/cm³ (zona saturada) — diferencia de +3% respecto a la densidad promedio de laboratorio ($1.89 \pm 0.05$ g/cm³). Con esta densidad, $G_{\max}(4\text{ m}) = 1.95 \times (200)^2 = 78$ MPa — consistente con ensayos de columna resonante que dan 75 ± 8 MPa. Foti concluye que Gardner es adecuado cuando no hay datos de densidad directos, pero debe verificarse contra al menos una medición en sitios con litologías atípicas.
>
> — Foti et al. (2018), §8.6.1; Gardner et al. (1974), *Geophysics* 39(6), 770–780.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Gardner, Gardner & Gregory (1974), *Geophysics* 39(6), 770–780 | Relaciones empíricas densidad-VP originales |
| Foti et al. (2018), *Surface Wave Methods* | §8.6.1 — petrofísica en [[Joint Inversion|inversión conjunta]] |
| Sheriff & Geldart (1995), *Exploration Seismology* | §5 — relaciones petrofísicas |
