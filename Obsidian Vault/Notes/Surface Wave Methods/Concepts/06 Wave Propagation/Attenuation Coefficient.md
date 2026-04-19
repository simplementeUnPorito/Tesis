---
name: Attenuation Coefficient
description: Coeficiente de decaimiento espacial de la amplitud de onda por absorción viscoelástica — parámetro que vincula el amortiguamiento del suelo DS con la curva de [[Attenuation|atenuación]] de Rayleigh
type: reference
---

# Attenuation Coefficient — Coeficiente de [[Attenuation|Atenuación]] ($\alpha$)

> [!CONCEPT] Definición
> El **coeficiente de [[Attenuation|atenuación]]** $\alpha$ (o $\alpha_R$ para ondas de Rayleigh) es la tasa de decaimiento exponencial de la **amplitud** de la onda con la distancia de propagación en un medio [[Viscoelastic Media|viscoelástico]]:
> $$A(x) = A_0 \cdot e^{-\alpha x}$$
> donde $A_0$ es la amplitud en $x = 0$ y $\alpha$ tiene unidades de Np/m (Neper por metro) o dB/m. Para ondas de Rayleigh en un semi-espacio viscoelástico estratificado, el coeficiente de [[Attenuation|atenuación]] $\alpha_R(\omega)$ se obtiene de la parte imaginaria del [[Wavenumber|número de onda]] de Rayleigh complejo $\hat{k}_R = k_R - i\alpha_R$ — que es la solución de la ecuación secular compleja mediante el [[Correspondence Principle|Principio de Correspondencia]]. La relación entre $\alpha_R$ y el [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s$ (promediado sobre el perfil de profundidad por los [[Sensitivity Kernel|kernels de sensibilidad]]) es:
> $$\alpha_R(\omega) \approx \frac{\omega \, D_s^{eff}(\omega)}{c_R(\omega)}$$
> donde $D_s^{eff}$ es el amortiguamiento efectivo de Rayleigh. La curva experimental $\alpha_R^{obs}(f)$ — obtenida del **decaimiento de la amplitud con la distancia** en el sismograma [[MASW Method|MASW]] (tras la corrección por [[Geometric Spreading|dispersión geométrica]] $A \propto 1/\sqrt{r}$) — es la **curva de [[Attenuation|atenuación]] de Rayleigh**, que se invierte para obtener el perfil $D_s(z)$.
>
> — Foti et al. (2018), §2.2, §7.3; Aki & Richards (2002), §5.5; Lai & Rix (1998).

## Relación con el factor de calidad Q

El coeficiente de [[Attenuation|atenuación]] y el **factor de calidad** $Q$ (inverso del amortiguamiento) se relacionan:

$$\alpha = \frac{\omega}{2Qc} = \frac{\omega D_s}{c}, \quad Q = \frac{1}{2D_s}$$

Para ondas de corte en suelos: $Q_S$ = 5–100 (suelos blandos: $Q_S$ = 5–20, $D_s$ = 2.5–10%; rocas: $Q_S$ = 50–200, $D_s$ = 0.25–1%).

## Estimación experimental en [[MASW Method|MASW]]

### Paso 1: Extracción de la curva de amplitud

En el sismograma multicanal, la amplitud espectral a la frecuencia $f$ decae con la distancia $x_j$ de cada [[Geophone|geófono]]:

$$A(f, x_j) = A_0(f) \cdot x_j^{-1/2} \cdot e^{-\alpha_R(f) x_j} \cdot H_{src}(f)$$

donde $x_j^{-1/2}$ es la [[Geometric Spreading|dispersión geométrica]] para ondas 2D (Rayleigh cilíndrico) y $H_{src}(f)$ es la función de fuente.

### Paso 2: Corrección de dispersión geométrica

Multiplicando las amplitudes por $\sqrt{x_j}$, el decaimiento residual es puramente exponencial:

$$\tilde{A}(f, x_j) = A(f, x_j) \cdot \sqrt{x_j} = A_0(f) \cdot H_{src}(f) \cdot e^{-\alpha_R(f) x_j}$$

### Paso 3: Ajuste exponencial

$\alpha_R(f)$ se estima por regresión lineal de $\ln \tilde{A}$ vs $x_j$:

$$\ln \tilde{A}(f, x_j) = \ln[A_0 H_{src}] - \alpha_R(f) \cdot x_j$$

La pendiente da $\alpha_R(f)$ directamente.

## Dificultades prácticas

1. **Campo cercano**: en [[Geophone|geófono]] próximos a la fuente ($x < \lambda$), la amplitude no sigue la ley de campo lejano → usar solo $x > 1{-}2\lambda$
2. **Scattering superficial**: heterogeneidades laterales producen fluctuaciones de amplitud no relacionadas con $D_s$ → ruido en la estimación de $\alpha_R$
3. **Función de fuente**: $H_{src}(f)$ modifica la amplitud inicial → necesita ser eliminada (promedio espacial, o [[Geophone|geófono]] en campo lejano)

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — curva de [[Attenuation|atenuación]] de Rayleigh en el sitio de Pisa
> Foti et al. (2018, §7.3) presentan la estimación experimental del coeficiente de [[Attenuation|atenuación]] $\alpha_R(f)$ en el sitio de Pisa (Torre di Pisa) a partir de datos [[MASW Method|MASW]] multicanal. Tras la corrección por dispersión geométrica ($\sqrt{x}$), el ajuste exponencial de la amplitud espectral en el rango 5–30 Hz produce la curva $\alpha_R(f)$ con valores de 0.005–0.05 Np/m — equivalente a $D_s^{eff}$ = 2–6% (suelo arcilloso de alta plasticidad). La inversión de $\alpha_R(f)$ por el [[Correspondence Principle|Principio de Correspondencia]] produce el perfil $D_s(z)$ que concuerda con los ensayos de [[Resonant Column Test|columna resonante]] en muestras del mismo sitio dentro de ±1–1.5% en valor absoluto. Los autores identifican que la fuente principal de incertidumbre en $\alpha_R^{obs}$ es la variabilidad entre disparos (±15–20%), que se reduce promediando múltiples fuentes.
>
> — Foti et al. (2018), §7.3, pp. 375–380, Figs. 7.25–7.29.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.2; §7.3 — estimación y inversión de αR |
| Lai & Rix (1998), *J. Geotech. Geoenviron.* | Inversión simultánea VS+DS mediante αR de Rayleigh |
| Aki & Richards (2002), *Quantitative Seismology* | §5.5 — [[Attenuation|atenuación]] de ondas sísmicas |
