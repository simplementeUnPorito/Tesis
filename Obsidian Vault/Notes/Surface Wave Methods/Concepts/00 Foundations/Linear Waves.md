# Linear Waves

> [!CONCEPT] Definición
> Las **ondas lineales** son ondas cuya propagación puede describirse mediante ecuaciones diferenciales lineales. El principio fundamental que las caracteriza es la **superposición**: si dos soluciones son válidas por separado, su suma también lo es. Este principio es la base de todo el análisis espectral y de la separación modal en geofísica de ondas superficiales.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.1, pp. 38–39.

---

## 1. Fundamento físico

La linealidad aparece cuando las perturbaciones son **suficientemente pequeñas** como para despreciar términos no lineales en las ecuaciones de movimiento. En ese régimen:

- La amplitud no modifica la [[Phase Velocity]] de propagación.
- Las ondas no se deforman por auto-interacción.
- Es válido descomponer la señal en componentes elementales mediante [[Fourier Integral]].
- La [[Wave Superposition]] aplica directamente.

> Linealidad **no** implica ausencia de dispersión. Una onda puede ser lineal y dispersiva simultáneamente — la [[Dispersion Relation]] determina si hay dispersión, no la linealidad de la ecuación.

---

## 2. Formulación matemática

Si $\phi_1(x,t)$ y $\phi_2(x,t)$ son soluciones de una ecuación lineal de ondas, entonces para constantes $a, b$:

$$
a\,\phi_1(x,t) + b\,\phi_2(x,t) \quad \text{también es solución}
$$

La [[1D Wave Equation]] es el ejemplo canónico de ecuación lineal de ondas — una [[Hyperbolic Partial Differential Equations|PDE hiperbólica]] cuya solución general es la suma de dos ondas viajeras ([[Wave Superposition]]).

---

## 3. Aplicación a geófonos

En geofísica near-surface, la teoría usada para interpretar registros de geófonos se construye bajo hipótesis de propagación lineal. Esto habilita:

- Análisis espectral vía [[Fourier Integral]]
- Separación de [[Surface Wave Modes]]
- Formulación del problema directo e inverso de [[Rayleigh Waves]] y [[Love Waves]]
- Descripción de la señal como [[Wave Superposition]] de contribuciones de distintas ondas

---

## 4. Implicaciones para el diseño experimental

- La linealidad es una **hipótesis de trabajo**, no una verdad universal.
- Si la fuente induce deformaciones grandes (explosivos, vibrador cercano), la aproximación lineal puede degradarse.
- La mayor parte de la instrumentación y procesamiento estándar (MASW, SASW, SPAC) asume régimen lineal.
- Conviene mantener fuentes y acoplamientos dentro de un rango reproducible y estable.

---

## 5. Relaciones con otros conceptos

- [[Wave Superposition]] — consecuencia directa de la linealidad
- [[1D Wave Equation]] — ecuación lineal de ondas más simple
- [[Hyperbolic Partial Differential Equations]] — clase de PDE que describe la propagación lineal
- [[Fourier Integral]] — herramienta habilitada por la linealidad
- [[Dispersion Relation]] — determina dispersión, independiente de linealidad
- [[Surface Wave Modes]] — separación modal posible gracias a la superposición

---

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–39 |
