---
name: Regularization
description: Estrategias matemáticas para estabilizar la inversión de problemas mal condicionados en métodos de ondas superficiales, controlando el balance entre ajuste de datos y suavidad del modelo
type: reference
---

# Regularization — Estabilización de Inversiones Mal Condicionadas

> [!CONCEPT]
> La **regularización** es el conjunto de técnicas que permiten obtener soluciones estables y geológicamente realistas en inversiones sísmicas cuando el problema es [[Ill-Posed Problem|mal condicionado]]. El principio fundamental es añadir información *a priori* sobre el modelo m para seleccionar, entre infinitas soluciones compatibles con los datos, aquella que minimiza un funcional penalizado:
>
> $$\Phi(\mathbf{m}) = \|\mathbf{J}\mathbf{m} - \mathbf{d}\|^2 + \lambda^2\|\mathbf{L}\mathbf{m}\|^2$$
>
> donde λ es el parámetro de regularización y **L** codifica el tipo de suavidad impuesta.

## Tipos principales de regularización en [[MASW Method|MASW]]/SWM

### 1. Tikhonov (orden 0 y 1)
Ver [[Tikhonov Regularization]]. La forma más extendida en inversión 1D:
- **Orden 0**: L = I → minimiza la norma del modelo (solución de mínima energía)
- **Orden 1**: L = D₁ (diferencias finitas) → minimiza la variación (perfil suave)
- **Orden 2**: L = D₂ → minimiza la curvatura (perfil más suave todavía)

### 2. Variación Total (TV)
Ver [[Total Variation Regularization]]. L = D₁ con norma L1 en lugar de L2:
$$\|\mathbf{L}\mathbf{m}\|_1 = \sum_i |m_{i+1} - m_i|$$
Produce perfiles **escalonados** (interfaces abruptas), ideal cuando se esperan discontinuidades geológicas.

### 3. Occam / Suavizado mínimo
Ver [[Occam Algorithm]]. Minimiza la rugosidad del modelo para un ajuste de datos dado (el modelo más suave que explica los datos dentro de la tolerancia de error).

## Selección del parámetro λ

| Método | Principio | Ventaja |
|--------|-----------|---------|
| [[L-Curve Criterion]] | Esquina de log\|\|r\|\| vs log\|\|Lm\|\| | Robusto sin conocer nivel de ruido |
| Chi-cuadrado (χ²) | λ tal que \|\|Jm−d\|\|²/N = σ² | Requiere estimación de σ |
| GCV | Validación cruzada generalizada | Automático, costo computacional alto |
| Factor de Ruido | Criterio de Herrmann (2013) | Popular en SurfSeis y Geopsy |

## Relación con [[Singular Value Decomposition|SVD]] y [[Condition Number|número de condición]]

La regularización Tikhonov actúa como filtro sobre los valores singulares de **J**:

$$f_i = \frac{\sigma_i^2}{\sigma_i^2 + \lambda^2}$$

Los valores singulares pequeños (responsables de la inestabilidad) son amortiguados. El [[Condition Number|número de condición]] efectivo se reduce de κ = σ_max/σ_min a κ_reg ~ σ_max/λ. En [[MASW Method]], κ típicamente 10³–10⁵ sin regularización; con λ óptimo se reduce a 10–100 (Xia et al. 1999).

## Comparación de métodos por tipo de perfil esperado

| Perfil Vs esperado | Regularización recomendada |
|-------------------|---------------------------|
| Gradual (suelo blando) | Tikhonov L2 (curvatura mínima) |
| Capas con interfaces | Tikhonov L1 u Occam |
| Discontinuidades abruptas | [[Total Variation Regularization|Variación Total]] |
| Incertidumbre alta | [[Monte Carlo Methods]] + cualquier regularización |
| [[Joint Inversion|inversión conjunta]] | [[Cross-Gradient Function]] como regularización estructural |

> [!EXAMPLE] Evidencia empírica (Foti et al. 2018, Xia et al. 1999)
> - **Xia et al. (1999, GRL)**: inversión [[MASW Method|MASW]] de 19 capas en Lawrence, Kansas — con regularización Tikhonov L1 y λ seleccionado por factor de ruido, el perfil Vs convergió en 3–5 iteraciones con error < 15% respecto a downhole. Sin regularización, la solución divergía tras la primera iteración (κ > 10⁴).
> - **Foti et al. (2018, §6.4)**: en el sitio La Salle (suelo blando), la TV regularization identificó una interfaz arena/arcilla a 4.2 m que el suavizado Tikhonov difuminaba a una zona de transición de 2 m.
> - **Maraschini & Foti (2010)**: en inversión por determinante Haskell-Thomson con búsqueda global ([[Monte Carlo Methods|Monte Carlo]]), la regularización implícita del espacio de modelos inicial es suficiente — no requiere penalización explícita si el espacio de búsqueda está bien acotado.

> [!EXAMPLE] Evidencia empírica: Cox & Teague (2016) — Layering Ratios para parametrización sin a priori
> **Paper 051 (Cox & Teague 2016, GJI 207(1):422–438, 115 citas)** aborda el problema de cómo definir el número de capas y sus espesores en la inversión de ondas superficiales cuando no se dispone de información a priori (borehole, geología detallada). Los autores proponen los **"layering ratios"** (LRs): relaciones sistemáticas entre los espesores de capas sucesivas ($h_{i+1}/h_i = $ constante) que guían la parametrización del modelo de forma reproducible y sin subjetividad del analista. Validado con datos sintéticos y reales ([[MASW Method|MASW]]/[[SASW Method|SASW]]), los LRs reducen la dependencia de la solución respecto a decisiones de parametrización ad hoc. La técnica conecta directamente con la [[Non-uniqueness|no-unicidad]]: al fijar sistemáticamente la estructura del modelo, la familia de soluciones aceptables refleja verdaderamente la ambigüedad de los datos y no artefactos de parametrización. Es especialmente útil para estudios de "análisis ciego" donde el operador no tiene acceso a datos de referencia.
>
> — Research Database, entrada 051 (core); Cox & Teague (2016), *Geophys. J. Int.* 207(1):422–438.

## Referencias

| Autor | Año | Contribución |
|-------|-----|--------------|
| Tikhonov & Arsenin | 1977 | Formulación clásica de regularización por norma |
| Xia, Miller & Park | 1999 | Aplicación a inversión [[MASW Method|MASW]] con Tikhonov L1 |
| Constable et al. | 1987 | Occam: suavizado mínimo en inversión 1D |
| Rudin et al. | 1992 | Variación Total (TV) en procesamiento de imagen/señal |
| Foti et al. | 2018 | §6.3–6.5: comparación de esquemas de regularización en SWM |
| Cox & Teague (2016), *GJI* 207(1):422–438 | Paper 051 — Layering Ratios para parametrización sin a priori; 115 citas |
