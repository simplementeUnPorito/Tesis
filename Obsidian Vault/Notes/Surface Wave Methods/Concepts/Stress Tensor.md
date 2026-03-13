# Stress Tensor

## 1. Concepto

El **tensor de esfuerzos** describe las fuerzas internas que actúan dentro de un medio continuo.

Cada componente del tensor representa una **fuerza por unidad de área** que actúa sobre un plano interno del material.

---

## 2. Interpretación física

En un medio continuo, si se corta un volumen diferencial aparece una **tracción** sobre cada cara.

Esta tracción depende de la orientación del plano.

El tensor de Cauchy:

$$
\sigma
$$

describe completamente estas fuerzas internas.

Para un medio tridimensional:

$$
\sigma =
\begin{bmatrix}
\sigma_{11} & \sigma_{12} & \sigma_{13}\\
\sigma_{21} & \sigma_{22} & \sigma_{23}\\
\sigma_{31} & \sigma_{32} & \sigma_{33}
\end{bmatrix}
$$

donde:

- elementos diagonales → **esfuerzos normales**
- elementos fuera de la diagonal → **esfuerzos de corte**

---

## 3. Tracción sobre un plano

La tracción sobre un plano con normal $n$ está dada por:

$$
t = \sigma n
$$

Este resultado es conocido como **teorema de Cauchy**.

---

## 4. Fuerza interna en un volumen

La fuerza neta sobre un volumen diferencial se obtiene mediante la divergencia del tensor:

$$
\nabla \cdot \sigma
$$

Este término representa **fuerza por unidad de volumen**.

---

## 5. Aplicación a ondas elásticas

El tensor de esfuerzos aparece en las ecuaciones de movimiento del medio:

$$
\nabla \cdot \sigma =
\rho \frac{\partial^2 u}{\partial t^2}
$$

que es la base de la derivación de las [[Body Waves]].

---

## Conceptos relacionados

- [[Strain Tensor]]
- [[Body Waves]]
- [[Linear Waves]]