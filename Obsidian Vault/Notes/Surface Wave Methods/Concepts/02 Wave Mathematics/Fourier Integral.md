---
name: Fourier Integral
description: Representación de una señal dispersiva como superposición de ondas monocromáticas; fundamento matemático del análisis f-k en MASW y de la conexión entre velocidad de grupo y transporte de energía
type: reference
---

# Integral de Fourier (Fourier Integral)

> **Contexto:** La integral de Fourier es la herramienta matemática que permite representar cualquier perturbación elástica como una superposición de ondas planas monocromáticas, cada una con su propia frecuencia angular $\omega$, número de onda $k$, y amplitud $A(k)$. En medios dispersivos, cada componente viaja a su propia velocidad de fase $c_p = \omega/k$, y el paquete completo se deforma al propagarse. Este marco es el fundamento teórico del análisis f-k en MASW y de la distinción entre [[Phase Velocity|velocidad de fase]] y [[Group Velocity|velocidad de grupo]].
> **Fuente:** Foti et al. (2014), Cap. 2.1.2, pp. 41–43.

## Intuición física

Un sismógrafo registra un tren de ondas complejo: la señal real no es una onda pura sino la superposición de infinitas frecuencias. La integral de Fourier es el principio que permite descomponer esta señal en sus componentes espectrales y analizarlas individualmente. En un medio no dispersivo, todas las frecuencias viajan a la misma velocidad y el tren de ondas mantiene su forma. En un medio dispersivo (como el suelo estratificado), cada frecuencia viaja a velocidad diferente y el tren se estira en el tiempo — esto es la dispersión observable en los sismogramas de MASW.

## Formulación matemática

La solución general para la propagación de ondas en un medio dispersivo se escribe como una superposición continua de ondas planas:

$$\phi(x, t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} A(k)\, e^{i[kx - \omega(k)\,t]}\, dk$$

donde:
- $A(k)$ — espectro de amplitud complejo en el dominio del número de onda.
- $\omega(k)$ — [[Dispersion Relation|relación de dispersión]]: la función que codifica cómo depende la frecuencia del número de onda en el medio.
- $e^{i(kx - \omega t)}$ — onda plana monocromática con velocidad de fase $c_p = \omega/k$.

Esta representación es la **transformada de Fourier inversa** del espectro $A(k)$, y el espectro se recupera con la **transformada directa**:

$$A(k) = \int_{-\infty}^{\infty} \phi(x, 0)\, e^{-ikx}\, dx$$

## Dispersión y deformación del paquete

**Medio no dispersivo**: si $\omega(k) = c\,k$ con $c$ constante, entonces $e^{i[kx - ckt]} = e^{ik(x - ct)}$ y la integral se reduce a $\phi(x,t) = \phi(x - ct, 0)$: el paquete se desplaza sin deformarse.

**Medio dispersivo**: si $\omega(k)$ es no lineal, las diferentes componentes de $k$ acumulan diferente fase al viajar, y el paquete cambia de forma. La frecuencia portadora parece viajar a $c_p$, pero la envolvente (contorno del paquete de energía) viaja a $c_g$.

### Método de la fase estacionaria

Para un paquete que ha viajado una distancia $x$ grande, la integral está dominada por el número de onda $k^*$ donde la fase es estacionaria:

$$\frac{d}{dk}\left[kx - \omega(k)\,t\right] = 0 \quad \Rightarrow \quad x = \frac{d\omega}{dk}\bigg|_{k^*} \cdot t = c_g(k^*)\, t$$

Esto muestra que la energía asociada al número de onda $k^*$ llega al punto $x$ en el tiempo $t = x/c_g(k^*)$: la **velocidad de grupo** es la velocidad de transporte de energía. Esta es la conexión fundamental entre la representación de Fourier y la [[Group Velocity|velocidad de grupo]].

## Transformada de Fourier discreta y 2D en MASW

En la práctica, el sismograma es un array discreto de muestras $u(x_j, t_n)$ medidas en $N_x$ geófonos a tiempos $t_n$. La transformada de Fourier continua se reemplaza por la **transformada de Fourier discreta (DFT)**, calculada eficientemente con el algoritmo FFT.

El análisis f-k en MASW aplica la **transformada de Fourier 2D** al sismograma:

$$U(f, k) = \sum_{j=1}^{N_x} \sum_{n=1}^{N_t} u(x_j, t_n)\, e^{-i(2\pi f\, t_n - k\, x_j)}$$

El módulo $|U(f, k)|$ es el **espectrograma f-k**. Los modos de Rayleigh aparecen como crestas de alta amplitud en el plano $(f, k)$; la velocidad de fase de cada modo en la frecuencia $f$ es:

$$c_p(f) = \frac{2\pi f}{k_{\text{cresta}}(f)} = \frac{\omega}{k}$$

Extraer la posición de estas crestas para cada $f$ produce la **[[Dispersion Curve|curva de dispersión]]** experimental.

## Limitaciones de la representación discreta

La discretización temporal y espacial impone restricciones al espectro estimado:

| Limitación | Expresión | Origen |
|---|---|---|
| $f_{\max}$ (Nyquist temporal) | $f_{\max} = 1/(2\Delta t)$ | Intervalo de muestreo $\Delta t$ |
| $k_{\max}$ (Nyquist espacial) | $k_{\max} = \pi/\Delta x$ | Espaciado entre geófonos $\Delta x$ |
| Resolución en $f$ | $\Delta f = 1/(N_t \Delta t)$ | Duración total del registro |
| Resolución en $k$ | $\Delta k = 2\pi/(N_x \Delta x)$ | Longitud total del arreglo |

La resolución en $k$ limita la precisión con la que se puede determinar la posición de los picos modales en el espectrograma, y por tanto la precisión de la curva de dispersión extraída.

## Conexión con el teorema de Parseval

La integral de Fourier preserva la energía total de la señal (teorema de Parseval):

$$\int_{-\infty}^{\infty} |\phi(x, t)|^2\, dt = \frac{1}{2\pi} \int_{-\infty}^{\infty} |A(\omega)|^2\, d\omega$$

Esto garantiza que la transformada f-k es un cambio de representación, no una pérdida de información: toda la energía del sismograma está contenida en su espectro f-k, distribuida entre los diferentes modos y frecuencias.

## Referencias

- Foti et al. (2014), Cap. 2.1.2, pp. 41–43 — representación de ondas dispersivas mediante integral de Fourier y fase estacionaria.
- Foti et al. (2014), Cap. 4.1, pp. 194–210 — análisis f-k como implementación discreta de la transformada 2D de Fourier.
