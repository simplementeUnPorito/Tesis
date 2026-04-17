---
aliases: [ecuaciones de Navier, elastodinámica, Navier-Cauchy]
tags: [elasticity, wave-propagation, pde]
---

# Navier Equations

Las **ecuaciones de Navier** (también llamadas ecuaciones de Navier-Cauchy o de la elastodinámica lineal) son el sistema de ecuaciones diferenciales parciales que rige el movimiento de un sólido [[Elasticity|elástico]] lineal isotrópico. Se obtienen combinando la ley de Newton (segunda ley), el [[Strain Tensor|tensor de deformación]] y la [[Hooke's Law|ley de Hooke generalizada]]:

$$
\mu \nabla^2 \mathbf{u} + (\lambda + \mu)\nabla(\nabla \cdot \mathbf{u}) = \rho \frac{\partial^2 \mathbf{u}}{\partial t^2}
$$

donde:
- $\mathbf{u}(\mathbf{x}, t)$ — campo vectorial de desplazamiento
- $\lambda, \mu$ — [[Lamé Constants|constantes de Lamé]] del material
- $\rho$ — densidad del medio
- $\nabla^2 = \Delta$ — operador de Laplace vectorial
- $\nabla \cdot \mathbf{u}$ — divergencia del campo de desplazamiento (deformación volumétrica)

## Interpretación física de cada término

- **$\mu \nabla^2 \mathbf{u}$**: resistencia del material a la deformación de *corte* (relacionada con el [[Shear Modulus|módulo de rigidez]] $G = \mu$). Este término gobierna la propagación de [[S-Waves|ondas S]].
- **$(\lambda + \mu)\nabla(\nabla \cdot \mathbf{u})$**: resistencia a la *compresión* volumétrica. Este término gobierna la propagación de [[P-waves|ondas P]].
- **$\rho\,\partial^2\mathbf{u}/\partial t^2$**: término de inercia (fuerza inercial por unidad de volumen).

## Descomposición en modos independientes

Aplicando la [[Helmholtz Decomposition|descomposición de Helmholtz]] $\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}$, las ecuaciones de Navier se separan en dos ecuaciones de onda independientes:

$$
\nabla^2 \phi = \frac{1}{V_P^2}\frac{\partial^2\phi}{\partial t^2}, \qquad V_P = \sqrt{\frac{\lambda+2\mu}{\rho}}
$$

$$
\nabla^2 \boldsymbol{\psi} = \frac{1}{V_S^2}\frac{\partial^2\boldsymbol{\psi}}{\partial t^2}, \qquad V_S = \sqrt{\frac{\mu}{\rho}}
$$

Esta separación formal es la base del **método de potenciales de onda elástica** ([[Elastic Wave Potentials]]).

## Relevancia para ondas superficiales

Las [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|ondas de Love]] son soluciones de las ecuaciones de Navier con condiciones de frontera específicas en la superficie libre de un [[Elastic Half Space|semiespacio elástico]]:
- Rayleigh: combina potenciales P y SV con esfuerzo nulo en $x_2 = 0$
- Love: utiliza solo el potencial SH con condición de reflexión total en capas estratificadas

La [[Dispersion Curve|curva de dispersión]] que explotan los métodos [[MASW Method|MASW]] se obtiene de las soluciones modales de las ecuaciones de Navier en medios [[Layered Media|estratificados]].

## Véase también

- [[Hooke's Law]] — relación constitutiva que alimenta las ecuaciones de Navier
- [[Helmholtz Decomposition]] — descomposición en ondas P y S
- [[Rayleigh Eigenproblem]] — problema de autovalores derivado de las ecuaciones de Navier
- [[Thomson-Haskell Matrix]] — algoritmo numérico que resuelve las Navier en medios estratificados

*Fuente: Foti et al. (2014), Sec. 2.1.3, pp. 40–48.*
