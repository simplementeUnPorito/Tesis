---
name: Shear Modulus
description: Módulo de rigidez de corte G del suelo — parámetro elástico fundamental medido por VS mediante G = ρVS² — alcanza su valor máximo Gmax a deformaciones de corte sísmicas γ < 10⁻⁵
type: reference
---

# Shear Modulus — Módulo de Corte $G$

> [!CONCEPT] Definición
> El **módulo de corte** $G$ (también llamado módulo de rigidez o *shear modulus*) es la constante elástica que relaciona el esfuerzo de corte $\tau$ con la deformación angular de corte $\gamma$ en un sólido isótropo:
> $$G = \frac{\tau}{\gamma}$$
> En un medio elástico lineal isótropo, $G$ coincide con la segunda constante de Lamé: $G = \mu$. La velocidad de onda de corte $V_S$ depende exclusivamente de $G$ y de la densidad $\rho$:
> $$V_S = \sqrt{\frac{G}{\rho}} \quad \Longrightarrow \quad G = \rho \, V_S^2$$
> Esta relación es la **base física de todos los métodos sísmicos de caracterización geotécnica**: medir $V_S$ en campo equivale directamente a medir $G$. A niveles de deformación sísmicos ($\gamma < 10^{-5}$, Burland 1989; Atkinson 2000), el suelo se comporta de forma esencialmente lineal y $G$ alcanza su valor máximo $G_{\max}$, la rigidez de referencia del suelo en estado de reposo. El módulo $G_{\max}$ es **independiente de la saturación** (Biot 1956): la presión del fluido intersticial no afecta la rigidez de corte del esqueleto sólido, razón por la que $V_S$ es preferido sobre $V_P$ en la caracterización sísmica de sitio (véase [[Porous Media]]).
>
> — Foti et al. (2018), §1.1, pp. 2–3; Biot (1956); Burland (1989).

## Relación con otras constantes elásticas

En un sólido isótropo, $G$ está relacionado con las demás constantes elásticas (Foti Ec. 1.1):

| Relación | Expresión |
|----------|-----------|
| $V_P$ en términos de $G$ | $V_P = \sqrt{(\lambda + 2G)/\rho}$ |
| Módulo de Young | $E = 2G(1+\nu)$ |
| Coeficiente de Poisson | $\nu = (\lambda/2)/(\lambda/2 + G) = (V_P^2 - 2V_S^2)/[2(V_P^2 - V_S^2)]$ |
| [[Lamé Constants|Constante de Lamé]] $\lambda$ | $\lambda = \rho V_P^2 - 2G$ |

El módulo de compresibilidad volumétrica $K = \lambda + 2G/3$ sí depende de la saturación — mientras que $G$ permanece invariante. Por tanto, en suelos saturados $V_P \to 1500$ m/s (dominado por $K_f$) pero $V_S$ refleja únicamente $G$ del esqueleto (véase [[Porous Media]]).

## Comportamiento no lineal y Gmax en geotecnia

Los suelos son materiales no lineales: $G$ disminuye al aumentar $\gamma$ (curva $G/G_{\max}$ vs. $\gamma$). Los métodos sísmicos operan en el rango de **muy pequeñas deformaciones** donde:

$$G_{\max} = \rho \, V_{S,\text{campo}}^2$$

Este $G_{\max}$ es la rigidez inicial (tangente en el origen) utilizada como:
- **Referencia de normalización** en curvas $G/G_{\max}$ para análisis de respuesta sísmica no lineal
- **Parámetro de entrada** en cálculos de asentamientos elásticos y vibraciones de máquinas
- **Indicador de densidad relativa** en suelos granulares (via correlaciones con $q_c$ del CPT)

La conversión $G_{\max} = \rho V_S^2$ requiere conocer la densidad $\rho$ del suelo — típicamente estimada a partir de correlaciones con $q_c$ (Robertson & Cabal 2015) o ensayos de laboratorio.

## Viscoelasticidad y módulo complejo

En realidad, los suelos disipan energía incluso a $\gamma < 10^{-5}$ (histéresis). El modelo viscoelástico lineal extiende el módulo real:

$$G^* = G(1 + 2i D_S)$$

donde $D_S$ es el [[Shear Damping Ratio|material damping ratio]] de corte ($D_S \approx 0.01$–$0.05$ en suelos). El módulo complejo $G^*$ genera un número de onda complejo $k^* = \omega/V_S + i\alpha_S$, donde $\alpha_S$ es el [[Attenuation Coefficient|coeficiente de atenuación]] (ver [[Correspondence Principle]]).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Gmax en el sitio La Salle
> Foti et al. (2018, §7.2.1) presentan el perfil $G_{\max}(z) = \rho(z) \cdot V_S(z)^2$ derivado de la inversión MASW del sitio La Salle, Francia. Con $V_S$ entre 200 y 450 m/s y densidades típicas de suelos blandos ($\rho \approx 1800$–2000 kg/m³), se obtiene $G_{\max}$ entre ~70 MPa (0–5 m) y ~400 MPa (15–25 m). El perfil es consistente con ensayos de laboratorio de [[Resonant Column Test]] (diferencias < 15%) confirmando que el campo sísmico refleja el estado de muy pequeña deformación del suelo en condiciones in situ. La concordancia valida el uso de $G = \rho V_S^2$ directamente en diseño geotécnico sin necesidad de factores de corrección por tamaño de muestra o confinamiento de laboratorio.
>
> — Foti et al. (2018), §7.2.1, pp. 354–362; Robertson & Cabal (2015), *CPT Guide*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1, pp. 2–3 — base física de métodos sísmicos |
| Biot, M.A. (1956), *J. Acoust. Soc. Am.* | Independencia de G respecto a saturación |
| Burland, J.B. (1989), *Géotechnique* | Límite de deformación pequeña γ < 10⁻⁵ |
| Robertson & Cabal (2015), *CPT Guide* | Correlaciones Gmax con qc |
