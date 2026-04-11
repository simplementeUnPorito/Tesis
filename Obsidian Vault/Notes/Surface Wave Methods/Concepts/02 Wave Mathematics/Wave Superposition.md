# Wave Superposition

> [!CONCEPT] Definición
> La **superposición de ondas** es el principio según el cual la respuesta total de un sistema [[Linear Waves|lineal]] puede obtenerse sumando las contribuciones de varias ondas independientes. Es una propiedad emergente de la linealidad de las ecuaciones de movimiento y la base matemática del análisis espectral y la separación modal en geofísica.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.1, pp. 38–40.

---

## 1. Fundamento físico

Cuando el medio está gobernado por ecuaciones lineales ([[Hyperbolic Partial Differential Equations]]), las ondas coexisten sin modificarse mutuamente de forma no lineal. Por ello, es posible describir una señal compleja como la suma de componentes más simples.

En la [[d'Alembert Solution]], la perturbación total se expresa como superposición de dos ondas viajeras en sentidos opuestos:

$$
\phi(x,t) = f(x - c_0 t) + g(x + c_0 t)
$$

---

## 2. Formulación matemática

Si $\phi_1$ y $\phi_2$ son soluciones de la [[1D Wave Equation]], para constantes $a, b$:

$$
\phi(x,t) = a\,\phi_1(x,t) + b\,\phi_2(x,t)
$$

también es solución. Generalizado a la descomposición espectral vía [[Fourier Integral]]:

$$
\phi(x,t) = \int_{-\infty}^{\infty} A(k)\, e^{i(kx - \omega t)}\, dk
$$

donde cada componente $e^{i(kx-\omega t)}$ viaja con su propia [[Phase Velocity]] $c_p = \omega/k$ determinada por la [[Dispersion Relation]].

---

## 3. Aplicación a geófonos

Los registros de geófonos contienen superposición de múltiples componentes:

| Componente | Origen |
|-----------|--------|
| [[Rayleigh Waves]] modo fundamental | Ondas superficiales dominantes |
| [[Surface Wave Modes|Modos superiores]] | Superposición modal — altera velocidad aparente |
| [[Love Waves]] | Componente horizontal superpuesta |
| [[Body Waves]] | [[P-waves]] y [[S-Waves]] directas y reflejadas |
| [[Near-field Effect|Campo cercano]] | Interferencia ondas de cuerpo + superficiales |

Entender la superposición es esencial para:
- Interpretar interferencia constructiva/destructiva en el espectro f-k
- Separación modal en [[MASW Method]]
- Detección del [[Near-field Effect]]

---

## 4. Implicaciones para el diseño experimental

- Muchas dificultades de interpretación nacen de señales superpuestas.
- El procesamiento f-k busca separar contribuciones modales aprovechando la superposición.
- La superposición modal puede alterar la velocidad aparente observada — riesgo de inversión errada.
- La linealidad del sistema es la base que permite usar [[Fourier Integral]] y análisis multicanal.

---

## 5. Relaciones con otros conceptos

- [[Linear Waves]] — condición necesaria para que aplique la superposición
- [[1D Wave Equation]] — ecuación donde la superposición es exacta
- [[d'Alembert Solution]] — superposición de dos ondas viajeras
- [[Fourier Integral]] — generalización espectral de la superposición
- [[Surface Wave Modes]] — modos como componentes de la superposición
- [[Near-field Effect]] — superposición indeseada de body waves y surface waves
- [[Dispersion Relation]] — gobierna $c_p$ de cada componente

---

> [!EXAMPLE] Evidencia empírica: Xu et al. (2006) — error por superposición modal en [[MASW Method|MASW]]
> **Paper 014 (Xu et al. 2006)** demuestra cuantitativamente las consecuencias de ignorar la superposición de modos superiores en la inversión [[MASW Method|MASW]]. Cuando el espectrograma f-k muestra energía de dos o más modos superpuestos sin separación clara, tomar la cresta del espectrograma como velocidad del modo fundamental produce una [[Dispersion Curve|curva de dispersión]] "aparente" sesgada — una superposición ponderada por energía de los modos presentes. En los experimentos sintéticos del paper (modelos con inversión de velocidad), este sesgo produce perfiles $V_S(z)$ con errores de hasta **50%** en las capas profundas respecto al modelo verdadero. La solución propuesta es la inversión multimodal: en lugar de separar modos en el espectrograma, se invierte la [[Phase Velocity|velocidad de fase]] aparente directamente, incluyendo la superposición modal en el cálculo teórico. El resultado demuestra que la superposición modal — consecuencia directa del principio de superposición — es el artefacto dominante en sitios con perfiles de velocidad complejos.
>
> — Research Database, entrada 014 (core); Xu et al. (2006), *Journal of Applied Geophysics* 59(4).

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–40 |
| Foti et al. (2018), *Surface Wave Methods* | §1.5.1 Higher modes, pp. 22–23 |
