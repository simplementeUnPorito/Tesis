---
name: Phase Velocity
description: Velocidad a la que se propaga una frente de fase constante de una onda; magnitud fundamental de las curvas de dispersión experimentales en métodos MASW y SASW
type: reference
---

# Velocidad de Fase (Phase Velocity)

> **Contexto:** La velocidad de fase $c_p = \omega/k$ describe la velocidad de propagación de un punto de fase constante (por ejemplo un máximo) de una onda armónica. En métodos de ondas superficiales es la **observable central**: los métodos MASW, SASW y pasivos estiman la velocidad de fase de [[Rayleigh Waves]] en función de la frecuencia, construyendo la curva de dispersión experimental.
> **Fuente:** Foti et al. (2014), Cap. 2.1.1, pp. 39–40; Cap. 4.1, pp. 206–207.

## Intuición física

Una onda monocromática de la forma $\phi(x,t) = A\,e^{i(kx-\omega t)}$ tiene crestas y valles que se desplazan en el espacio. La cresta ubicada en $x_0$ en el instante $t_0$ satisface $kx_0 - \omega t_0 = \text{const}$. Para seguir esa cresta en el tiempo, debe moverse a velocidad:

$$\frac{dx_0}{dt} = \frac{\omega}{k} = c_p$$

Esta es la velocidad de fase. Físicamente, es la velocidad a la que se "mueve" el patrón ondulatorio en el espacio. En medios sin dispersión, $c_p$ es constante e igual para todas las frecuencias. En medios [[Wave Dispersion|dispersivos]], $c_p$ varía con $\omega$ (y con $k$).

**Importante**: la velocidad de fase no es necesariamente la velocidad a la que se transporta la energía. En medios dispersivos, la energía se propaga con la [[Group Velocity|velocidad de grupo]] $c_g = d\omega/dk$, que en general es distinta de $c_p$.

## Formulación matemática

La velocidad de fase se define como:

$$c_p = \frac{\omega}{k}$$

donde:
- $\omega = 2\pi f$ — frecuencia angular [rad/s]
- $k$ — número de onda [rad/m]
- $c_p$ — velocidad de fase [m/s]

En medios dispersivos, $\omega$ y $k$ están relacionados por la [[Dispersion Relation|relación de dispersión]] $\omega = \omega(k)$, de modo que:

$$c_p(k) = \frac{\omega(k)}{k} = \frac{\omega}{k} \neq \text{const}$$

La **curva de dispersión experimental** es la representación de $c_p(f)$ — velocidad de fase de Rayleigh como función de la frecuencia — obtenida a partir de los registros de geófonos.

## Medición experimental

En un arreglo de geófonos alineado con la dirección de propagación, la velocidad de fase se estima midiendo el retardo de fase entre receptores. Para un par de receptores separados $\Delta x$:

$$c_p = \frac{2\pi f \cdot \Delta x}{\Delta\phi(f)}$$

donde $\Delta\phi(f)$ es la diferencia de fase entre los espectros de Fourier de los dos registros. En la práctica con múltiples receptores:

- **Análisis f-k**: $c_p = \omega/k$ donde $k$ es el número de onda del pico del espectro f-k.
- **Análisis τ-p (slant-stack)**: la velocidad de fase se visualiza directamente en el dominio velocidad–frecuencia.
- **SASW**: estimación punto a punto de $\Delta\phi(f)$ para cada par de receptores.

## Velocidad de fase de Rayleigh

Para [[Rayleigh Waves]] en un [[Elastic Half Space|semiespacio elástico]] homogéneo, la velocidad de fase es constante (no dispersiva) e igual a:

$$c_R \approx f(\nu) \cdot V_S \approx 0.92\,V_S \quad (\text{para } \nu = 0.25)$$

En un medio [[Layered Media|estratificado]], $c_R$ varía con la frecuencia: ondas de alta frecuencia (corta longitud de onda) son sensibles a las capas superficiales y tienen velocidades que reflejan la rigidez local. Ondas de baja frecuencia (longitud de onda larga) promedian el perfil hasta mayor profundidad. Esta dependencia es la [[Geometric Dispersion|dispersión geométrica]].

## Velocidad de fase aparente

En medios estratificados con múltiples [[Surface Wave Modes|modos]], lo que los métodos experimentales miden es la **velocidad de fase aparente** resultante de la superposición de todos los modos activos (ver Foti Ec. 2.93):

$$V_R^{app}(r, \omega) = \frac{\omega}{\partial\psi(r,\omega)/\partial r}$$

La velocidad aparente coincide con la del modo fundamental en medios normalmente dispersivos a distancias intermedias. En medios con fuertes contrastes de velocidad o capas rígidas superficiales, puede diferir significativamente del modo fundamental — lo que introduce sesgo en la inversión si se asume modo fundamental.

## Relación con la inversión

La curva de dispersión experimental $c_p^{exp}(f)$ es la entrada principal de la inversión. El algoritmo de inversión busca el modelo de capas $\mathbf{m} = [V_{S,n}, h_n]$ cuya curva de dispersión teórica $c_p^{teor}(f; \mathbf{m})$ minimiza el desajuste con $c_p^{exp}$:

$$\text{misfit} = \sum_i \left[\frac{c_p^{exp}(f_i) - c_p^{teor}(f_i; \mathbf{m})}{\sigma_i}\right]^2$$

La sensibilidad de $c_p$ a $V_S$ es máxima en las capas cuya profundidad central es $\approx \lambda/3$ a $\lambda/2$.

## Implicaciones para el diseño del arreglo de geófonos

- **Rango de frecuencias medible**: determinado por la longitud del arreglo ($f_{\min} \approx V_{R}/L$) y el espaciado entre receptores ($f_{\max} \approx V_{R}/(2\Delta x)$).
- **Resolución en velocidad**: depende del número de receptores y la longitud total.
- **Error de fase**: el ruido en los registros introduce incertidumbre en $\Delta\phi(f)$, lo que se propaga a incertidumbre en $c_p$. La coherencia entre receptores es un indicador de la confiabilidad de la estimación.

## Referencias

- Foti et al. (2014), Cap. 2.1.1, pp. 39–40 — definición y relación con la relación de dispersión.
- Foti et al. (2014), Cap. 4.1, pp. 206–207 — estimación experimental de velocidad de fase.
- Foti et al. (2014), Cap. 2.4.2.4, pp. 90–95, Ec. 2.93 — velocidad de fase aparente.
