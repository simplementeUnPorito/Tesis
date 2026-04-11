---
name: Correspondence Principle
description: Principio que extiende las soluciones elásticas a medios viscoelásticos reemplazando los módulos reales por módulos complejos — base teórica del cálculo de [[Dispersion Curve|curvas de dispersión]] en medios con amortiguamiento
type: reference
---

# Correspondence Principle — Principio de Correspondencia Viscoelástica

> [!CONCEPT] Definición
> El **Principio de Correspondencia** (o *Correspondence Principle*, Elastic-Viscoelastic Analogy) establece que las soluciones de los problemas de elasticidad lineal pueden extenderse a medios [[Viscoelastic Media|viscoelásticos]] lineales simplemente **reemplazando los módulos elásticos reales** (módulo de Young $E$, [[Shear Modulus|módulo de corte]] $G$, módulo de Lamé $\lambda$) por los correspondientes **módulos viscoelásticos complejos** $\hat{E}(\omega)$, $\hat{G}(\omega)$, $\hat{\lambda}(\omega)$, en el dominio de la frecuencia. Matemáticamente, si la solución elástica del campo de desplazamiento es $\mathbf{u}^{el}(\mathbf{x}, \omega; G, \lambda)$, entonces la solución viscoelástica es:
> $$\mathbf{u}^{ve}(\mathbf{x}, \omega) = \mathbf{u}^{el}(\mathbf{x}, \omega; \hat{G}(\omega), \hat{\lambda}(\omega))$$
> En el contexto de las ondas de Rayleigh, el Principio de Correspondencia permite usar directamente el [[Thomson-Haskell Matrix|método de matrices de Thomson-Haskell]] (derivado para medios elásticos) para calcular la **[[Dispersion Curve|curva de dispersión]] compleja** $\hat{c}_R(\omega) = c_R(\omega) + i \alpha_R(\omega)/k$ de un medio viscoelástico estratificado — donde la parte imaginaria da el [[Attenuation Coefficient|coeficiente de atenuación]] $\alpha_R(\omega)$ ligado al [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s$. Los módulos complejos satisfacen las [[Kramers-Kronig Relations|Relaciones de Kramers-Kronig]] por causalidad.
>
> — Foti et al. (2018), §2.2; Lai & Rix (1998); Aki & Richards (2002), §5.5.

## Formulación matemática

### Módulo de corte complejo

Para un modelo de Kelvin-Voigt generalizado (Maxwell fraccionado):

$$\hat{G}(\omega) = G_0 \left[1 + 2i D_s(\omega) \cdot \text{sgn}(\omega)\right] \approx G_0 (1 + 2i D_s)$$

para $D_s \ll 1$ (amortiguamiento pequeño, válido en suelos $D_s < 20\%$).

La velocidad de onda de corte compleja:

$$\hat{V}_S(\omega) = \sqrt{\frac{\hat{G}(\omega)}{\rho}} = V_S\sqrt{1 + 2iD_s} \approx V_S(1 + iD_s)$$

### [[Wavenumber|número de onda]] complejo

El [[Wavenumber|número de onda]] de Rayleigh complejo:

$$\hat{k}_R(\omega) = \frac{\omega}{\hat{c}_R(\omega)} = k_R(\omega) - i\alpha_R(\omega)$$

donde $\alpha_R$ es el coeficiente de [[Attenuation|atenuación]] espacial (Np/m). La relación con $D_s$:

$$\alpha_R(\omega) \approx \frac{\omega D_s^{eff}(\omega)}{c_R(\omega)}$$

donde $D_s^{eff}$ es el amortiguamiento efectivo de Rayleigh (promedio pesado de $D_s(z)$ por los kernels de sensibilidad).

## Aplicación al cálculo del espectro de dispersión de Rayleigh

El Principio de Correspondencia permite calcular la curva de [[Attenuation|atenuación]] de Rayleigh $\alpha_R(f)$ de un perfil viscoelástico estratificado:
1. Sustituir $G_j \to \hat{G}_j = G_j(1 + 2iD_{s,j})$ en cada capa $j$
2. Aplicar el método de matrices [[Thomson-Haskell Matrix]] con módulos complejos
3. Resolver la ecuación secular compleja → obtener $\hat{c}_R(\omega) = c_R + i\alpha_R c_R^2/\omega$

La inversión de la curva de [[Attenuation|atenuación]] experimental $\alpha_R^{obs}(f)$ produce el perfil $D_s(z)$.

> [!EXAMPLE] Evidencia empírica: Lai & Rix (1998) — Principio de Correspondencia en inversión simultánea VS+DS
> Lai & Rix (1998) aplican el Principio de Correspondencia al desarrollo de la teoría de inversión simultánea de $V_S$ y $D_s$ a partir de la [[Dispersion Curve|curva de dispersión]] y la curva de [[Attenuation|atenuación]] de ondas de Rayleigh. El algoritmo reemplaza los módulos elásticos reales por módulos de Kelvin-Voigt complejos $\hat{G} = G(1 + 2iD_s)$ en la formulación de matrices de capas, y resuelve la ecuación secular compleja. Validado en el sitio de Pisa (arcilla de alta plasticidad, $D_s$ = 2–6%), el perfil $D_s(z)$ obtenido por inversión concuerda con los ensayos de [[Resonant Column Test|columna resonante]] (RCT) dentro de ±1–1.5% en valor absoluto. El Principio de Correspondencia es el fundamento teórico de todas las implementaciones modernas de inversión de la curva de [[Attenuation|atenuación]] de Rayleigh en [[MASW Method|MASW]] para estimar el amortiguamiento in situ.
>
> — Lai & Rix (1998), *J. Geotech. Geoenviron. Eng.*; Foti et al. (2018), §2.2, pp. 45–55.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.2 — Principio de Correspondencia en [[MASW Method|MASW]] |
| Lai & Rix (1998), *J. Geotech. Geoenviron.* | Inversión simultánea VS+DS mediante Principio de Correspondencia |
| Aki & Richards (2002), *Quantitative Seismology* | §5.5 — viscoelasticidad y analogía elástica-viscoelástica |
