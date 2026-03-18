Llamadas así en honor a Lord Rayleigh, quien predijo su existencia en 1885 [2, 20].

### Características de Movimiento
- **Naturaleza**: Resultan de la interacción entre ondas P y ondas SV en la superficie libre [10, 21].
- **Trayectoria de Partícula**: El movimiento es elíptico en el plano vertical de propagación [9]. 
- **Sentido del Movimiento**: 
    - En la superficie, la órbita es **retrógrada** (sentido antihorario) [11, 22].
    - A una profundidad crítica (aprox. $0.2\lambda$), el movimiento se vuelve **progrado** (sentido horario) [11, 22].
- **Velocidad ($V_R$)**: En medios homogéneos, $V_R$ es ligeramente menor que $V_s$ (aprox. $V_R \approx 0.9 V_s$ para una relación de Poisson de 0.25) [23, 24].
### Propagación superficial

Las [[Rayleigh Waves]] se propagan a lo largo de la superficie libre de un medio elástico.

A diferencia de las [[Body Waves]], su patrón de radiación es esencialmente **bidimensional (2D)**, lo que implica que la energía se propaga principalmente a lo largo de la superficie.

Como consecuencia, presentan **menor atenuación geométrica** que las ondas de cuerpo.

En un medio homogéneo semi-infinito:

- fuente lineal → no hay atenuación geométrica
- fuente puntual → la amplitud decae como

$$
\frac{1}{\sqrt{r}}
$$

donde $r$ es la distancia a la fuente.

Las [[Body Waves]] en la misma geometría decaen como

$$
\frac{1}{r^2}
$$

Por esta razón, a distancias del orden de **1–2 longitudes de onda**, el campo sísmico queda dominado por [[Rayleigh Waves]].
### Ventajas en Geotecnia
- Son las ondas más fáciles de generar y detectar mediante geófonos verticales [8].
- Al transportar una gran porción de la energía sísmica, son menos sensibles al ruido que las ondas de cuerpo en superficie [25, 26].
### Decaimiento con profundidad

El desplazamiento asociado a las [[Rayleigh Waves]] decrece **exponencialmente con la profundidad**.

Esto ocurre porque la energía de estas ondas permanece confinada cerca de la superficie.

Gran parte de la energía de deformación se concentra aproximadamente dentro de una profundidad del orden de

$$
\lambda
$$

donde $\lambda$ es la [[Wavelength]].

### Skin depth

La profundidad característica de penetración puede describirse mediante el concepto de [[Skin Depth]].

Se define como la profundidad a la cual la amplitud de la onda se reduce por un factor

$$
\frac{1}{e}
$$

Para [[Rayleigh Waves]] en un medio homogéneo:

$$
\text{Skin depth} \approx 0.94 \lambda
$$

Esto implica que:

- longitudes de onda grandes investigan mayores profundidades
- longitudes de onda pequeñas investigan capas superficiales

### Ecuación secular de Rayleigh

La existencia de las Rayleigh waves en un semiespacio homogéneo se demuestra imponiendo condiciones de esfuerzo nulo en la superficie libre sobre el campo derivado de [[Elastic Wave Potentials]].

El resultado es la **ecuación secular de Rayleigh**:

$$
\left(2 - \frac{c_R^2}{V_S^2}\right)^2 = 4\sqrt{1 - \frac{c_R^2}{V_P^2}}\sqrt{1 - \frac{c_R^2}{V_S^2}}
$$

Expresada como polinomio en $\xi = c_R / V_S$:

$$
\xi^6 - 8\xi^4 + \left(24 - 16\frac{V_S^2}{V_P^2}\right)\xi^2 - 16\left(1 - \frac{V_S^2}{V_P^2}\right) = 0
$$

Este polinomio cúbico en $\xi^2$ tiene una única raíz real físicamente admisible ($0 < c_R < V_S$).

### Velocidad de Rayleigh en función de $\nu$

La velocidad $c_R$ depende únicamente de $V_S$ y del coeficiente de Poisson $\nu$ (que fija el cociente $V_P/V_S$):

$$
\frac{c_R}{V_S} \approx \frac{0.862 + 1.14\nu}{1 + \nu}
$$

(aproximación de Viktorov, válida para $0 \leq \nu < 0.5$)

Valores numéricos de referencia:

| $\nu$ | $c_R / V_S$ |
|--------|-------------|
| 0.00 | 0.874 |
| 0.25 | 0.919 |
| 0.33 | 0.932 |
| 0.50 | 0.955 |

### Implicación crítica para la tesis

Los geófonos miden **velocidad de Rayleigh** $c_R$, no $V_S$ directamente. La conversión requiere conocer o asumir $\nu$. Si $\nu$ no se mide y se asume un valor fijo, se introduce un error sistemático no cuantificado en el perfil $V_S$ resultante.

Para $\nu$ desconocido con incertidumbre $\pm 0.05$ en torno a $0.25$, el error en $c_R/V_S$ es del orden de $\pm 1\text{–}2\%$, lo que se traduce en un error similar en $V_S$.

### No-dispersividad en el half-space homogéneo

En un [[Elastic Half Space]] homogéneo, $c_R$ **no depende de la frecuencia**: la ecuación secular no contiene $\omega$ ni $k$ de forma independiente, solo el cociente $c_R = \omega/k$.

Por lo tanto, las Rayleigh waves en este medio son **no dispersivas**.

Esta es la referencia fundamental: toda dispersión observable en campo es evidencia directa de heterogeneidad vertical del subsuelo.

### Fuente (sección 2.2)

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.2 Rayleigh waves in homogeneous elastic continua