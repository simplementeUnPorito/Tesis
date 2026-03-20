---
name: Wavelength
description: λ = c/f; período espacial de una onda; controla la profundidad de investigación en MASW (~λ/2) y la resolución vertical (~λ/2 mínimo resoluble)
type: reference
---

# Longitud de Onda (Wavelength)

> **Contexto:** La longitud de onda $\lambda$ es la distancia espacial entre dos puntos consecutivos de la misma fase. En los métodos de ondas superficiales, la longitud de onda de Rayleigh $\lambda_R = V_R/f$ es el parámetro que controla directamente la profundidad de investigación y la resolución vertical del perfil $V_S$ obtenido por inversión. El rango de longitudes de onda accesibles en el experimento determina el rango de profundidades que se puede caracterizar.
> **Fuente:** Foti et al. (2014), Cap. 2.1.1, pp. 39–41; Cap. 3.4, pp. 163–180.

## Intuición física

Una onda progresiva sinusoidal tiene dos periodicidades: una en el tiempo (con período $T = 1/f$) y una en el espacio (con período $\lambda$). La longitud de onda es el análogo espacial del período temporal: la distancia que separa dos crestas (o dos ceros, o cualquier par de puntos en la misma fase).

En un medio dispersivo, $\lambda$ no es una propiedad intrínseca del medio sino de la combinación medio + frecuencia: la misma frecuencia produce diferentes longitudes de onda en materiales con distintas velocidades.

## Definición y relaciones fundamentales

La longitud de onda se relaciona con el [[Wavenumber|número de onda]] $k$ y la [[Phase Velocity|velocidad de fase]] $c$ mediante:

$$k = \frac{2\pi}{\lambda}, \qquad \lambda = \frac{c}{f} = \frac{2\pi c}{\omega}$$

donde $\omega = 2\pi f$ es la [[Angular Frequency|frecuencia angular]]. Estas tres representaciones (longitud de onda, número de onda, frecuencia) son equivalentes cuando se conoce la velocidad de fase.

Para ondas de Rayleigh en un semiespacio homogéneo, $c_R \approx 0.92 V_S$ (casi constante), por lo que:

$$\lambda_R \approx \frac{0.92\,V_S}{f}$$

La longitud de onda crece con la velocidad del material y decrece con la frecuencia.

## Longitud de onda y profundidad de investigación

El resultado más importante para MASW es la relación entre $\lambda_R$ y la profundidad efectiva de investigación. Las eigenfunciones de Rayleigh muestran que la amplitud de desplazamiento decae exponencialmente con la profundidad, con la mayor parte de la energía de deformación (~95%) concentrada dentro de $z \lesssim \lambda_R$ (ver [[Skin Depth]]).

La regla práctica ampliamente utilizada es:

$$z_{\max} \approx \frac{\lambda_{\max}}{2} \quad \text{a} \quad \lambda_{\max}$$

donde $\lambda_{\max} = V_{R,\min}/f_{\min}$ es la longitud de onda más larga del experimento. La versión conservadora ($\lambda/2$) reconoce que la sensibilidad de la curva de dispersión a $V_S$ a profundidad $z$ cae rápidamente para $z > \lambda/2$.

**Ejemplo**: con $f_{\min} = 5$ Hz y $V_R \approx 200$ m/s:
$$\lambda_{\max} = 200/5 = 40 \text{ m} \Rightarrow z_{\max} \approx 20\text{–}40 \text{ m}$$

## Longitud de onda y resolución vertical

Del mismo modo que la profundidad de investigación está controlada por $\lambda_{\max}$, la **resolución vertical** (espesor mínimo de capa detectable) está controlada por $\lambda_{\min}$:

$$\Delta z_{\min} \approx \frac{\lambda_{\min}}{2} = \frac{V_{R,\max}}{2\,f_{\max}}$$

donde $\lambda_{\min} = V_{R,\max}/f_{\max}$ es la longitud de onda más corta. Capas más delgadas que $\lambda_{\min}/2$ no pueden resolverse individualmente — su efecto aparece como un gradiente suave en el perfil invertido.

## Rango de longitudes de onda en MASW

El rango de $\lambda_R$ accesible está determinado por el diseño del arreglo:

| Parámetro | Controla | Expresión |
|---|---|---|
| Espaciado geófono $\Delta x$ | $\lambda_{\min}$ (aliasing espacial) | $\lambda_{\min} = 2\Delta x$ |
| Longitud arreglo $L$ | $\lambda_{\max}$ (resolución en $k$) | $\lambda_{\max} \approx L$ |
| Frecuencia de muestreo $f_s$ | $f_{\max}$ temporal | $f_{\max} = f_s/2$ |
| Fuente / terreno | $f_{\min}$ | Depende del experimento |

Para una caracterización de sitio a 20 m de profundidad con $V_S \sim 200$ m/s, se necesita $\lambda_{\max} \approx 40$ m, lo que implica $L \geq 40$ m y $f_{\min} \leq 5$ Hz.

## Aliasing espacial

El teorema de muestreo espacial impone que para medir una onda de longitud de onda $\lambda$ con un arreglo de geófonos de espaciado $\Delta x$, se necesitan al menos **dos muestras por longitud de onda**:

$$\lambda > 2\Delta x \quad \Rightarrow \quad k < \frac{\pi}{\Delta x}$$

Si esta condición no se cumple, las ondas de longitud de onda $\lambda < 2\Delta x$ son aliased: su número de onda aparece reflejado en el espectro f-k a un valor erróneo. En la práctica, esto significa que el espaciado $\Delta x$ debe ser menor que la mitad de la longitud de onda más corta de interés.

## Valores típicos en caracterización geotécnica

| Profundidad objetivo | $V_S$ típico | $f_{\min}$ necesaria | $\lambda_{\max}$ necesaria | $L$ mínimo |
|---|---|---|---|---|
| 5 m | 100–200 m/s | ~20–40 Hz | ~5–10 m | ~10 m |
| 20 m | 150–300 m/s | ~7–15 Hz | ~20–40 m | ~40 m |
| 50 m | 200–500 m/s | ~4–10 Hz | ~50–100 m | ~100 m |

## Referencias

- Foti et al. (2014), Cap. 2.1.1, pp. 39–41 — definición de longitud de onda y relaciones con número de onda.
- Foti et al. (2014), Cap. 3.4, pp. 163–180 — criterios de diseño del arreglo en función de $\lambda$.
