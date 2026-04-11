---
name: Cross-Correlation
description: Operación matemática que mide la similitud entre dos señales en función del desfase — base de la [[Seismic Interferometry|interferometría sísmica]] y la estimación de velocidad en métodos de [[Surface Waves|ondas superficiales]]
type: reference
---

# Cross-Correlation — Correlación Cruzada

> [!CONCEPT] Definición
> La **correlación cruzada** (*cross-correlation*) es una operación matemática que mide la **similitud** entre dos señales $u_1(t)$ y $u_2(t)$ en función del **desfase temporal** $\tau$:
> $$R_{12}(\tau) = \int_{-\infty}^{\infty} u_1(t) \cdot u_2(t + \tau) \, dt = (u_1 \star u_2)(\tau)$$
> En el dominio de la frecuencia, es el producto de la Transformada de Fourier de una señal por el conjugado complejo de la otra: $\hat{R}_{12}(\omega) = \hat{U}_1^*(\omega) \cdot \hat{U}_2(\omega)$ — que es el espectro de potencia cruzado ([[Cross-Power Spectrum]]). El pico de $R_{12}(\tau)$ ocurre al desfase $\tau^*$ que maximiza la similitud — en señales sísmicas, $\tau^*$ es el **tiempo de viaje** de la onda de una estación a la otra. La correlación cruzada es la base de dos aplicaciones fundamentales en métodos de [[Surface Waves|ondas superficiales]]: (1) la estimación de [[Phase Velocity|velocidad de fase]] en [[SASW Method|SASW]] (a través del [[Cross-Power Spectrum|espectro de potencia cruzado]]); y (2) la recuperación de la función de Green del medio en [[Seismic Interferometry|interferometría sísmica]] — la correlación cruzada de registros de ruido ambiental entre dos receptores converge a la función de Green entre ellos con suficiente promediado temporal.
>
> — Foti et al. (2018), §4.5; Snieder (2004); Shapiro & Campillo (2004).

## Estimación de [[Phase Velocity|velocidad de fase]] en [[SASW Method|SASW]]

En [[SASW Method|SASW]], se coloca la fuente en superficie y se usan dos receptores a distancias $x_1$ y $x_2$. La [[Phase Velocity|velocidad de fase]] de Rayleigh a la frecuencia $f$ se estima del desfase de la correlación cruzada:

$$\phi_{12}(f) = \arg\left[\hat{U}_1^*(f) \cdot \hat{U}_2(f)\right] = \frac{2\pi f (x_2 - x_1)}{c_R(f)}$$

→ $c_R(f) = \frac{2\pi f (x_2 - x_1)}{\phi_{12}(f)}$

Este es el principio del [[Cross-Power Spectrum|espectro de potencia cruzado]] en [[SASW Method|SASW]]. La ambigüedad de $\pm 2\pi$ en $\phi_{12}$ requiere [[Phase Unwrapping|phase unwrapping]].

## Interferometría sísmica: función de Green por correlación cruzada

Para ruido sísmico difuso (campo de ondas isotrópico), la correlación cruzada de registros en dos receptores A y B promediada en el tiempo converge a la función de Green:

$$\langle u_A(t) \star u_B(t) \rangle_t \propto G_{AB}(t) - G_{AB}(-t)$$

donde $G_{AB}(t)$ es la función de Green entre A y B (la señal que se observaría en B si hay un impulso en A). Para [[Surface Waves|ondas superficiales]], la función de Green contiene las ondas de Rayleigh y Love — su análisis da la [[Dispersion Curve|curva de dispersión]] de la onda entre A y B, que permite la inversión del perfil $V_S(z)$.

## Propiedades matemáticas

| Propiedad | Fórmula | Relevancia |
|-----------|---------|-----------|
| Simetría | $R_{12}(\tau) = R_{21}(-\tau)$ | Causalidad en interferometría |
| Máximo en $\tau=0$ para señal idéntica | $R_{11}(0) = \|u_1\|^2$ | Auto-correlación = potencia |
| Dominio frecuencial | $\hat{R}_{12} = \hat{U}_1^* \hat{U}_2$ | [[Cross-Power Spectrum]] |
| Convolución vs correlación | $\hat{R}_{12} = \hat{U}_1^* \hat{U}_2 \neq \hat{U}_1 \hat{U}_2$ | No conmutar los operandos |

> [!EXAMPLE] Evidencia empírica: Shapiro & Campillo (2004) — correlación cruzada de ruido ambiental para la función de Green
> **Shapiro & Campillo (2004)** demuestran que la correlación cruzada de registros de ruido sísmico ambiental entre estaciones sísmicas separadas hasta ~1000 km reproduce la **función de Green de [[Surface Waves|ondas superficiales]]** entre las estaciones. Para períodos de 5–150 s, las ondas de Rayleigh y Love emergen de la correlación cruzada con coherencia suficiente para medir la velocidad de grupo entre pares de estaciones. Este es el fundamento de la [[Seismic Interferometry|interferometría sísmica]] pasiva — aplicada en [[MASW Method|MASW]] pasivo y [[SPAC Method|SPAC]] para estimar la [[Dispersion Curve|curva de dispersión]] sin fuente activa. En el contexto de [[ReMi Method|ReMi]], la correlación cruzada entre geófonos en arreglos urbanos produce la función de Green de ondas de Rayleigh del subsuelo local.
>
> — Shapiro & Campillo (2004), *Science* 307; Foti et al. (2018), §4.5.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §4.5 — cross-correlación en [[Seismic Interferometry|interferometría sísmica]] |
| Shapiro & Campillo (2004), *Science* 307 | Función de Green por correlación cruzada de ruido ambiental |
| Snieder (2004), *Phys. Rev. E* | Fundamento teórico de la correlación cruzada en ruido difuso |
