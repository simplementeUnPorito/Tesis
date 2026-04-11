---
name: Sensitivity Kernel
description: Función que cuantifica la sensibilidad de la [[Phase Velocity|velocidad de fase]] de Rayleigh a cambios de VS, VP o densidad en cada profundidad — determina la resolución vertical de [[MASW Method|MASW]]
type: reference
---

# Sensitivity Kernel — Kernel de Sensibilidad

> [!CONCEPT] Definición
> El **sensitivity kernel** (o *kernel de sensibilidad*) $K_{c,m}(z, f)$ cuantifica cómo cambia la [[Phase Velocity|velocidad de fase]] $c_R(f)$ al perturbarse el parámetro del modelo $m$ (tipicamente $V_S$, $V_P$ o $\rho$) en la profundidad $z$: $\delta c_R(f) = \int_0^\infty K_{c,V_S}(z, f)\, \delta V_S(z)\, dz$. Es la función de sensibilidad del problema directo y determina la **resolución vertical** de la [[Inversión|inversión]]: la profundidad $z^*$ donde $|K_{c,V_S}(z^*, f)|$ es máximo define a qué profundidad contribuye principalmente la frecuencia $f$ de la [[Dispersion Curve|curva de dispersión]]. Los kernels de Rayleigh muestran máxima sensibilidad a $V_S$ en el rango $z \approx \lambda/3$–$\lambda/2$ ([[Skin Depth]]), con contribución despreciable de $V_P$ (<10%) y prácticamente nula de $\rho$ (<2%). La forma del kernel justifica la regla de profundidad $z_{max} \approx \lambda_{max}/2$ usada en el diseño de arreglos [[MASW Method|MASW]].
>
> — Foti et al. (2018), Cap. 6, §6.2; Xia et al. (1999), Paper 002.

## Definición matemática

Para la [[Phase Velocity|velocidad de fase]] del modo $n$ de Rayleigh a frecuencia $f$:

$$\delta c_R^{(n)}(f) = \int_0^\infty \left[ K_{V_S}^{(n)}(z,f)\, \delta V_S(z) + K_{V_P}^{(n)}(z,f)\, \delta V_P(z) + K_\rho^{(n)}(z,f)\, \delta \rho(z) \right] dz$$

Los kernels se calculan a partir de las **eigenfunciones** del [[Rayleigh Eigenproblem|Rayleigh Eigenproblem]]:

$$K_{V_S}^{(n)}(z,f) = \frac{\partial c_R^{(n)}}{\partial V_S(z)} = \frac{2\rho(z) V_S(z)}{c_R \cdot I_n} \left[ r_2^2(z) - \left(k r_1(z)\right)^2 \right]$$

donde $r_1, r_2$ son las eigenfunciones de desplazamiento horizontal y vertical, e $I_n$ es una integral de normalización.

## Propiedades de los kernels de Rayleigh

| Parámetro | Kernel $K$ típico | Implicación |
|---|---|---|
| $V_S$ | Máximo a $z \approx \lambda/3$–$\lambda/2$; decae a 0 para $z \gg \lambda$ | La inversión de $V_S$ es robusta |
| $V_P$ | Positivo pero pequeño (<10% de $K_{V_S}$) en la zona saturada | Puede fijarse a priori |
| $\rho$ | Muy pequeño (<2%) | Generalmente fijo en la inversión |

El kernel $K_{V_S}$ tiene un máximo claro a $z \approx \lambda/3$–$\lambda/2$, lo que justifica la regla de profundidad práctica: la frecuencia $f$ con longitud de onda $\lambda = c_R/f$ "mide" principalmente la zona a profundidad $\lambda/3$–$\lambda/2$.

## Uso en la inversión

El kernel de sensibilidad es la base del **Jacobiano** en los métodos de inversión local (mínimos cuadrados):

$$\mathbf{J}_{ij} = K_{V_S}^{(n_i)}(z_j, f_i) \cdot \Delta z_j$$

donde el subíndice $i$ corresponde al dato $(f_i, c_R^{obs}(f_i))$ y $j$ a la capa $j$ del modelo. El Jacobiano mapea perturbaciones de $V_S$ en capas a perturbaciones de la [[Dispersion Curve|curva de dispersión]].

## Resolución vertical

La resolución vertical del [[MASW Method|MASW]] no es uniforme con la profundidad:
- **Capas superficiales** ($z < 5$ m): cubiertas por las altas frecuencias (30–100 Hz); kernels estrechos → buena resolución
- **Capas intermedias** ($z \approx 10$–30 m): cubiertas por 5–30 Hz; resolución media
- **Capas profundas** ($z > 30$ m): cubiertas por <5 Hz; kernels anchos → baja resolución

Esta degradación de la resolución con la profundidad es intrínseca y no depende del algoritmo de inversión.

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — kernels de sensibilidad como base del análisis [[MASW Method|MASW]]
> **Paper 002 (Xia et al. 1999)** calcula los kernels de sensibilidad $\partial c_R / \partial V_S$, $\partial c_R / \partial V_P$ y $\partial c_R / \partial \rho$ para perfiles de suelo típicos de Kansas y demuestra cuantitativamente que: (1) $V_S$ domina la sensibilidad (80–95% de la variación de $c_R$); (2) $V_P$ contribuye <10% solo en la zona saturada (por debajo de la tabla de agua donde $V_P \approx 1500$ m/s); (3) $\rho$ es prácticamente insensible. Esta jerarquía de sensibilidad justifica la práctica estándar de fijar $V_P$ y $\rho$ a valores a priori e invertir únicamente $V_S$. Los kernels son también la base del Jacobiano usado en la inversión por mínimos cuadrados del paper.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3), pp. 691–700.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6, §6.2, pp. 282–290 — kernels de sensibilidad |
| Xia et al. (1999), *Geophysics* 64(3) | Paper 002 — análisis de sensibilidad VS/VP/ρ |
