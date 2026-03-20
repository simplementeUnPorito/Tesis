---
name: Skin Depth
description: Profundidad a la que la amplitud de una onda superficial cae a 1/e del valor en superficie; establece la profundidad efectiva de investigación de los métodos de ondas superficiales
type: reference
---

# Profundidad de Piel / Profundidad de Investigación (Skin Depth)

> **Contexto:** El skin depth (profundidad de piel) cuantifica cómo decae la amplitud de las [[Rayleigh Waves]] con la profundidad y establece la **profundidad efectiva de investigación** de los métodos de ondas superficiales. Es la base física de la regla práctica que relaciona longitud de onda con profundidad sondeable.
> **Fuente:** Foti et al. (2014), Cap. 2.2.1, pp. 52–55.

## Intuición física

Las [[Rayleigh Waves]] están confinadas cerca de la superficie libre: la mayor parte de su energía de deformación se concentra en una capa de espesor comparable a la longitud de onda. A mayor profundidad, las partículas apenas se desplazan. Este confinamiento superficial es precisamente lo que define a las ondas superficiales como categoría: ondas cuya amplitud decae exponencialmente al alejarse de la interfaz.

La consecuencia práctica es que la profundidad que una onda de Rayleigh puede "sentir" está determinada por su longitud de onda: ondas largas (baja frecuencia) penetran más profundo que ondas cortas (alta frecuencia). Esta propiedad es el fundamento de la **estrategia de barrido en frecuencia** usada en MASW para explorar perfiles de $V_S$ con distintas profundidades.

## Definición

El skin depth $\delta$ se define como la profundidad $z$ a la cual la amplitud de desplazamiento cae a $1/e \approx 37\%$ del valor en superficie:

$$A(\delta) = \frac{A_0}{e}$$

Para una onda de Rayleigh en un [[Elastic Half Space]] homogéneo, el decaimiento de la componente vertical de desplazamiento puede aproximarse como:

$$u_2(z) \approx A_0\,e^{-\beta z}$$

donde $\beta$ es proporcional al número de onda $k = 2\pi/\lambda$. Esto conduce a:

$$\delta \approx \frac{1}{k} = \frac{\lambda}{2\pi}$$

Sin embargo, la expresión exacta (resolución de las eigenfunciones) muestra que la mayor parte de la **energía de deformación** de la onda de Rayleigh está contenida dentro de una profundidad aproximadamente igual a la longitud de onda:

$$z_{95\%} \approx 0.94\,\lambda_R$$

Esta es la profundidad dentro de la cual se concentra ~95% de la energía total de la onda.

## Regla práctica de profundidad de investigación

En la práctica de los métodos de ondas superficiales, se usa la regla empírica:

$$z_{\max} \approx \frac{\lambda_{\max}}{2} \quad \text{a} \quad \lambda_{\max}$$

donde $\lambda_{\max} = V_{R,\min}/f_{\min}$ es la longitud de onda máxima del experimento. Esta regla es una aproximación conservadora del skin depth, y reconoce que la **sensibilidad de la curva de dispersión** a $V_S$ a una profundidad dada es mayor que cero pero decrece rápidamente más allá de $\lambda/2$.

Por ejemplo, si la frecuencia mínima accesible es $f_{\min} = 5\,\text{Hz}$ y la velocidad de Rayleigh mínima es $V_R = 200\,\text{m/s}$:

$$\lambda_{\max} = \frac{200}{5} = 40\,\text{m} \quad \Rightarrow \quad z_{\max} \approx 20\text{–}40\,\text{m}$$

## Influencia en el diseño del arreglo

El skin depth determina directamente los requerimientos de diseño del arreglo de geófonos:

| Objetivo | Requerimiento | Relación con skin depth |
|---|---|---|
| Mayor profundidad de investigación | Menor $f_{\min}$ | $\lambda_{\max} = V_R/f_{\min}$, $z_{\max} \propto \lambda_{\max}$ |
| Mejor resolución superficial | Mayor $f_{\max}$ | $\lambda_{\min} = V_R/f_{\max}$, espesor mínimo resoluble $\propto \lambda_{\min}/2$ |
| Frecuencia mínima accesible | Mayor longitud del arreglo $L$ | $f_{\min} \approx V_R/L$ |
| Frecuencia máxima sin aliasing | Menor espaciado $\Delta x$ | $f_{\max} = V_R/(2\Delta x)$ |

## Limitaciones de la regla del skin depth

La regla $z_{\max} \approx \lambda/2$ es válida para el modo fundamental en un medio normalmente dispersivo. En medios con inversiones de velocidad (capas blandas intercaladas), la profundidad efectiva puede ser mayor porque los modos superiores penetran más. La sensibilidad real a cada profundidad se cuantifica mediante las **derivadas parciales** $\partial V_R/\partial V_S(z)$ (kernels de sensibilidad), que pueden calcularse numéricamente para cualquier modelo.

## Referencias

- Foti et al. (2014), Cap. 2.2.1, pp. 52–55 — derivación de eigenfunciones y decaimiento con profundidad.
- Foti et al. (2014), Cap. 3.4, pp. 163–180 — aplicación al diseño de arreglos.
