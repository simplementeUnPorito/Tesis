---
name: Surface Wave Modes
description: Modos de propagación de ondas superficiales en medios estratificados; cada modo tiene su propia velocidad de fase, frecuencia de corte y patrón de desplazamiento profundo
type: reference
---

# Modos de Ondas Superficiales (Surface Wave Modes)

> **Contexto:** En medios [[Layered Media|estratificados]], las [[Rayleigh Waves]] y [[Love Waves]] no se propagan como una única onda sino como un conjunto discreto de modos. Cada modo tiene su propia relación de dispersión, velocidad de fase y patrón de penetración con la profundidad.
> **Fuente:** Foti et al. (2014), Cap. 2.4, pp. 64–95.

## Intuición física

En un [[Elastic Half Space]] homogéneo existe exactamente un modo de Rayleigh y no existen modos de Love. Cuando se añaden capas sobre el semiespacio, la energía puede quedar "atrapada" en diversas combinaciones de reflexiones entre interfaces, lo que da lugar a múltiples patrones de resonancia: los modos de propagación. Cada modo tiene una configuración propia de desplazamiento vs. profundidad (eigenfunción) y una velocidad de fase que varía con la frecuencia (curva de dispersión modal).

La analogía con una guía de ondas acústica es útil: así como una guía rectangular transmite múltiples modos de onda electromagnética a frecuencias distintas, el subsuelo estratificado soporta múltiples modos de onda superficial.

## Definición

Para un modelo de [[Layered Media|capas]] con $N$ capas, a una frecuencia dada $\omega$, la [[Dispersion Relation|ecuación secular]] $\Phi[k, \omega; \mathbf{m}] = 0$ tiene múltiples raíces reales $k_1(\omega) < k_2(\omega) < \cdots < k_M(\omega)$ con $M$ finito. Cada raíz corresponde a un **modo de propagación**:

| Modo | Índice | Número de onda | Velocidad de fase | Penetración |
|---|---|---|---|---|
| Fundamental | $n=0$ (o $n=1$) | mayor $k$ | menor $c_R$ | menor profundidad |
| Primer superior | $n=1$ | segundo mayor $k$ | segunda menor $c_R$ | mayor profundidad |
| ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |

El modo fundamental no tiene frecuencia de corte: existe para cualquier frecuencia. Los modos superiores tienen una **frecuencia de corte** mínima $f_c^n$ por debajo de la cual no se propagan:

$$f_c^n = \frac{(n-1) V_{S,\text{top}}}{2h}, \qquad n = 2, 3, \ldots$$

donde $h$ es el espesor de la capa superficial y $V_{S,\text{top}}$ es su velocidad de corte.

## Eigenfunciones de desplazamiento

Cada modo tiene un patrón de desplazamiento característico en profundidad: la **eigenfunción** $r_1(x_2, k_n)$ (horizontal) y $r_2(x_2, k_n)$ (vertical). Propiedades clave:

- **Modo fundamental**: máxima amplitud en superficie, penetración moderada. Su eigenfunción tiene el comportamiento más "suave" con profundidad.
- **Modos superiores**: menor amplitud en superficie pero mayor amplitud a mayor profundidad. Su eigenfunción tiene más nodos (cambios de signo) con la profundidad.
- A igual frecuencia, los modos superiores penetran más profundamente que el fundamental.

Esta propiedad implica que **los modos superiores son sensibles a la estructura más profunda del perfil** — lo que puede aprovecharse para mejorar la resolución de la inversión.

## Dispersión modal e identificación

La curva de dispersión modal de cada modo se traza en el plano frecuencia–velocidad de fase. En un perfil normalmente dispersivo:

- El modo fundamental tiene velocidad de fase creciente a alta frecuencia (capas más rígidas superficiales) y decreciente a baja frecuencia.
- Los modos superiores tienen velocidades de fase mayores que el fundamental a la misma frecuencia.
- Las curvas modales no se cruzan en medios simples; pueden tener **puntos de osculación** (acercamiento extremo) en medios con fuertes contrastes, donde la energía puede saltar entre modos.

## Curva de dispersión aparente

Lo que los métodos experimentales (f-k, MASW, SASW) miden no es la curva de un modo individual sino la **[[Phase Velocity|velocidad de fase aparente]]** resultante de la superposición de todos los modos activos:

$$V_R^{app}(\omega) = \frac{\omega}{\partial\psi/\partial r}$$

donde $\psi$ es la fase del campo total. En medios normalmente dispersivos, la curva aparente está próxima al modo fundamental a frecuencias intermedias. En medios con inversiones de velocidad o capas rígidas superficiales (que excitan fuertemente modos superiores), la curva aparente puede seguir modos superiores en ciertos rangos de frecuencia.

## Implicaciones para MASW / adquisición

1. **Problema de identificación de modos**: si el espectro f-k muestra múltiples ramas, es necesario identificar a qué modo pertenece cada rama antes de la inversión. Invertir la rama errónea produce perfiles $V_S$ sistemáticamente incorrectos.

2. **Estrategia de offset**: la excitación relativa de modos depende de la distancia fuente-receptor. El modo fundamental domina a distancias intermedias; los modos superiores son más visibles a distancias largas (mayor separación de curvas modales en el espacio $k$).

3. **Longitud de arreglo**: debe ser suficiente para resolver las diferencias en número de onda entre modos a las frecuencias de interés.

4. **Estrategias de inversión**:
   - Inversión multimodal: se incluyen varias curvas modales en la función de desajuste, lo que constraña mejor el perfil de $V_S$ a mayor profundidad.
   - *Determinant misfit* (Maraschini et al. 2010): evita asignar a priori puntos experimentales a modos específicos; evalúa la función secular directamente en los puntos experimentales.

## Referencias

- Foti et al. (2014), Cap. 2.4, pp. 64–95, Figs. 2.21–2.22 — curvas modales y eigenfunciones.
- Maraschini, M. et al. (2010), *Geophysics* — determinant misfit para inversión sin identificación de modos.
