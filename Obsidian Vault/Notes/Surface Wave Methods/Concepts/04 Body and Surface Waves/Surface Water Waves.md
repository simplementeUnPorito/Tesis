# Surface Water Waves

> [!CONCEPT] Definición
> Las **surface water waves** son un caso específico de [[Water Waves]]: ondas que se propagan en la **superficie libre** de un cuerpo de agua bajo la acción de la gravedad. Son el arquetipo de onda dispersiva y sirven en la literatura de geofísica de ondas superficiales como analogía pedagógica directa de las [[Rayleigh Waves]].
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.2.

---

## 1. Características principales

- Se propagan en la interfaz agua-aire (superficie libre).
- Son **dispersivas**: su [[Phase Velocity]] depende de la longitud de onda y de la profundidad $h$.
- En el límite de agua profunda ($kh \gg 1$): ondas de mayor longitud de onda se propagan más rápido → dispersión normal.
- Las partículas describen trayectorias elípticas que decaen exponencialmente con la profundidad — igual que el movimiento de partícula de las [[Rayleigh Waves]].

---

## 2. Relación de dispersión

$$
\omega^2 = gk\tanh(kh)
$$

La [[Phase Velocity]] resulta:

$$
c_p = \frac{\omega}{k} = \sqrt{\frac{g}{k}\tanh(kh)}
$$

y la [[Group Velocity]]:

$$
c_g = \frac{d\omega}{dk} = \frac{c_p}{2}\left(1 + \frac{2kh}{\sinh(2kh)}\right)
$$

En agua profunda: $c_g = c_p/2$ — el paquete viaja a la mitad de velocidad que la fase.

---

## 3. Analogía física con Rayleigh Waves

| Propiedad | Surface Water Waves | [[Rayleigh Waves]] |
|-----------|--------------------|--------------------|
| Medio | Agua (gravedad superficial) | Sólido elástico estratificado |
| Mecanismo de dispersión | Profundidad $h$ (geométrico) | Estratificación Vs(z) (geométrico) |
| Decaimiento con profundidad | Exponencial | Exponencial ([[Skin Depth]]) |
| Movimiento de partícula | Elíptico, retrógrado | Elíptico, retrógrado |
| Velocidad de fase | $c_p(\omega)$ — crece con $\lambda$ | $c_R(\omega)$ — crece con $\lambda$ |

Esta analogía justifica el uso de modelos de water waves como introducción pedagógica a la [[Geometric Dispersion]] en textos de geofísica (Foti 2018, §2.1.2).

---

## 4. Relaciones con otros conceptos

- [[Water Waves]] — concepto padre (categoría general)
- [[Dispersion Relation]] — $\omega^2 = gk\tanh(kh)$
- [[Wave Dispersion]] — dispersión geométrica por profundidad variable
- [[Geometric Dispersion]] — mecanismo físico análogo al de Rayleigh
- [[Phase Velocity]] / [[Group Velocity]] — observables clave
- [[Rayleigh Waves]] — análogo sísmico

---

## 5. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.2, pp. 41–43 |
| Lamb, H. (1932), *Hydrodynamics*, 6th ed., Cambridge University Press | Cap. IX |
