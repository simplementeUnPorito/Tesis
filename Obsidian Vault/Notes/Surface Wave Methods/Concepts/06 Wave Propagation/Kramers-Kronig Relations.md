---
name: Kramers-Kronig Relations
description: Relaciones integrales que vinculan la parte real e imaginaria de cualquier función de respuesta causal — en viscoelasticidad conectan la [[Phase Velocity|velocidad de fase]] con el coeficiente de atenuación
type: reference
---

# Kramers-Kronig Relations — Relaciones de Kramers-Kronig

> [!CONCEPT] Definición
> Las **Relaciones de Kramers-Kronig (KK)** son relaciones integrales que vinculan la **parte real** e **imaginaria** de cualquier **función de respuesta lineal causal** — una consecuencia directa del principio de causalidad (la respuesta no puede preceder al estímulo) y del Teorema de Titchmarsh. En [[Viscoelastic Media|mecánica viscoelástica]], vinculan el **módulo de almacenamiento** $G'(\omega)$ (parte real → [[Phase Velocity|velocidad de fase]]) con el **módulo de pérdida** $G''(\omega)$ (parte imaginaria → atenuación):
> $$G'(\omega) = G_\infty + \frac{2}{\pi} \mathcal{P}\!\int_0^\infty \frac{\omega' G''(\omega')}{\omega'^2 - \omega^2} d\omega'$$
> $$G''(\omega) = -\frac{2\omega}{\pi} \mathcal{P}\!\int_0^\infty \frac{G'(\omega') - G_\infty}{\omega'^2 - \omega^2} d\omega'$$
> donde $G_\infty$ es el módulo elástico a frecuencia infinita y $\mathcal{P}$ denota la integral en valor principal de Cauchy. En el contexto de [[Surface Waves|ondas superficiales]], las KK conectan el [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s$ (que controla la [[Attenuation Coefficient|atenuación]] $\alpha$) con la [[Material Dispersion|dispersión de material]] (variación de la [[Phase Velocity|velocidad de fase]] con la frecuencia debida a la viscoelasticidad, no a la estratificación). Garantizan que cualquier modelo de atenuación que satisface la causalidad también implica dispersión de material — lo que debe tenerse en cuenta en la inversión de la [[Dispersion Curve|curva de dispersión]] de Rayleigh para separar **dispersión geométrica** (por capas) de **dispersión de material** (por viscoelasticidad).
>
> — Foti et al. (2018), §2.2; Aki & Richards (2002), §5.5; Kennett (1983), Cap. 4.

## Implicaciones para la propagación de ondas sísmicas

### Dispersión de material vs dispersión geométrica

En un medio viscoelástico estratificado, la [[Phase Velocity|velocidad de fase]] de la onda de Rayleigh varía con la frecuencia por **dos mecanismos**:
1. **Dispersión geométrica**: variación de $V_S(z)$ con la profundidad (mecanismo dominante)
2. **Dispersión de material**: cambio de la velocidad con la frecuencia del módulo viscoelástico de cada capa (mecanismo secundario)

Las KK garantizan que la dispersión de material (mecanismo 2) es consistente con el modelo de atenuación (Ds). Si se usa un modelo de $D_s$ constante con la frecuencia (*constant-Q model*), las KK implican una dispersión de material logarítmica:

$$V_S(\omega) = V_{S,ref} \left[1 + \frac{D_s}{\pi} \ln\!\left(\frac{\omega}{\omega_{ref}}\right)\right]$$

### Corrección en la inversión de [[MASW Method|MASW]]

Para $D_s$ típicos de suelos (1–10%), la dispersión de material introduce una variación de $c_R$ de ~0.5–2% por década de frecuencia — generalmente un efecto de segundo orden comparado con la dispersión geométrica (~50–200% de variación en $c_R$ en el rango 5–50 Hz). No obstante, en la [[Joint Inversion|inversión conjunta]] de $V_S$ y $D_s$ (inversión de la curva de atenuación de Rayleigh), las KK deben satisfacerse para garantizar la consistencia física del modelo viscoelástico.

## Modelos de atenuación que satisfacen las KK

| Modelo | $G(\omega)$ | Satisface KK | Dispersión de material |
|--------|------------|-------------|----------------------|
| Kelvin-Voigt | $G_0(1 + i\eta\omega)$ | Sí | Fuerte (crece con $\omega$) |
| Maxwell | $G_0 i\omega\tau/(1+i\omega\tau)$ | Sí | Fuerte |
| Zener (SLS) | $G_0(1+i\omega\tau_\epsilon)/(1+i\omega\tau_\sigma)$ | Sí | Moderada (pico a $\omega_{pico}$) |
| Constant-Q | $G_0(\omega/\omega_0)^{2D_s/\pi}$ | Sí | Logarítmica (suave) |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — KK en la inversión simultánea VS+DS
> Foti et al. (2018, §2.2 y §7.3) discuten las Relaciones de Kramers-Kronig en el contexto de la inversión simultánea de $V_S(z)$ y $D_s(z)$ a partir de la [[Dispersion Curve|curva de dispersión]] y la curva de atenuación de ondas de Rayleigh. El modelo viscoelástico adoptado (módulo complejo de Kelvin-Voigt generalizado) satisface las KK por construcción — esto garantiza que la curva de atenuación $\alpha_R(f)$ calculada a partir del $D_s$ del modelo sea consistente con la [[Material Dispersion|dispersión de material]] implícita. En el sitio de Pisa (arcilla de alta plasticidad, $D_s$ = 2–6%), la corrección por dispersión de material de las KK modifica la [[Phase Velocity|velocidad de fase]] calculada en ~0.3–0.8 m/s en el rango 5–30 Hz — un efecto de ~0.3% que es detectable pero inferior a la incertidumbre de picking de la [[Dispersion Curve|curva de dispersión]] (~1–2 m/s). Los autores concluyen que para $D_s < 5$%, la corrección KK es de segundo orden en la inversión de $V_S$, pero es de primer orden en la inversión de $D_s$.
>
> — Foti et al. (2018), §2.2, pp. 45–52; §7.3, pp. 375–380.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.2 — viscoelasticidad y relaciones KK |
| Aki & Richards (2002), *Quantitative Seismology* | §5.5 — relaciones KK en sismología |
| Kennett (1983), *Seismic Wave Propagation* | Cap. 4 — dispersión de material y KK |
