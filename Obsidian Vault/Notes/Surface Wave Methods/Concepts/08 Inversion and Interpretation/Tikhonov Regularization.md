# Tikhonov Regularization

La **regularización de Tikhonov** es la técnica matemática más sistemática y ampliamente usada para mitigar la **ill-posedness** de los problemas inversos en geofísica, incluyendo la inversión de curvas de dispersión de ondas superficiales.

---

## Intuición física

El problema fundamental de la inversión es que el sistema de ecuaciones G·m = d puede estar mal condicionado: pequeñas variaciones en los datos producen grandes variaciones en la solución. Esto ocurre porque el operador G tiene valores singulares muy pequeños, que amplifican el ruido al invertir.

La regularización de Tikhonov resuelve este problema añadiendo un término extra al problema de minimización que "penaliza" soluciones complicadas. En esencia, obliga al algoritmo a buscar no solo el mejor ajuste a los datos, sino también la solución más simple entre todas las que ajustan bien los datos. El parámetro μ controla qué tan importante es la simplicidad respecto al ajuste.

---

## Definición técnica

El problema de minimización regularizado de **orden cero** es (Tikhonov y Arsenin, 1977):

$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{m}\|_2^2 \right\}$$

donde:
- **Gm − d** es el error de predicción (diferencia entre datos teóricos y experimentales)
- **m** es la norma de la solución (mide su "complejidad" o amplitud)
- **μ** es el **parámetro de regularización** o multiplicador de Lagrange

El primer término busca el mejor ajuste; el segundo penaliza soluciones de gran norma. El parámetro μ controla el balance entre ambos objetivos.

---

## Formulación matemática

**Solución — mínimos cuadrados amortiguados (Ec. 6.16):**
$$\mathbf{m} = (\mathbf{G}^T\mathbf{G} + \mu^2 \mathbf{I})^{-1} \mathbf{G}^T \mathbf{d}$$

En términos de la descomposición SVD G = Q₁ΣQ₂ᵀ, la solución se puede escribir como:
$$\mathbf{m} = \sum_{i=1}^{k} \frac{s_i^2}{s_i^2 + \mu^2} \cdot \frac{[(\mathbf{Q}_1^T)_i \cdot \mathbf{d}]}{s_i} \cdot [(\mathbf{Q}_2)_i] \qquad (6.17)$$

Los factores $s_i^2/(s_i^2 + \mu^2)$ son los **factores de filtro**: para valores singulares grandes (sᵢ >> μ), el factor es ≈ 1 → esos componentes se preservan. Para valores singulares pequeños (sᵢ << μ), el factor → 0 → esos componentes se amortiguan (evitando la amplificación del ruido).

**Regularización de orden superior (Ec. 6.20):**
$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{L}^n \mathbf{m}\|_2^2 \right\}$$

donde **L** es la **matriz de rugosidad** (diferencias finitas centradas, Ec. 6.19):

$$\mathbf{L} = \begin{bmatrix} 0 & \cdots & & \\ -1 & 1 & 0 & \\ \cdots & -1 & 1 & \\ & 0 & -1 & 1 \end{bmatrix}$$

Los escalares de rugosidad son:
- **R₁ = ||Lm||²** (primer orden): mide la irregularidad del gradiente del perfil
- **R₂ = ||L(Lm)||²** (segundo orden): mide la curvatura del perfil

Los órdenes disponibles son:
| Orden (n) | Penaliza | Favorece |
|-----------|---------|---------|
| 0 | Amplitud de m | Soluciones de pequeña norma |
| 1 | Gradiente de m | Perfiles suaves (sin saltos bruscos) |
| 2 | Curvatura de m | Perfiles muy suaves, con variación casi lineal |

---

## Elección del parámetro μ

La elección de μ es crítica y no trivial:
- **μ = 0**: recupera el problema original sin regularización (inestable si hay valores singulares pequeños)
- **μ demasiado pequeño**: ajuste bueno pero solución inestable (oscilaciones espurias en el perfil)
- **μ demasiado grande**: solución muy suave y estable, pero con error de ajuste alto (exceso de suavizado)

El valor óptimo de μ se busca con métodos como:
- **Curva L (L-curve):** grafica ||Gm - d||² vs ||m||² para diferentes μ; el punto de mayor curvatura ("codo" de la L) es el compromiso óptimo.
- **Principio de discrepancia:** elige μ tal que el error de ajuste sea consistente con la incertidumbre conocida de los datos.
- **Validación cruzada generalizada (GCV)**.

---

## Conexión con el algoritmo de Occam

El **algoritmo de Occam** (Constable et al. 1987, Lai 2005) es la aplicación iterativa de la regularización de Tikhonov de primer y segundo orden al problema no lineal de inversión conjunta de las curvas de dispersión y atenuación de Rayleigh. En Occam, μ se ajusta automáticamente en cada iteración para que el error residual coincida con un valor objetivo $\tilde{Er}$ determinado por la incertidumbre de los datos.

---

## Implicación práctica para MASW

En la inversión MASW de curvas de dispersión:

- La regularización de **orden 1** (suavizar el gradiente) es la más apropiada para sitios con variación gradual de las propiedades del suelo con la profundidad (perfiles normalmente dispersivos).
- La regularización de **orden 2** produce perfiles aún más suaves, adecuados cuando se sabe a priori que el subsuelo es muy homogéneo.
- La regularización de **orden 0** puede usarse cuando se necesita controlar la amplitud absoluta del perfil (por ejemplo, si hay restricciones de Vs de boreholes).
- Para sitios con **capas rígidas superficiales o inversiones de velocidad**, la regularización de Tikhonov puede dificultar la recuperación de la discontinuidad. En esos casos, conviene usar **total variation regularization** (norma L₁ en lugar de L₂) o información a priori explícita sobre la interfaz.

---

*Trazabilidad: Sebastiano Foti, Surface Wave Methods, Cap. 6, §6.4.2.3, pp. 298–301; §6.4.3.4, pp. 312–320.*
*Referencias clave: Tikhonov y Arsenin (1977); Constable et al. (1987); Lai (2005).*
