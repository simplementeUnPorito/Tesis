---
name: Vertically Inhomogeneous Media
description: Generalización continua del modelo de capas donde las propiedades elásticas varían continuamente con la profundidad; relevante para depósitos granulares con gradiente de compactación
type: reference
---

# Medios Verticalmente Inhomogéneos (Vertically Inhomogeneous Media)

> **Contexto:** Extensión del modelo de [[Layered Media|capas horizontales]] donde las propiedades elásticas ($\lambda$, $\mu$, $\rho$) son funciones continuas de la profundidad $x_2$. Relevante para depósitos granulares en los que la rigidez aumenta progresivamente con la presión de confinamiento.
> **Fuente:** Foti et al. (2014), Cap. 2.4, pp. 64–95.

## Intuición física

En un depósito sedimentario real, la rigidez del suelo no cambia en saltos abruptos sino que aumenta gradualmente con la profundidad, principalmente por el incremento de la presión de confinamiento (que cierra los contactos entre partículas y aumenta el módulo de corte efectivo). Un abanico aluvial, una arena uniforme depositada en capas sucesivas, o un suelo residual profundo son ejemplos donde la transición entre "capas" es suave y gradual.

El modelo de [[Layered Media|capas]] discretas aproxima este comportamiento con escalones: en cada interfaz las propiedades cambian abruptamente. Esta aproximación introduce artefactos matemáticos (discontinuidades en las derivadas de las eigenfunciones) que pueden afectar la precisión numérica del modelo directo. El modelo continuo evita esta limitación pero requiere esquemas numéricos distintos.

## Definición matemática

En un medio verticalmente inhomogéneo, los parámetros elásticos son funciones de la profundidad:

$$\lambda = \lambda(x_2), \quad \mu = \mu(x_2), \quad \rho = \rho(x_2)$$

Las ecuaciones de Navier para este medio son (Foti Ec. 2.56):

$$\nabla\cdot\boldsymbol{\sigma} = \rho(x_2)\,\ddot{\mathbf{u}}$$

con la ley de Hooke correspondiente. La búsqueda de soluciones del tipo ondas superficiales conduce a sistemas de EDOs ordinarias con coeficientes variables (dependientes de $x_2$), que no tienen solución analítica cerrada en general.

## Sistemas de EDOs para los modos

Para **ondas de Love** (desplazamiento SH, Foti Ec. 2.65):

$$\frac{d}{dx_2}\begin{bmatrix}l_1 \\ l_2\end{bmatrix} = \begin{bmatrix}0 & \mu(x_2)^{-1} \\ k^2\mu(x_2)-\omega^2\rho(x_2) & 0\end{bmatrix}\begin{bmatrix}l_1 \\ l_2\end{bmatrix}$$

Para **ondas de Rayleigh** (Foti Ec. 2.66), sistema de cuarto orden:

$$\frac{d\mathbf{f}}{dx_2} = \mathbf{A}(x_2)\cdot\mathbf{f}(x_2), \qquad \mathbf{f} = [r_1,\, r_2,\, r_3,\, r_4]^T$$

donde $r_1$, $r_2$ son las eigenfunciones de desplazamiento horizontal y vertical, y $r_3$, $r_4$ son los esfuerzos asociados. La matriz $\mathbf{A}(x_2)$ depende continuamente de $\lambda(x_2)$, $\mu(x_2)$ y $\rho(x_2)$.

## Solución numérica

Como los sistemas de EDOs tienen coeficientes variables, se resuelven numéricamente. Las dos estrategias principales son:

1. **Discretización en capas finas**: el perfil continuo se aproxima con muchas capas delgadas ($\Delta x_2$ pequeño), cada una tratada como homogénea. Se aplica entonces el método de [[Layered Media|Thomson–Haskell]] o la matriz de rigidez. La precisión mejora al aumentar el número de capas.

2. **Integración directa de la EDO**: se integra numéricamente el sistema de EDOs con coeficientes variables usando métodos como Runge-Kutta de cuarto orden. Más preciso para perfiles suaves, pero más costoso computacionalmente.

## Diferencias prácticas con el modelo de capas

| Aspecto | Modelo de capas | Medio continuo |
|---|---|---|
| Descripción del perfil | Escalones en Vs(z) | Función suave Vs(z) |
| Parámetros del modelo | Vs, h por capa | Vs(z) funcional |
| Capa vegetal delgada | Bien representada | Puede perderse |
| Gradiente de compactación | Aproximado con N capas | Natural |
| Costo computacional | Menor | Mayor |

## Cuándo usar cada modelo

- **Modelo de capas**: siempre que existan horizontes litológicos diferenciados (interfaz arena/arcilla, tabla de agua, roca sobre sedimento). La estratigrafía del sitio debe justificar el uso de capas con interfaces bien definidas.

- **Modelo continuo**: depósitos granulares homogéneos con gradiente de compactación (arenas fluviales, abanicos aluviales homogéneos, suelos residuales). El ejemplo de La Salle (Foti Cap. 7.2.5, Fig. 7.23) muestra un acuerdo razonable entre ambos modelos con excepción de la capa vegetal superficial, que el modelo continuo no reproduce bien.

## Aplicación en inversión

Los códigos de inversión que usan el modelo continuo (como el de Rix & Lai, 2013) parametrizan el perfil $V_S(z)$ mediante funciones suaves (splines, polinomios, perfiles de potencia $V_S = a\cdot z^b$). Los parámetros de esa función son las incógnitas de la inversión.

La **no-unicidad** de la inversión es si cabe mayor en el modelo continuo que en el modelo de capas, porque la dimensión del espacio de parámetros es efectivamente infinita (función continua). En la práctica se restringen las formas admisibles a una familia paramétrica de dimensión finita.

## Referencias

- Foti et al. (2014), Cap. 2.4, pp. 64–76, Ecs. 2.56–2.74 — formulación matemática.
- Foti et al. (2014), Cap. 7.2.5, p. 375, Fig. 7.23 — comparación práctica capas vs. continuo.
- Rix, G.J. y Lai, C.G. (2013) — código de inversión con modelo continuo.
