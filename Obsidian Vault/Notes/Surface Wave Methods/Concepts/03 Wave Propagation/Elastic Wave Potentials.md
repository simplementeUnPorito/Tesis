---
name: Elastic Wave Potentials
description: Descomposición de Helmholtz del campo de desplazamientos en potencial escalar (ondas P) y vectorial (ondas S); fundamento matemático de la derivación de la ecuación secular de Rayleigh
type: reference
---

# Potenciales de Onda Elástica (Elastic Wave Potentials)

> [!CONCEPT] Definición
> Los **potenciales de onda elástica** son funciones auxiliares que permiten descomponer el campo de desplazamientos $\mathbf{u}$ en dos partes independientes: un potencial escalar $\phi$ (campo irrotacional → [[P-waves|ondas P]]) y un potencial vectorial $\boldsymbol{\psi}$ (campo solenoidal → [[S-Waves|ondas S]]), via la **descomposición de Helmholtz**: $\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}$. Este formalismo desacopla las ecuaciones de Navier y permite derivar la ecuación secular de [[Rayleigh Waves]] aplicando las condiciones de superficie libre sobre los potenciales.
>
> — Foti et al. (2018), §2.2, pp. 50–62.

## 1. Descomposición de Helmholtz

Las ecuaciones de Navier acoplan los movimientos compresional y de corte en un sólido. La descomposición de Helmholtz desacopla el sistema:

$$\mathbf{u} = \nabla \phi + \nabla \times \boldsymbol{\psi}$$

donde:
- $\phi$ — potencial escalar (irrotacional): $\nabla \times (\nabla\phi) = 0$ → ondas P
- $\boldsymbol{\psi}$ — potencial vectorial (solenoidal): $\nabla \cdot (\nabla\times\boldsymbol{\psi}) = 0$ → ondas S

Cada potencial satisface su propia ecuación de onda escalar (desacoplada):

$$\nabla^2 \phi = \frac{1}{V_P^2}\frac{\partial^2 \phi}{\partial t^2}, \qquad \nabla^2 \boldsymbol{\psi} = \frac{1}{V_S^2}\frac{\partial^2 \boldsymbol{\psi}}{\partial t^2}$$

## 2. Solución armónica en el semiespacio (problema 2D)

Para propagación en $x$ con profundidad $z \geq 0$, se proponen soluciones de la forma:

$$\phi = A\,e^{-\alpha z}\,e^{i(kx - \omega t)}, \qquad \psi = B\,e^{-\beta z}\,e^{i(kx - \omega t)}$$

con:

$$\alpha = \sqrt{k^2 - \frac{\omega^2}{V_P^2}}, \qquad \beta = \sqrt{k^2 - \frac{\omega^2}{V_S^2}}$$

La condición $\text{Re}(\alpha) > 0$, $\text{Re}(\beta) > 0$ garantiza decaimiento con la profundidad — condición necesaria para que existan [[Surface Waves|ondas superficiales]] (ligadas a la interfaz).

## 3. Ecuación secular de Rayleigh

Las condiciones de superficie libre en $z = 0$ ($\sigma_{zz} = 0$, $\sigma_{xz} = 0$) imponen un sistema en $A$ y $B$. Para que tenga solución no trivial, el determinante del sistema debe ser cero — esto produce la **ecuación secular de Rayleigh**:

$$\xi^6 - 8\xi^4 + \left(24 - 16\frac{V_S^2}{V_P^2}\right)\xi^2 - 16\left(1-\frac{V_S^2}{V_P^2}\right) = 0, \quad \xi = c_R/V_S$$

que tiene exactamente una raíz real física en $0 < c_R < V_S$.

## 4. Importancia para el forward modeling

Este formalismo es el punto de partida del **[[Forward Problem|problema directo]]** de [[Surface Waves|ondas superficiales]]. Toda la teoría de inversión de ondas de Rayleigh descansa en la solución del sistema de potenciales con condiciones de frontera en cada interfaz del modelo de capas (método de [[Layered Media|Thomson-Haskell]]).

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — potenciales como núcleo del [[Forward Problem|problema directo]] [[MASW Method|MASW]]
> **Paper 002 (Xia, Miller & Park 1999)** implementa el formalismo de potenciales de Helmholtz como núcleo del [[Forward Problem|problema directo]] de [[MASW Method|MASW]]. La ecuación secular generalizada al caso estratificado (derivada iterando las condiciones de frontera con el método de la matriz de transferencia) se evalúa numéricamente para calcular $c_R(\omega)$ dado un perfil $V_S(z)$. El Jacobiano $\partial c_R/\partial V_S$ — calculado analíticamente sobre la base de los potenciales — permite la inversión iterativa convergente en < 10 iteraciones. La validación contra borehole en Kansas confirma que el formalismo de potenciales es suficientemente preciso para caracterización geotécnica real.
>
> — Research Database, entrada 002 (core).

## 5. Relaciones con otros conceptos

- [[Elasticity]] — las ecuaciones de Navier son el punto de partida
- [[P-waves]] — componente irrotacional de la descomposición
- [[S-Waves]] — componente solenoidal
- [[Rayleigh Waves]] — solución que emerge de las condiciones de frontera sobre los potenciales
- [[Layered Media]] — extensión a medios estratificados mediante matrices de transferencia
- [[Rayleigh Eigenproblem]] — formulación matricial del mismo problema

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.2, pp. 50–62 — descomposición de Helmholtz y ecuación secular |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — implementación en forward modeling [[MASW Method|MASW]] |
