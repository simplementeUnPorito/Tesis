# Strain Tensor

## 1. Concepto

El **tensor de deformación** describe cómo cambia la geometría de un medio continuo cuando se aplica un desplazamiento.

Mide **cómo varían las distancias entre puntos vecinos del material**.

---

## 2. Definición matemática

Para deformaciones pequeñas:

$$
\varepsilon =
\frac{1}{2}
(\nabla u + (\nabla u)^T)
$$

donde:

- $u(x,t)$ es el campo de desplazamiento
- $\nabla u$ es el gradiente del desplazamiento

---

## 3. Interpretación física

Componentes del tensor:

- $\varepsilon_{11}, \varepsilon_{22}, \varepsilon_{33}$  
  → **deformaciones normales**

- $\varepsilon_{12}, \varepsilon_{13}, \varepsilon_{23}$  
  → **deformaciones de corte**

---

## 4. Cambio volumétrico

La **traza** del tensor de deformación:

$$
tr(\varepsilon) =
\varepsilon_{11} +
\varepsilon_{22} +
\varepsilon_{33}
$$

representa el **cambio volumétrico relativo del material**.

Esto se relaciona con la divergencia del desplazamiento:

$$
tr(\varepsilon) = \nabla \cdot u
$$

---

## 5. Relación con esfuerzos

En un material elástico isotrópico:

$$
\sigma =
\lambda tr(\varepsilon) I +
2 \mu \varepsilon
$$

donde:

- $\lambda,\mu$ son constantes de Lamé.

---

## Conceptos relacionados

- [[Stress Tensor]]
- [[Body Waves]]
- [[Linear Waves]]