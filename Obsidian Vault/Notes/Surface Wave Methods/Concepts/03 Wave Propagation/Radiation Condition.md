---
aliases: [condición de radiación, condición de Sommerfeld, condición de campo lejano]
tags: [wave-propagation, boundary-conditions, seismology]
---

# Radiation Condition (Condición de Radiación de Sommerfeld)

La **condición de radiación de Sommerfeld** (o condición de campo lejano) es una condición de frontera en el infinito que exige que las ondas emitidas por una fuente finita se propaguen *hacia afuera* y no regresen. Matemáticamente, para ondas armónicas en 2D/3D, exige que la solución decrezca con la distancia de la forma:

$$
\lim_{r \to \infty} r^{n/2 - 1/2} \left(\frac{\partial u}{\partial r} - ik\,u\right) = 0, \qquad r = |\mathbf{x}|
$$

donde $n$ es la dimensión espacial ($n=2$ en 2D, $n=3$ en 3D) y $k$ el número de onda. Para $n=2$ (problema en plano), esto requiere $u \sim r^{-1/2}e^{ikr}$ en el infinito — exactamente el comportamiento de un frente de onda cilíndrico divergente.

## Interpretación física

La condición de radiación expresa el **principio de causalidad**: las ondas emitidas por una fuente viajan hacia afuera y disipan su energía en el infinito. Sin esta condición, el problema de onda en dominio no acotado es matemáticamente indeterminado — admite tanto ondas entrantes como salientes como soluciones, y la solución no es única.

En el contexto del [[Lamb's Problem]], la condición de radiación selecciona la solución física (ondas divergentes desde la fuente) entre todas las soluciones matemáticamente posibles de las [[Navier Equations|ecuaciones de Navier]].

## Relación con las ondas superficiales

Para las [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|ondas de Love]], la condición de radiación en profundidad adopta la forma de un **decaimiento exponencial** (condición de onda evanescente): los desplazamientos deben tender a cero conforme $x_2 \to \infty$. Esta condición — junto con los esfuerzos nulos en superficie libre — selecciona los **autovalores** (números de onda) que forman los modos de ondas superficiales.

En el [[Rayleigh Eigenproblem|eigenproblem de Rayleigh]], la condición de radiación impone que los coeficientes $\alpha = \sqrt{k^2 - \omega^2/V_P^2} > 0$ y $\beta = \sqrt{k^2 - \omega^2/V_S^2} > 0$, exigiendo $k > \omega/V_S > \omega/V_P$ — lo que garantiza que $c_R < V_S < V_P$.

## Implementación numérica

En simulaciones por elementos finitos o diferencias finitas, el dominio debe truncarse. Las estrategias para imponer la condición de radiación artificialmente incluyen:
- **Capas absorbentes perfectamente ajustadas (PML)**: añaden amortiguamiento artificial en la periferia del dominio
- **Fronteras absorbentes de primer orden**: $\partial u/\partial r = ik\,u$ evaluada en la frontera
- **Elementos infinitos**: formulación de elementos finitos con funciones de forma que satisfacen la condición de campo lejano

## Véase también

- [[Lamb's Problem]] — problema donde la condición de radiación selecciona la solución física
- [[Rayleigh Eigenproblem]] — la condición de radiación en profundidad es parte de las condiciones de borde que definen los modos
- [[Near-field Effect]] — región donde la condición de campo lejano (propagación radial pura) no se satisface aún
- [[Navier Equations]] — sistema cuya solución requiere condiciones de frontera incluyendo la de radiación

*Fuente: Foti et al. (2014), Sec. 2.2.2, p. 55; referencia clásica: Sommerfeld (1949), Partial Differential Equations in Physics.*
