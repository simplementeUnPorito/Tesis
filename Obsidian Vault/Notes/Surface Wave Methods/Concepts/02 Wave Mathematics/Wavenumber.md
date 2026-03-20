---
name: Wavenumber
description: k = 2π/λ; número de onda espacial en rad/m; análogo espacial de la frecuencia angular; aparece en la relación de dispersión y en el análisis f-k como eje horizontal
type: reference
---

# Número de Onda (Wavenumber)

> **Contexto:** El número de onda $k = 2\pi/\lambda$ es la representación espacial de la frecuencia: mide cuántos ciclos de fase (en radianes) ocurren por metro en la dirección de propagación. Es el análogo espacial de la [[Angular Frequency|frecuencia angular]] $\omega$, y junto con ella define completamente el comportamiento de una onda plana. En MASW, $k$ es uno de los dos ejes del espectrograma f-k; la velocidad de fase se lee directamente como $c_p = \omega/k$.
> **Fuente:** Foti et al. (2014), Cap. 2.1.1, pp. 39–41.

## Intuición física

Si una onda sinusoidal tiene [[Wavelength|longitud de onda]] $\lambda$, entre dos puntos separados una distancia $\lambda$ la fase ha avanzado exactamente $2\pi$ radianes (un ciclo completo). El número de onda $k$ mide la tasa de cambio de fase por unidad de distancia: es la "frecuencia espacial" de la onda. Un $k$ grande significa longitudes de onda cortas (oscilación espacial rápida); un $k$ pequeño corresponde a longitudes de onda largas (variación espacial lenta).

En medios dispersivos, $k$ no es simplemente $\omega/c$ con $c$ constante: la relación $\omega(k)$ — la [[Dispersion Relation|relación de dispersión]] — puede ser no lineal, y diferentes frecuencias tienen diferentes velocidades de fase $c_p = \omega/k$.

## Definición y relaciones fundamentales

$$k = \frac{2\pi}{\lambda}, \qquad k = \frac{\omega}{c_p} = \frac{2\pi f}{c_p}$$

En una onda plana armónica $\phi(x,t) = A\,e^{i(kx - \omega t)}$, el número de onda $k$ controla la **variación espacial** de la fase, del mismo modo que $\omega$ controla la variación temporal.

La relación entre $k$, $\omega$ y la [[Phase Velocity|velocidad de fase]] $c_p$:

$$c_p = \frac{\omega}{k}, \qquad k = \frac{\omega}{c_p}$$

Y la [[Group Velocity|velocidad de grupo]]:

$$c_g = \frac{d\omega}{dk}$$

es la derivada de $\omega$ respecto a $k$ a lo largo de la curva de dispersión $\omega(k)$.

## Número de onda complejo: atenuación

En medios disipadores, el número de onda se generaliza a un valor complejo:

$$k^* = k + i\alpha$$

donde la parte real $k = \omega/c_p$ controla la velocidad de fase y la parte imaginaria $\alpha$ es el **coeficiente de atenuación espacial**: cuantifica cuánta amplitud pierde la onda por metro de propagación debido a [[Attenuation|atenuación]] material. Una onda plana en un medio disipador:

$$\phi(x,t) = A\,e^{i(k^*x - \omega t)} = A\,e^{-\alpha x}\,e^{i(kx - \omega t)}$$

decae exponencialmente con la distancia a tasa $\alpha$ (unidades: 1/m o Np/m).

## Rol en el análisis f-k (MASW)

El análisis f-k transforma el sismograma $u(x, t)$ al dominio $(\omega, k)$ mediante la transformada de Fourier 2D. En el espectrograma f-k resultante:

- El **eje horizontal** es $k$ (en rad/m o ciclos/m).
- El **eje vertical** es $f$ (o $\omega$).
- Cada modo de Rayleigh aparece como una **cresta** cuya pendiente $\omega/k$ da la velocidad de fase.

Para extraer la curva de dispersión se identifica el máximo de amplitud en $k$ para cada frecuencia $f$:

$$c_p(f) = \frac{2\pi f}{k_{\text{cresta}}(f)}$$

## Resolución en k y longitud del arreglo

La resolución del espectrograma f-k en el eje $k$ depende de la longitud total del arreglo $L$:

$$\Delta k = \frac{2\pi}{L}$$

Una longitud mayor permite resolver con más precisión el pico de cada modo en el espectrograma, mejorando la precisión de la curva de dispersión extraída. El aliasing espacial ocurre cuando $k > \pi/\Delta x$ (donde $\Delta x$ es el espaciado entre geófonos).

## Referencias

- Foti et al. (2014), Cap. 2.1.1, pp. 39–41 — definición de $k$ en el contexto de ondas armónicas.
- Foti et al. (2014), Cap. 4.1, pp. 194–210 — número de onda en el análisis f-k y curva de dispersión experimental.
