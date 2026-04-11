---
name: Arias Intensity
description: Medida de la intensidad sísmica total de un acelerograma I_A = (π/2g)·∫a²(t)dt — parámetro de movimiento fuerte relacionado con el potencial de daño sísmico y correlacionado con VS30 del sitio para evaluar amplificación local
type: reference
---

# Arias Intensity — Intensidad de Arias $I_A$

> [!CONCEPT] Definición
> La **intensidad de Arias** $I_A$ es una medida escalar de la **energía total** de un acelerograma sísmico $a(t)$, proporcional a la integral de su cuadrado:
> $$I_A = \frac{\pi}{2g} \int_0^{t_d} a^2(t) \, dt \qquad [\text{m/s}]$$
> donde $g$ es la aceleración gravitacional y $t_d$ es la duración del movimiento. Fue propuesta por Arias (1970) como parámetro de movimiento fuerte que captura simultáneamente la amplitud y la duración del sismo. Tiene unidades de m/s y puede interpretarse físicamente como la energía total que disipa un oscilador de un grado de libertad con amortiguamiento crítico durante el sismo. En el contexto de los métodos de ondas superficiales, $I_A$ es relevante porque:
> (1) La **amplificación sísmica local** que produce el suelo blando (caracterizado por $V_{S,30}$ bajo) multiplica $I_A$ en factores de 4–20× respecto a la roca de referencia; (2) Correlaciones empíricas permiten estimar $I_A$ esperada en función de $V_{S,30}$, magnitud y distancia — base de las funciones de atenuación (GMPEs); (3) El umbral de $I_A > 0.3$ m/s es la condición crítica para inicio de [[Soil Liquefaction|licuefacción]] en suelos susceptibles (Kayen & Mitchell 1997).
>
> — Foti et al. (2018), §7.4.2, pp. 383–386; Arias (1970), *Seismic Design for Nuclear Power Plants*; Kayen & Mitchell (1997), *JGGE*.

## Relación entre VS30 e intensidad de Arias

Las funciones de predicción del movimiento fuerte (GMPEs) incluyen $V_{S,30}$ como factor de amplificación de sitio. Para suelos blandos:

| Clase | $V_{S,30}$ (m/s) | Factor $I_A$ vs. roca |
|-------|-----------------|----------------------|
| A (roca dura) | > 1500 | 1.0 (referencia) |
| B (roca) | 760–1500 | 1.0–1.5 |
| C (suelo denso) | 360–760 | 1.5–3.0 |
| D (suelo rígido) | 180–360 | 3.0–6.0 |
| E (suelo blando) | < 180 | 6.0–20.0 |

La amplificación no lineal (para $I_A > 0.1$ m/s) reduce el factor de amplificación porque el suelo blando entra en régimen no lineal con reducción efectiva de $V_S$ — razón por la que las GMPEs incluyen términos de saturación no lineal.

## Aplicación: umbral de licuefacción

Kayen & Mitchell (1997) establecen la condición de licuefacción en términos de $I_A$ y $V_{S1}$:
$$\text{FS}_{liq} = \frac{f(V_{S1})}{I_A^{0.5} \cdot \text{factor de sitio}}$$

Para $V_{S1} < 100$ m/s, la licuefacción es posible con $I_A > 0.3$ m/s — más conservador que el criterio CSR/CRR clásico (Andrus & Stokoe 2000).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — amplificación de IA en Memphis por VS30 del sitio
> Foti et al. (2018, §7.4.2, pp. 383–386) calculan la intensidad de Arias esperada en Memphis para el sismo de diseño del New Madrid Seismic Zone ($M_w = 7.5$, R = 50 km) usando la GMPE de Travasarou et al. (2003). En roca (clase B, $V_{S,30} = 800$ m/s), $I_A^{med} = 0.12$ m/s. En suelos de Mud Island (clase E, $V_{S,30} = 150$ m/s — determinado por [[MASW Method|MASW]]), $I_A^{med} = 1.8$ m/s — amplificación de 15×. Con $I_A > 0.3$ m/s, todos los depósitos deltaicos de arena suelta (identificados en el perfil [[MASW Method|MASW]] a 5–12 m) satisfacen la condición de susceptibilidad a la licuefacción según Kayen & Mitchell. Este resultado muestra cómo el perfil $V_S$ de [[MASW Method|MASW]] se convierte directamente en un mapa de riesgo de licuefacción.
>
> — Foti et al. (2018), §7.4.2, pp. 383–386; Kayen & Mitchell (1997), *JGGE* 123(12), 1162–1174.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.4.2 — intensidad de Arias y VS30 en microzonificación |
| Arias, A. (1970), *Seismic Design for Nuclear Power Plants* | Definición original de la intensidad de Arias |
| Kayen & Mitchell (1997), *JGGE* 123(12) | Umbral de licuefacción en términos de IA |
| Travasarou et al. (2003), *Earthquake Engineering & Structural Dynamics* | GMPE para intensidad de Arias con factores de sitio |
