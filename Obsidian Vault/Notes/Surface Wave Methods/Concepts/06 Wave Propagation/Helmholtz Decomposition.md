---
name: Helmholtz Decomposition
description: Descomposición del campo de desplazamiento en potencial escalar (ondas P) y potencial vectorial (ondas S) — base para separar modos de propagación en medios elásticos
type: reference
---

# Helmholtz Decomposition — Descomposición de Helmholtz

> [!CONCEPT] Definición
> La **Descomposición de Helmholtz** (o *Helmholtz decomposition*, *Lamé decomposition*) establece que cualquier campo de desplazamiento $\mathbf{u}(\mathbf{x}, t)$ en un medio elástico puede descomponerse en la suma de un **campo irrotacional** (gradiente de un escalar) y un **campo solenoidal** (rotacional de un vector):
> $$\mathbf{u} = \nabla\phi + \nabla\times\mathbf{\psi}$$
> donde $\phi$ es el **potencial escalar** (asociado a las [[P Wave|ondas de compresión P]]) y $\mathbf{\psi}$ es el **potencial vectorial** (asociado a las [[S Wave|ondas de corte S]]). Sustituyendo en la ecuación de Navier de la elastodinámica, los potenciales satisfacen ecuaciones de onda desacopladas independientes:
> $$\nabla^2\phi - \frac{1}{V_P^2}\ddot{\phi} = 0, \quad \nabla^2\mathbf{\psi} - \frac{1}{V_S^2}\ddot{\mathbf{\psi}} = 0$$
> con $V_P = \sqrt{(\lambda + 2\mu)/\rho}$ y $V_S = \sqrt{\mu/\rho}$ (ver [[Lamé Constants|constantes de Lamé]]). En el contexto de las ondas de Rayleigh, la Descomposición de Helmholtz es fundamental: la onda de Rayleigh es una **combinación acoplada** de onda P evanescente (potencial $\phi$) y onda S evanescente (potencial $\psi$) — cuya acoplamiento en la condición de contorno de superficie libre produce la ecuación de dispersión de Rayleigh para el semiespacio homogéneo. Para el semiespacio estratificado, el mismo principio se aplica en cada capa del [[Thomson-Haskell Matrix|método de matrices de Thomson-Haskell]].
>
> — Foti et al. (2018), §2.1.1; Aki & Richards (2002), §4.1; Achenbach (1973).

## Aplicación a ondas de Rayleigh

Para un semiespacio homogéneo con propagación en la dirección $x$ y coordenada vertical $z$ positiva hacia abajo, los potenciales de la onda de Rayleigh son:

$$\phi(x, z, t) = A \, e^{-pz} e^{i(kx - \omega t)}, \quad \psi(x, z, t) = B \, e^{-qz} e^{i(kx - \omega t)}$$

donde $p = \sqrt{k^2 - k_P^2}$ y $q = \sqrt{k^2 - k_S^2}$ son los decaimientos evanescentes de las ondas P y S en profundidad (condición de existencia: $k > k_S > k_P$, es decir $c_R < V_S < V_P$).

Los desplazamientos en términos de los potenciales:

$$u_x = \frac{\partial\phi}{\partial x} - \frac{\partial\psi}{\partial z}, \quad u_z = \frac{\partial\phi}{\partial z} + \frac{\partial\psi}{\partial x}$$

La condición de superficie libre ($\sigma_{zz} = \sigma_{xz} = 0$ en $z = 0$) genera el sistema $2\times 2$ en $(A, B)$ cuyo determinante igual a cero produce la **ecuación secular de Rayleigh**.

## Implicación para la partícula de movimiento elíptico

La combinación de las componentes $u_x$ (horizontal) y $u_z$ (vertical) de la onda de Rayleigh — cada una con contribuciones de $\phi$ y $\psi$ — produce el movimiento **elíptico retrógrado** (en campo lejano) de la partícula de suelo: la componente vertical domina sobre la horizontal en superficie, con relación típica $|u_z|/|u_x|$ = 1.0–1.5 dependiendo del coeficiente de Poisson.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Descomposición de Helmholtz en la derivación de la ecuación secular
> Foti et al. (2018, §2.1.1) aplican la Descomposición de Helmholtz como primer paso en la derivación de la ecuación de dispersión de las ondas de Rayleigh para un semiespacio estratificado. Los potenciales $\phi$ y $\psi$ en cada capa satisfacen las ecuaciones de onda de P y S respectivamente, con condiciones de interfaz (continuidad de desplazamiento y estrés) que acoplan los potenciales entre capas. El [[Thomson-Haskell Matrix|método de matrices de Thomson-Haskell]] es precisamente la implementación matricial de este acoplamiento: la matriz de capa $M_j$ transforma los potenciales en la parte superior de la capa $j$ a la parte inferior, propagando la solución desde la superficie hasta el semiespacio inferior. La ecuación secular ($\det[M_{total}] = 0$) determina los valores de $k_R$ para cada $\omega$ — es decir, la curva de dispersión.
>
> — Foti et al. (2018), §2.1.1, pp. 27–40; Aki & Richards (2002), §7.1–7.2.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1 — descomposición y ondas de Rayleigh |
| Aki & Richards (2002), *Quantitative Seismology* | §4.1 — Descomposición de Helmholtz en elastodinámica |
| Achenbach (1973), *Wave Propagation in Elastic Solids* | Cap. 2 — potenciales de desplazamiento |
