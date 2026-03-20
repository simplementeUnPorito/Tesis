---
name: Elastic Half Space
description: Modelo de semiespacio elástico homogéneo, isotrópico y semi-infinito; medio más simple en el que existen ondas de Rayleigh no dispersivas
type: reference
---

# Semiespacio Elástico (Elastic Half Space)

> **Contexto:** Modelo idealizado de subsuelo consistente en un medio elástico, lineal, isotrópico y homogéneo que ocupa el semi-espacio $z \geq 0$ (superficie libre en $z = 0$). Es el punto de partida teórico de la teoría de ondas superficiales y el caso más simple en que las [[Rayleigh Waves]] existen.
> **Fuente:** Foti et al. (2014), Cap. 2.2, pp. 50–62.

## Intuición física

El semiespacio elástico representa el caso más simple posible: un material perfectamente homogéneo que se extiende infinitamente en profundidad y en horizontal, con una superficie libre plana horizontal en la parte superior. En este medio:

- Existen dos tipos de ondas de cuerpo: [[P-waves]] y [[S-Waves]], que se propagan en todas las direcciones.
- En la interfaz superficie libre–semiespacio, la condición de esfuerzo nulo obliga a que exista también una onda que viaja *a lo largo de la superficie*: las [[Rayleigh Waves]].
- Las ondas de Rayleigh en este medio son **no dispersivas**: viajan siempre a la misma velocidad $V_R \approx 0.92 V_S$, independientemente de la frecuencia.

La no-dispersividad es una consecuencia directa de la homogeneidad: no existe ninguna longitud de escala intrínseca en el medio que pueda hacer que ondas de diferente longitud de onda se propaguen a diferente velocidad. Esto contrasta con el caso de [[Layered Media]], donde la estratificación introduce longitudes de escala (espesores de capa) que producen dispersión.

## Parámetros del modelo

El semiespacio elástico queda completamente definido por tres parámetros:

| Parámetro | Símbolo | Descripción |
|---|---|---|
| Velocidad de onda P | $V_P = \sqrt{(\lambda + 2\mu)/\rho}$ | Controla compresibilidad volumétrica |
| Velocidad de onda S | $V_S = \sqrt{\mu/\rho}$ | Controla rigidez de corte |
| Densidad | $\rho$ | Masa por unidad de volumen |

Los parámetros de Lamé $\lambda$ y $\mu$ equivalentemente describen las propiedades elásticas. El [[Poisson Ratio|coeficiente de Poisson]] $\nu$ relaciona $V_P$ y $V_S$:

$$\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

## Ecuación secular de Rayleigh

La existencia de ondas de Rayleigh en el semiespacio elástico se demuestra aplicando la descomposición de [[Elastic Wave Potentials|potenciales de onda]] y la condición de superficie libre. El resultado es la **ecuación secular** (polinomio en $c_R/V_S$):

$$\xi^6 - 8\xi^4 + \left(24 - 16\frac{V_S^2}{V_P^2}\right)\xi^2 - 16\left(1 - \frac{V_S^2}{V_P^2}\right) = 0, \qquad \xi = \frac{c_R}{V_S}$$

Esta ecuación tiene exactamente una raíz real físicamente admisible en el intervalo $0 < c_R < V_S$.

## Velocidad de Rayleigh

La velocidad de Rayleigh $c_R$ depende únicamente de $V_S$ y del [[Poisson Ratio|coeficiente de Poisson]] $\nu$:

| $\nu$ | $c_R/V_S$ |
|---|---|
| 0.00 | 0.862 |
| 0.25 | 0.919 |
| 0.33 | 0.932 |
| 0.50 | 0.955 |

Para $\nu = 0.25$ (valor clásico de muchas rocas): $c_R \approx 0.919\,V_S$.

**Consecuencia práctica**: los geófonos miden $c_R$. Para obtener $V_S$ se necesita conocer $\nu$. Si $\nu$ no se conoce, se introduce una incertidumbre del orden de 4–9% en $V_S$ según el rango plausible de $\nu$.

## Movimiento de partícula

En el semiespacio, las partículas en superficie describen una **elipse retrógrada** en el plano vertical de propagación:
- Componente vertical amplia que la horizontal (~1.5:1 en superficie).
- En superficie: movimiento retrograde (elipse recorrida en sentido antihorario para propagación en $+x$).
- A profundidad crítica $x_2^c \approx 0.2\lambda$: la componente horizontal se anula, inversión de sentido de la órbita.
- Por debajo de esa profundidad: movimiento prograde.

Esta polarización elíptica con dominancia vertical es la razón por la que los **geófonos verticales** capturan eficientemente las ondas de Rayleigh.

## Decaimiento con profundidad

Los desplazamientos decaen exponencialmente con la profundidad. La mayor parte de la energía está confinada dentro de una profundidad $\approx \lambda_R$ (longitud de onda de Rayleigh). El **[[Skin Depth]]** (profundidad donde la amplitud cae a $1/e$ del valor superficial) es $\approx 0.94\lambda_R$. Esta propiedad establece la **regla de investigación**: la profundidad máxima explorada es aproximadamente $\lambda_R/2$ a $\lambda_R$.

## Decaimiento geométrico

Para una fuente puntual vertical en la superficie libre, la amplitud de las ondas de Rayleigh decae con la distancia $r$ desde la fuente como:

$$A_R \propto \frac{1}{\sqrt{r}}$$

mientras que las ondas de cuerpo en la misma superficie decaen como $1/r^2$. Esto implica que a distancias mayores de una o dos longitudes de onda, el campo de ondas queda dominado por las ondas de Rayleigh. Es la base experimental de los métodos MASW y SASW.

## Relación con medios reales

El semiespacio elástico es una idealización: ningún suelo real es perfectamente homogéneo. En la práctica:

- El semiespacio homogéneo sirve como **referencia teórica** para derivar límites asintóticos de la curva de dispersión.
- La diferencia entre la curva de dispersión experimental y la velocidad constante del semiespacio equivalente **cuantifica la heterogeneidad** del perfil.
- Los **métodos de inversión empírica** usan la relación $V_S \approx V_R/0.92$ como primera estimación antes de una inversión formal (véase [[Inversión]]).

## Referencias

- Lord Rayleigh (1885). *Proc. London Math. Soc.*, 17, 4–11 — predicción teórica original.
- Foti et al. (2014), Cap. 2.2, pp. 50–62, Ecs. 2.36–2.46 — derivación completa incluyendo eigenfunciones y Fig. 2.15.
