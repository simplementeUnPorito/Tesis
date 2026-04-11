# Hyperbolic Partial Differential Equations

> [!CONCEPT] Definición
> Las **ecuaciones en derivadas parciales hiperbólicas** (Hyperbolic PDEs) son una clase de EDPs que gobiernan la propagación de perturbaciones a velocidad finita. Su nombre proviene de la analogía con la sección cónica hipérbola en la clasificación de Cauchy-Kowalewski de ecuaciones de segundo orden.
>
> En geofísica de ondas superficiales, las Hyperbolic PDEs son el marco matemático que describe la propagación de [[Body Waves]] y [[Rayleigh Waves]] en medios elásticos.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.1.

---

## 1. Clasificación de PDEs de segundo orden

Una PDE lineal de segundo orden en dos variables $(x, t)$:

$$
A\frac{\partial^2 u}{\partial x^2} + B\frac{\partial^2 u}{\partial x \partial t} + C\frac{\partial^2 u}{\partial t^2} = F\left(x,t,u,\frac{\partial u}{\partial x},\frac{\partial u}{\partial t}\right)
$$

se clasifica según el discriminante $\Delta = B^2 - 4AC$:

| $\Delta$ | Tipo | Ejemplo físico |
|----------|------|----------------|
| $\Delta > 0$ | **Hiperbólica** | Propagación de ondas |
| $\Delta = 0$ | Parabólica | Difusión de calor |
| $\Delta < 0$ | Elíptica | Electrostática, flujo potencial |

Las Hyperbolic PDEs son las únicas que admiten **soluciones de onda viajera** con velocidad de propagación finita.

---

## 2. Forma canónica: ecuación de onda 1D

El ejemplo más simple es la [[1D Wave Equation]]:

$$
\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}
$$

donde $c_0$ es la [[Phase Velocity]] de propagación. Su solución general es la [[d'Alembert Solution]]:

$$
\phi(x,t) = f(x - c_0 t) + g(x + c_0 t)
$$

representando [[Wave Superposition]] de dos ondas viajeras en sentidos opuestos.

---

## 3. Extensión a 3D — elastodinámica

En un medio elástico isótropo, las ecuaciones de movimiento de Navier forman un sistema de Hyperbolic PDEs vectorial:

$$
\rho\,\ddot{\mathbf{u}} = (\lambda + \mu)\nabla(\nabla\cdot\mathbf{u}) + \mu\nabla^2\mathbf{u}
$$

Este sistema admite dos tipos de soluciones de onda:
- [[P-waves]] — velocidad $V_P = \sqrt{(\lambda+2\mu)/\rho}$
- [[S-Waves]] — velocidad $V_S = \sqrt{\mu/\rho}$

Ambas son soluciones hiperbólicas: se propagan a velocidad finita y transportan información sin difusión.

---

## 4. Relación con la dispersión

Las Hyperbolic PDEs en medios homogéneos producen ondas **no dispersivas**: la [[Phase Velocity]] es independiente de la frecuencia.

Sin embargo, cuando el medio es [[Layered Media]] o [[Viscoelastic Media]], las condiciones de contorno o el comportamiento reológico introducen [[Wave Dispersion]], aunque las ecuaciones sigan siendo hiperbólicas en cada capa.

> Esta intersección — hiperbolicidad local + dispersión global — es la base matemática de los métodos de ondas superficiales para caracterización del subsuelo.

Véase: [[Hyperbolic Waves]], [[Geometric Dispersion]], [[Material Dispersion]].

---

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — sistema hiperbólico de Navier como base del [[Forward Problem|problema directo]] [[MASW Method|MASW]]
> **Paper 002 (Xia et al. 1999)** parte del sistema de Hyperbolic PDEs de Navier para derivar la ecuación secular de Rayleigh en medios estratificados. El carácter hiperbólico garantiza que las perturbaciones se propagan a velocidad finita ($V_P$, $V_S$) y que la solución en cada capa admite la forma $e^{i(kx-\omega t)}$ con dependencia exponencial en profundidad — habilitando el método de la matriz de transferencia. Sin la estructura hiperbólica del sistema de Navier, no existiría el concepto de [[Phase Velocity|velocidad de fase]] bien definida ni la [[Dispersion Curve|curva de dispersión]] que [[MASW Method|MASW]] extrae. El paper demuestra que el análisis de sensibilidad de la [[Dispersion Curve|curva de dispersión]] respecto a $V_S$, $V_P$ y $\rho$ es directo gracias a la linealidad del sistema hiperbólico en cada capa — permitiendo linearizar el problema inverso.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3).

## 5. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–41 |
| Achenbach, J.D. (1984), *Wave Propagation in Elastic Solids*, North-Holland | Cap. 1–2 |
