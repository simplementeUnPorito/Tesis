# 1D Wave Equation

> [!CONCEPT] Definición
> La **ecuación de onda unidimensional** es el modelo más simple de propagación ondulatoria [[Linear Waves|lineal]]. Describe cómo una perturbación evoluciona en una dimensión espacial propagándose con velocidad constante $c_0$. Es el caso paradigmático de las [[Hyperbolic Partial Differential Equations]] y el punto de partida conceptual para entender ondas sísmicas antes de pasar a la complejidad de [[Rayleigh Waves]] y [[Love Waves]] en medios estratificados.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.1, pp. 38–39.

---

## 1. Formulación matemática

$$
\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}
$$

donde:
- $\phi(x,t)$ — campo de la onda (desplazamiento, presión, etc.)
- $x$ — coordenada espacial
- $t$ — tiempo
- $c_0$ — [[Phase Velocity]] de propagación (constante — no dispersiva)

---

## 2. Solución general

La solución general es la [[d'Alembert Solution]]:

$$
\phi(x,t) = f(x - c_0 t) + g(x + c_0 t)
$$

Esta es una [[Wave Superposition]] de dos ondas viajeras:
- $f(x - c_0 t)$ → se propaga hacia $+x$ con velocidad $c_0$
- $g(x + c_0 t)$ → se propaga hacia $-x$ con velocidad $c_0$

La forma de la onda se conserva perfectamente — no hay dispersión.

---

## 3. Clasificación y propiedades

La 1D Wave Equation es una [[Hyperbolic Partial Differential Equations|PDE hiperbólica]] con discriminante $\Delta = B^2 - 4AC > 0$:

| Propiedad | Valor |
|-----------|-------|
| Tipo PDE | Hiperbólica |
| Dispersiva | No — $c_p = c_0$ independiente de frecuencia |
| Lineal | Sí — aplica [[Wave Superposition]] |
| [[Dispersion Relation]] | $\omega = c_0 k$ (lineal) |
| [[Phase Velocity]] = [[Group Velocity]] | Sí — $c_p = c_g = c_0$ |

---

## 4. Relevancia para ondas sísmicas

En un medio elástico homogéneo, la ecuación de Navier se desacopla en versiones vectoriales de esta ecuación para [[P-waves]] y [[S-Waves]]:

$$
V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}, \quad V_S = \sqrt{\frac{\mu}{\rho}}
$$

Ambas se propagan sin dispersión en medios homogéneos. La dispersión aparece cuando el medio es [[Layered Media]] — esto es la [[Geometric Dispersion]] que explotan los métodos de ondas superficiales.

La 1D Wave Equation sirve como **referencia**: cuando un registro de geófonos muestra dispersión, es porque el subsuelo real se aleja del ideal homogéneo que esta ecuación describe.

---

## 5. Relaciones con otros conceptos

- [[d'Alembert Solution]] — solución general de esta ecuación
- [[Wave Superposition]] — propiedad fundamental de la solución
- [[Linear Waves]] — la ecuación es lineal → aplica superposición
- [[Hyperbolic Partial Differential Equations]] — clase a la que pertenece
- [[Phase Velocity]] — $c_0$, constante en este modelo
- [[Group Velocity]] — igual a [[Phase Velocity]] (no hay dispersión)
- [[Dispersion Relation]] — $\omega = c_0 k$, lineal → no dispersiva
- [[Geometric Dispersion]] — lo que aparece cuando el medio deja de ser homogéneo
- [[Rayleigh Waves]] — caso mucho más complejo que esta ecuación

---

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — la 1D Wave Equation como baseline para la dispersión [[MASW Method|MASW]]
> **Paper 002 (Xia et al. 1999)** formula el [[Forward Problem|problema directo]] del [[MASW Method|MASW]] como la extensión de la propagación en medios homogéneos (gobernada por la 1D Wave Equation) al caso estratificado. El análisis de sensibilidad demuestra que en un medio perfectamente homogéneo ($V_S$ constante con la profundidad), la [[Dispersion Curve|curva de dispersión]] de Rayleigh sería una línea horizontal ($c_R \approx 0.92\,V_S$ independiente de $f$) — exactamente el caso no-dispersivo descrito por la 1D Wave Equation. La dispersión observada en campo (curva $c_R(f)$ creciente con $\lambda$) es evidencia directa de estratificación real y se cuantifica respecto a este baseline homogéneo. La 1D Wave Equation es así el punto de referencia conceptual que hace posible la inversión: la desviación de la no-dispersividad contiene la información del perfil $V_S(z)$.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3).

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–39 |
| Achenbach, J.D. (1984), *Wave Propagation in Elastic Solids* | Cap. 1 |
