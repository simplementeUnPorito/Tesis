# Elasticity

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