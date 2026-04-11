---
name: Wave Dispersion
description: Fenómeno por el que distintas componentes espectrales de una onda viajan a velocidades diferentes; la dispersión geométrica en medios estratificados es la base de [[MASW Method|MASW]]
type: reference
---

# Dispersión de Ondas (Wave Dispersion)

> [!CONCEPT] Definición
> La **dispersión de ondas** es el fenómeno por el cual distintas componentes frecuenciales de una señal se propagan a velocidades de fase diferentes $c_p(\omega) \neq \text{const}$. En un medio no dispersivo, $\omega = ck$ con $c$ constante y el paquete mantiene su forma. En un medio dispersivo, la [[Dispersion Relation|relación de dispersión]] $\omega(k)$ es no lineal: el paquete se deforma al propagarse y la [[Phase Velocity|velocidad de fase]] difiere de la [[Group Velocity|velocidad de grupo]]. En geofísica de superficie, la **dispersión geométrica** de las [[Rayleigh Waves]] en [[Layered Media|medios estratificados]] es el observable que permite inferir $V_S(z)$.
>
> — Foti et al. (2018), §2.1.1, pp. 39–41; §2.1.2, pp. 41–42.

## 1. Concepto

La dispersión de ondas ocurre cuando el medio impone una relación $\omega(k)$ no lineal: diferentes frecuencias viajan a velocidades de fase distintas. Una señal no monocromática se propaga como una superposición de ondas (ver [[Fourier Integral]]):

$$\phi(x,t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} A(k)\,e^{i[kx - \omega(k)t]}\,dk$$

Si $\omega(k)$ es no lineal, el paquete se "estira" en el tiempo al propagarse: las componentes de alta frecuencia y las de baja frecuencia acumulan diferente retraso de fase.

## 2. Dos categorías de dispersión

| Tipo | Origen | Ejemplo en geofísica |
|---|---|---|
| **[[Geometric Dispersion|Dispersión geométrica]]** | Estratificación del medio — diferentes $\lambda$ sondean distintas profundidades | [[Rayleigh Waves]] en suelo estratificado |
| **Dispersión material** | Propiedades elásticas dependientes de $\omega$ — viscoelasticidad, [[Attenuation|atenuación]] | Suelos con rigidez dependiente de frecuencia |

En la práctica de métodos de [[Surface Waves|ondas superficiales]] ([[MASW Method|MASW]], [[SASW Method|SASW]]), la dispersión dominante es **geométrica**: el medio es estratificado y las ondas de Rayleigh de diferente [[Wavelength|longitud de onda]] penetran a diferentes profundidades, "viendo" diferentes velocidades.

## 3. Condición matemática de dispersividad

Una onda es dispersiva si y solo si:

$$\frac{d c_p}{d k} \neq 0 \quad \Leftrightarrow \quad c_g \neq c_p$$

donde $c_p = \omega/k$ es la [[Phase Velocity|velocidad de fase]] y $c_g = d\omega/dk$ es la [[Group Velocity|velocidad de grupo]]. En un medio no dispersivo, $c_p = c_g = c$ constante.

## 4. Implicaciones para el diseño experimental

- La dispersión observable depende del rango frecuencial excitado por la fuente
- La geometría del arreglo condiciona el rango de [[Wavelength|longitudes de onda]] muestreado
- En métodos de [[Surface Waves|ondas superficiales]], la [[Dispersion Curve|curva de dispersión]] $c_p(f)$ es el dato primario de la inversión para obtener $V_S(z)$

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — primera medición sistemática de la dispersión geométrica en [[SASW Method|SASW]]
> **Paper 003 (Nazarian & Stokoe 1984)** introduce el método [[SASW Method|SASW]] precisamente sobre la base de la dispersión geométrica de las ondas de Rayleigh: las componentes de baja frecuencia ([[Wavelength|longitud de onda]] larga) penetran más profundo y viajan más rápido en sitios con velocidad creciente con la profundidad (normalmente dispersivos). Midiendo la fase relativa entre dos [[Geophone|geófono]] separados una distancia $d$, extraen $c_p(f)$ directamente — y demuestran que la [[Dispersion Curve|curva de dispersión]] así obtenida invierte de forma única para el perfil $V_S(z)$. Este trabajo fundacional validó la dispersión geométrica de Rayleigh como observable de caracterización de sitio.
>
> — Research Database, entrada 003 (core).

## 5. Relaciones con otros conceptos

- [[Geometric Dispersion]] — dispersión en medios estratificados (mecanismo dominante en [[MASW Method|MASW]])
- [[Dispersion Relation]] — $\omega(k)$: la función que codifica toda la dispersividad del medio
- [[Phase Velocity]] — $c_p = \omega/k$: el observable experimental primario
- [[Group Velocity]] — $c_g = d\omega/dk$: velocidad de transporte de energía; $c_g \neq c_p$ en dispersión
- [[Fourier Integral]] — marco matemático de la superposición de componentes espectrales
- [[Rayleigh Waves]] — el tipo de onda cuya dispersión se invierte en [[MASW Method|MASW]]
- [[Layered Media]] — la causa física de la dispersión geométrica

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 39–41 — dispersión en propagación de ondas |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.2, pp. 41–42 — velocidades de fase y grupo |
| Foti et al. (2018), *Surface Wave Methods* | §4.1, pp. 205–206 — dispersión geométrica en curva experimental |
| Nazarian & Stokoe (1984) | Paper 003 — [[SASW Method|SASW]] basado en dispersión geométrica |
