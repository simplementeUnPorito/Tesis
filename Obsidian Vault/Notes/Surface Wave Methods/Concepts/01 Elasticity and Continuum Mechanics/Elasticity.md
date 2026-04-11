# Elasticity

> [!CONCEPT] Definición
> La **elasticidad** es la rama de la mecánica del continuo que estudia la deformación reversible de materiales bajo la acción de fuerzas. En un medio elástico ideal, la deformación desaparece completamente al retirar la carga — no hay disipación de energía. Las ecuaciones de Navier, derivadas de la ley de Hooke generalizada y la conservación de momento, gobiernan la propagación de [[Body Waves]] y [[Surface Waves]] y son la base teórica de todos los métodos sísmicos.
>
> — Foti et al. (2018), §2.1.1, pp. 38–41; Achenbach (1984), *Wave Propagation in Elastic Solids*.

---

## 1. Concepto

La **elasticidad** es la rama de la mecánica del continuo que estudia cómo los materiales se deforman bajo la acción de fuerzas y cómo recuperan su forma original cuando dichas fuerzas desaparecen.

En un medio elástico ideal:

- la deformación es **reversible**
- no existe disipación permanente de energía
- el material vuelve a su estado inicial al retirar la carga

---

## 2. Variables fundamentales

La teoría de la elasticidad describe el comportamiento del medio mediante tres campos principales:

**1. Campo de desplazamiento**

$$
u(x,t)
$$

describe el desplazamiento de cada punto material del medio.

Relacionado con:

- [[Linear Waves]]

---

**2. Tensor de deformación**

Describe cómo cambian las distancias internas del material.

Ver:

- [[Strain Tensor]]

---

**3. Tensor de esfuerzos**

Describe las fuerzas internas que aparecen dentro del material cuando se deforma.

Ver:

- [[Stress Tensor]]

---

## 3. Ecuación de movimiento

Aplicando conservación de momento lineal a un medio continuo se obtiene:

$$
\nabla \cdot \sigma =
\rho
\frac{\partial^2 u}{\partial t^2}
$$

donde:

- $\sigma$ → [[Stress Tensor]]
- $\rho$ → densidad
- $u$ → campo de desplazamiento

Esta ecuación es el equivalente continuo de la **segunda ley de Newton**.

---

## 4. Relación constitutiva

Para cerrar el sistema de ecuaciones es necesario relacionar esfuerzo y deformación.

En un material **elástico lineal isotrópico** se utiliza la ley de Hooke generalizada:

$$
\sigma =
\lambda \, tr(\varepsilon) I
+
2\mu \varepsilon
$$

donde:

- $\lambda , \mu$ → **constantes de Lamé**
- $I$ → tensor identidad
- $\varepsilon$ → [[Strain Tensor]]

Interpretación física:

- $tr(\varepsilon)$ → deformación **volumétrica**
- $\varepsilon$ → deformación **distorsional**

---

## 5. Ecuaciones de Navier

Sustituyendo la ley de Hooke en la ecuación de movimiento se obtienen las **ecuaciones de Navier**:

$$
\mu \nabla^2 u +
(\lambda + \mu)\nabla(\nabla \cdot u)
=
\rho
\frac{\partial^2 u}{\partial t^2}
$$

Estas ecuaciones gobiernan la propagación de perturbaciones en un medio elástico.

Son un sistema de:

- [[Hyperbolic Partial Differential Equations]]

---

## 6. Ondas en medios elásticos

Las ecuaciones de Navier admiten soluciones ondulatorias.

Estas soluciones corresponden a:

- [[P-waves]] → ondas compresionales
- [[S-Waves]] → ondas de corte

Estas ondas constituyen las **[[Body Waves]]**.

En presencia de superficies libres o interfaces también aparecen:

- [[Surface Waves]]

---

## 7. Hipótesis comunes en geofísica

Muchos modelos sísmicos asumen:

- medio **elástico lineal**
- **isotropía**
- **deformaciones pequeñas**
- propiedades constantes en cada capa

Estas simplificaciones permiten modelar la propagación de ondas en:

- [[Layered Media]]
- [[Vertically Inhomogeneous Media]]

---

## 8. Importancia en geofísica

La teoría de la elasticidad proporciona la base física para:

- propagación de ondas sísmicas
- interpretación de datos de geófonos
- estimación de propiedades del subsuelo

En particular, las velocidades de:

- [[P-waves]]
- [[S-Waves]]

dependen directamente de las constantes elásticas del material.

---

## Conceptos relacionados

- [[Strain Tensor]]
- [[Stress Tensor]]
- [[Linear Waves]]
- [[Body Waves]]
- [[Surface Waves]]
- [[Rayleigh Waves]]
- [[Elastic Half Space]]
- [[Layered Media]]
- [[Hyperbolic Partial Differential Equations]]

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — elasticidad lineal como base del problema directo MASW
> **Paper 002 (Xia, Miller & Park 1999)** implementa el problema directo de propagación de Rayleigh Waves sobre la base de las ecuaciones de Navier en cada capa elástica lineal isotrópica. El Jacobiano analítico $\partial V_R / \partial V_S$ (núcleo del algoritmo de inversión) se deriva directamente de la teoría de elasticidad lineal, lo que hace posible la inversión en < 10 iteraciones con convergencia garantizada. La validez de la aproximación elástica lineal queda confirmada por el acuerdo con borehole en múltiples sitios.
>
> — Research Database, entrada 002 (core).

## Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–41 |
| Achenbach, J.D. (1984), *Wave Propagation in Elastic Solids*, North-Holland | Cap. 1–3 |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 |