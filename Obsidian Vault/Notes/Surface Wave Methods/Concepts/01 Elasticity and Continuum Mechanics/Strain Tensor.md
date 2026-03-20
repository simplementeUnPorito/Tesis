---
name: Strain Tensor
description: Tensor simétrico de segundo orden que cuantifica la deformación local de un medio continuo; distingue extensión normal de deformación de corte; entrada a la ley de Hooke que genera el tensor de esfuerzos
type: reference
---

# Tensor de Deformación (Strain Tensor)

> **Contexto:** El tensor de deformación $\boldsymbol{\varepsilon}$ describe cómo cambia la geometría local de un medio continuo bajo un campo de desplazamientos $\mathbf{u}(\mathbf{x},t)$. Es uno de los dos tensores fundamentales de la mecánica del continuo elástico (junto con el [[Stress Tensor|tensor de esfuerzos]]) y la entrada a la ley de Hooke que relaciona deformación con esfuerzo. Su divergencia, combinada con la ley de Hooke y la segunda ley de Newton, conduce a las ecuaciones de onda de Navier que gobiernan la propagación de [[Body Waves|ondas de cuerpo]].
> **Fuente:** Foti et al. (2014), Cap. 2.1.1, pp. 36–41.

## Intuición física

Cuando un sólido se deforma, la distancia y el ángulo entre puntos materiales vecinos cambia. El tensor de deformación captura exactamente este cambio local: para cada punto $\mathbf{x}$ del medio, describe cuánto se estira o comprime un segmento infinitesimal (deformación normal) y cuánto rota un par de segmentos ortogonales (deformación de corte).

La distinción entre deformación normal y de corte tiene consecuencias físicas directas:
- La **suma de deformaciones normales** (traza del tensor) mide el **cambio volumétrico**: relacionada con las [[P-waves|ondas P]].
- Las **deformaciones de corte** representan distorsión sin cambio de volumen: relacionadas con las [[S-Waves|ondas S]].

## Definición matemática

Para un campo de desplazamientos $\mathbf{u}(\mathbf{x},t)$ y bajo la hipótesis de **deformaciones pequeñas** ($|\nabla \mathbf{u}| \ll 1$), el tensor de deformación de Cauchy-Green linealizado (tensor de deformación infinitesimal) es:

$$\boldsymbol{\varepsilon} = \frac{1}{2}\left(\nabla\mathbf{u} + (\nabla\mathbf{u})^T\right)$$

En notación indicial:

$$\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)$$

El tensor es **simétrico**: $\varepsilon_{ij} = \varepsilon_{ji}$. Tiene seis componentes independientes en 3D.

## Componentes físicas

$$\boldsymbol{\varepsilon} = \begin{bmatrix} \varepsilon_{11} & \varepsilon_{12} & \varepsilon_{13} \\ \varepsilon_{12} & \varepsilon_{22} & \varepsilon_{23} \\ \varepsilon_{13} & \varepsilon_{23} & \varepsilon_{33} \end{bmatrix}$$

| Tipo de componente | Componentes | Significado físico |
|---|---|---|
| **Deformaciones normales** | $\varepsilon_{11}, \varepsilon_{22}, \varepsilon_{33}$ | Estiramiento/compresión en $x$, $y$, $z$ |
| **Deformaciones de corte** | $\varepsilon_{12}, \varepsilon_{13}, \varepsilon_{23}$ | Cambio de ángulo entre pares de segmentos ortogonales |

## Cambio volumétrico y dilatación

La **traza** del tensor de deformación mide el cambio de volumen relativo (dilatación):

$$\text{tr}(\boldsymbol{\varepsilon}) = \varepsilon_{11} + \varepsilon_{22} + \varepsilon_{33} = \nabla \cdot \mathbf{u} = \theta$$

donde $\theta$ se llama dilatación cúbica. Esta cantidad aparece en la parte P de las ecuaciones de Navier. Para deformación de corte pura (ondas S): $\nabla \cdot \mathbf{u} = 0$ — sin cambio de volumen.

## Ley de Hooke generalizada: vínculo con esfuerzos

En un medio elástico **isótropo**, el [[Stress Tensor|tensor de esfuerzos]] $\boldsymbol{\sigma}$ se relaciona con $\boldsymbol{\varepsilon}$ mediante la ley de Hooke generalizada:

$$\boldsymbol{\sigma} = \lambda\,(\nabla \cdot \mathbf{u})\,\mathbf{I} + 2\mu\,\boldsymbol{\varepsilon}$$

En notación indicial:

$$\sigma_{ij} = \lambda\,\theta\,\delta_{ij} + 2\mu\,\varepsilon_{ij}$$

donde $\lambda$ y $\mu$ son las **constantes de Lamé**:
- $\lambda$ — parámetro que relaciona esfuerzo normal con cambio de volumen.
- $\mu = G$ — módulo de corte: relaciona esfuerzo de corte con deformación de corte.

## Desde deformaciones a ondas elásticas

Sustituyendo la ley de Hooke en la ecuación de movimiento ($\nabla \cdot \boldsymbol{\sigma} = \rho\,\ddot{\mathbf{u}}$) y usando la definición de $\boldsymbol{\varepsilon}$, se obtienen las **ecuaciones de Navier**:

$$(\lambda + \mu)\,\nabla(\nabla \cdot \mathbf{u}) + \mu\,\nabla^2 \mathbf{u} = \rho\,\ddot{\mathbf{u}}$$

La descomposición de Helmholtz $\mathbf{u} = \nabla\phi + \nabla \times \boldsymbol{\psi}$ separa esta ecuación en:
- Ecuación de onda P: $\nabla^2\phi = \ddot{\phi}/V_P^2$, con $V_P = \sqrt{(\lambda+2\mu)/\rho}$.
- Ecuación de onda S: $\nabla^2\boldsymbol{\psi} = \ddot{\boldsymbol{\psi}}/V_S^2$, con $V_S = \sqrt{\mu/\rho}$.

El tensor de deformación es, por tanto, el eslabón que conecta el campo de desplazamientos observable con las propiedades elásticas del medio y las ecuaciones de onda.

## Referencias

- Foti et al. (2014), Cap. 2.1.1, pp. 36–39 — definición del tensor de deformación linealizado y ley de Hooke para medio isótropo.
- Foti et al. (2014), Cap. 2.1.3, pp. 43–46 — ecuaciones de Navier y descomposición P/S.
