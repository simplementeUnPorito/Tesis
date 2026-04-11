---
name: Joint Inversion
description: Inversión simultánea de múltiples tipos de datos geofísicos para reducir la no-unicidad y mejorar la resolución del perfil Vs mediante vínculos estructurales o petrofísicos
type: reference
---

# Joint Inversion — Inversión Conjunta Multi-Método

> [!CONCEPT]
> La **inversión conjunta** (joint inversion) minimiza simultáneamente el desajuste de dos o más conjuntos de datos geofísicos mediante un funcional unificado:
>
> $$\Phi = \alpha_1\|\mathbf{J}_1\mathbf{m} - \mathbf{d}_1\|^2 + \alpha_2\|\mathbf{J}_2\mathbf{m} - \mathbf{d}_2\|^2 + \lambda^2\|\mathbf{L}\mathbf{m}\|^2$$
>
> Los pesos αᵢ equilibran la contribución de cada dataset según su incertidumbre. El objetivo es que cada método compense las debilidades del otro: [[MASW Method|MASW]] resuelve bien Vs pero no distingue saturación de fluidos; ERT detecta contraste de resistividad pero no diferencia rigidez. Combinados, reducen drásticamente la [[Non-uniqueness|no-unicidad]].

## Combinaciones más comunes en SWM

| Combinación | Vínculo | Complementariedad |
|-------------|---------|-------------------|
| [[MASW Method|MASW]] + ERT | [[Cross-Gradient Function]] o petrofísico ([[Archie's Law]]) | ERT → φ → VP (vía [[Wyllie Equation]]); [[MASW Method|MASW]] → VS, Gmax |
| [[MASW Method|MASW]] + HVSR | Elipticidad de Rayleigh | HVSR constrain f₀ = VS/4H → profundidad bedrock |
| [[MASW Method|MASW]] + refracción | VP y VS independientes | VP → saturación; VS → rigidez; Poisson ratio → estado tensional |
| Activo + Pasivo | Mismo modelo 1D | Activo → altas frecuencias (z < 10 m); Pasivo → bajas frecuencias (z > 20 m) |
| [[MASW Method|MASW]] + Love | Modos Love y Rayleigh | Love → VS puro (no contamina VP); Rayleigh → VS y VP acoplados |

## Tipos de vínculo entre métodos

### 1. Vínculo petrofísico (acoplamiento fuerte)
Se impone una relación cuantitativa entre los modelos de distintos métodos, e.g. Archie's Law para ERT→φ→VP. Requiere conocer los parámetros petrofísicos (m, n, a) del sitio.

### 2. [[Cross-Gradient Function|Vínculo estructural (cross-gradient)]]
No se asume ninguna relación petrofísica; se penaliza la diferencia en orientación de gradientes:
$$\mathbf{t} = \nabla m_1 \times \nabla m_2 = 0$$
Las interfaces deben co-localizarse, pero los valores pueden ser independientes. Útil cuando no se conoce la litología.

### 3. Ratio ponderado (acoplamiento débil)
Los datasets simplemente comparten el mismo espacio de modelos sin imposición explícita. La información de uno actúa como regularización implícita del otro a través del peso relativo αᵢ.

## Ventajas sobre inversión individual

- **Reduce no-unicidad**: cada dataset añade vínculos independientes sobre el mismo modelo
- **Mejora resolución en profundidad**: la combinación activo+pasivo extiende el rango frecuencial y por tanto el rango de profundidades sensibles
- **Vincula propiedades físicas independientes**: Vs (rigidez) + ρ_elec (fluidos) → estimación de saturación y porosidad
- **Detecta anomalías coherentes**: interferencias laterales visibles en ambos métodos son más confiables que en uno solo

## Esquemas de inversión

| Esquema | Descripción | Referencia |
|---------|-------------|-----------|
| Simultánea | Un único vector de modelo, un único sistema linealizado | Gallardo & Meju 2003 |
| Alternada | Cada método se invierte por separado, el resultado alimenta al siguiente | Lochbühler et al. 2013 |
| Acoplada por cross-gradient | Término de penalización en el funcional global | Gallardo & Meju 2004 |
| Bayesiana | Función de verosimilitud combinada, MCMC | Bodin et al. 2012 |

> [!EXAMPLE] Evidencia empírica (Foti et al. 2018, Parolai et al. 2005, Comina et al. 2002)
> - **Comina et al. (2002)** — Sitio Po river dike (dique del río Po, Italia): inversión conjunta [[MASW Method|MASW]] + ERT con cross-gradient constraint. La ERT detectó una anomalía de alta resistividad (arena gruesa) a 3–5 m que la [[MASW Method|MASW]] sola no resolvía. La inversión conjunta mejoró la correlación con perfiles de control (CPT) de r² = 0.71 → 0.89 en VS.
> - **Parolai et al. (2005)** — Joint inversion de [[Dispersion Curve|curvas de dispersión]] pasiva + razón H/V con algoritmo genético en 6 sitios de Colonia (Alemania). La no-unicidad en VS se redujo en ~40% comparado con inversión sola de dispersión. 239 citas confirman adopción amplia de este esquema.
> - **Arai & Tokimatsu (2005)** — Combinación de array pasivo + H/V: inversión conjunta exploró correctamente la profundidad a bedrock (VS > 800 m/s) a 60 m, donde la [[MASW Method|MASW]] activa (12 geófonos, 4 m separación) sólo alcanzaba 30 m.
> - **Foti et al. (2018, §8.3)** — Ensayo en Torre de Pisa: [[MASW Method|MASW]] + crosshole en inversión conjunta. Los perfiles VS de ambos métodos concordaron dentro del ±8% hasta 30 m, validando la consistencia del esquema.

## Referencias

| Autor | Año | Contribución |
|-------|-----|--------------|
| Gallardo & Meju | 2003 | Cross-gradient constraint para inversión conjunta geoeléctrica-sísmica |
| Gallardo & Meju | 2004 | Implementación de cross-gradient en inversión 2D conjunta |
| Parolai et al. | 2005 | Joint inversion dispersión + H/V con algoritmo genético (239 citas) |
| Arai & Tokimatsu | 2005 | Joint inversion microtremor + H/V en perfiles VS urbanos |
| Comina et al. | 2002 | [[MASW Method|MASW]]+ERT dique del Po con cross-gradient |
| Foti et al. | 2018 | §8.3, §8.4: ejemplos de joint inversion en site characterization |
