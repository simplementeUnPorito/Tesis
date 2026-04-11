---
name: Poisson Ratio
description: Parámetro elástico que relaciona deformación transversal y axial; controla la razón VP/VS y el comportamiento de ondas en suelos saturados
type: reference
---

# Razón de Poisson (Coeficiente de Poisson)

> [!CONCEPT] Definición
> La **razón de Poisson** $\nu$ relaciona la contracción lateral con la elongación axial de un material bajo carga uniaxial. En el contexto de ondas superficiales, controla la razón $V_P/V_S = \sqrt{2(1-\nu)/(1-2\nu)}$ y la velocidad de [[Rayleigh Waves|Rayleigh]] $c_R \approx f(\nu)\cdot V_S$. Es necesario como **parámetro a priori** en la inversión MASW: un $\nu$ incorrecto — especialmente al ignorar el nivel freático que cambia $\nu$ de ~0.3 a ~0.5 en suelos saturados — introduce errores sistemáticos en el perfil $V_S$ invertido.
>
> — Foti et al. (2018), §2.1.3, pp. 43–45; §7.1.3, pp. 361–363.

## Definición

La razón de Poisson ν se define como el cociente entre la deformación transversal (contracción lateral) y la deformación longitudinal (elongación axial) bajo carga uniaxial:

$$\nu = -\frac{\varepsilon_{\text{transversal}}}{\varepsilon_{\text{axial}}}$$

Para materiales isótropos y elásticos lineales, el rango físicamente admisible es:

$$-1 \leq \nu < 0.5$$

En la práctica, casi todos los materiales naturales tienen $0 \leq \nu < 0.5$.

## Relación con velocidades de ondas de cuerpo

Las velocidades de ondas P y S en un medio isótropo elástico son:

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}, \qquad V_S = \sqrt{\frac{\mu}{\rho}}$$

El cociente $V_P/V_S$ depende exclusivamente de $\nu$:

$$\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

| $\nu$ | $V_P/V_S$ |
|-------|-----------|
| 0.0 | 1.41 |
| 0.25 | 1.73 |
| 0.33 | 2.00 |
| 0.40 | 2.45 |
| 0.49 | 7.00 |
| 0.50 | ∞ |

Para $\nu = 0.25$ (valor clásico de muchas rocas) se obtiene $V_P/V_S = \sqrt{3} \approx 1.73$.

## Relación con la velocidad de Rayleigh

La velocidad de fase de las [[Rayleigh Waves]] en un [[Elastic Half Space]] homogéneo depende únicamente de $V_S$ y de $\nu$:

$$c_R \approx f(\nu) \cdot V_S$$

El factor $f(\nu)$ varía entre 0.862 (para $\nu = 0$) y 0.955 (para $\nu \to 0.5$). Para $\nu = 0.25$, $c_R \approx 0.919\,V_S$. Esta dependencia implica que, para convertir la velocidad de Rayleigh medida experimentalmente en $V_S$, es necesario conocer o asumir $\nu$.

## Comportamiento en geomateriales

### Suelos secos / no saturados

En suelos sin saturar, la respuesta volumétrica está dominada por el esqueleto sólido:

$$\nu_{\text{seco}} \approx 0.1\text{–}0.35$$

### Suelos saturados (comportamiento no drenado)

En suelos saturados bajo carga rápida (drenaje impedido), la compresibilidad del fluido poral domina la respuesta volumétrica. La compresibilidad del agua es muy baja ($K_{\text{agua}} \approx 2.2\,\text{GPa}$), por lo que la deformación volumétrica del suelo se vuelve casi nula:

$$\nu_{\text{saturado, no drenado}} \approx 0.45\text{–}0.50$$

Como consecuencia, $V_P$ aumenta drásticamente (llega a ~1500 m/s = velocidad del agua), mientras que $V_S$ no cambia. Este efecto hace que $V_P$ **no sea un buen indicador de la rigidez del esqueleto** en suelos saturados — razón fundamental por la que los métodos de ondas superficiales (sensibles a $V_S$) son preferibles para caracterización geotécnica.

## Implicación práctica en la inversión de ondas superficiales

La curva de dispersión de Rayleigh es **poco sensible** a $\nu$ (o equivalentemente a $V_P$), pero no completamente insensible. En la inversión, $\nu$ debe ser proporcionado como **parámetro a priori** (o como parámetro fijo).

Un error en $\nu$ — especialmente el no reconocer la presencia de un nivel freático que cambia $\nu$ de ~0.3 a ~0.5 — puede introducir errores sistemáticos en el perfil $V_S$ obtenido. Foti (Cap. 7.1.3) demuestra que ignorar el nivel freático a 3 m de profundidad produce un perfil $V_S$ fuertemente erróneo (Fig. 7.9). La sinergia con métodos de refracción P (que detectan el salto de $V_P$ en la tabla de agua) es esencial para usar $\nu$ correcto en la inversión.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — impacto crítico del nivel freático sobre ν en inversión MASW
> Foti et al. (2018, §7.1.3, Fig. 7.9) demuestran cuantitativamente que **ignorar un nivel freático a 3 m de profundidad** — que eleva $\nu$ de ~0.3 a ~0.5 en la zona saturada — produce un perfil $V_S(z)$ con errores sistemáticos que superan el 20% en las capas afectadas. La razón es que el aumento de $V_P$ por saturación (de ~300 m/s a ~1500 m/s) cambia la relación $c_R/V_S$ para las frecuencias que sondean esa profundidad, sesgando la inversión. La sinergia con un perfil de refracción P (que detecta el salto de $V_P$ en la tabla de agua) elimina este sesgo — recomendación activa en todos los estudios de sitio en zonas con nivel freático somero.
>
> — Foti et al. (2018), §7.1.3, pp. 361–363, Fig. 7.9.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.3, pp. 43–45 — derivación de $V_P/V_S$ en términos de $\nu$ |
| Foti et al. (2018), *Surface Wave Methods* | §7.1.3, pp. 361–363 — impacto del nivel freático sobre $\nu$ e inversión |
