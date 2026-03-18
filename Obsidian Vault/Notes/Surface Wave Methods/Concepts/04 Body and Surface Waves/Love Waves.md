Ondas superficiales que consisten en movimiento puramente de corte y polarizado horizontalmente (SH) [10, 27].

### Condiciones de Existencia
- **Heterogeneidad obligatoria**: A diferencia de las Rayleigh, las ondas Love **no pueden existir en un semiespacio homogéneo** [21, 28].
- **Guía de ondas**: Requieren al menos una capa superior con menor velocidad de corte sobre un semiespacio más rígido para que la energía quede "atrapada" por reflexión total interna [11, 29].

### Comparativa con Rayleigh
- **Polarización**: Horizontal (perpendicular a la dirección de propagación) vs. Vertical/Radial en Rayleigh [30].
- **Dificultad**: Son más difíciles de generar en campo, requiriendo fuentes de impacto horizontal (como golpear lateralmente una viga cargada) [8, 31].
- **Ventaja**: En sitios con grandes contrastes de velocidad, las ondas Love suelen mostrar curvas de dispersión más simples y fáciles de identificar que las Rayleigh [13, 32].
### Dispersión

Las ondas Love son fuertemente **dispersivas** en medios estratificados.

La velocidad de fase depende de la frecuencia de excitación, lo que genera curvas de dispersión observables en arreglos sísmicos.

Conceptos relacionados:

- [[Wave Dispersion]]
- [[Phase Velocity]]
- [[Group Velocity]]

### Relación de dispersión de Love

La condición de frontera en superficie libre ($z = 0$, esfuerzo nulo) y continuidad de desplazamiento y esfuerzo en la interfaz ($z = H$) conduce a:

$$
\tan\left(\beta_1 H\right) = \frac{\mu_2 \beta_2}{\mu_1 \beta_1}
$$

donde:

$$
\beta_1 = \sqrt{\frac{\omega^2}{V_{S1}^2} - k^2}, \qquad \beta_2 = \sqrt{k^2 - \frac{\omega^2}{V_{S2}^2}}
$$

y $\mu_1$, $\mu_2$ son los módulos de corte de la capa superior y del semiespacio respectivamente.

A diferencia de la ecuación secular de Rayleigh en el half-space homogéneo, esta relación contiene $\omega$ y $k$ de forma separada, confirmando que las Love waves son intrínsecamente **dispersivas**.

### Condición física necesaria

Para que existan Love waves la velocidad de fase $c_L$ debe satisfacer:

$$
V_{S1} < c_L < V_{S2}
$$

Cuando esta condición se cumple, las ondas SH quedan atrapadas en la capa por reflexión total interna en la interfaz.

### Modos de propagación

La relación de dispersión admite múltiples soluciones:

- **Modo fundamental (modo 0):** existe para todas las frecuencias; a bajas frecuencias $c_L \to V_{S2}$, a altas frecuencias $c_L \to V_{S1}$.
- **Modos superiores (modo 1, 2, ...):** cada uno tiene una frecuencia de corte mínima $f_c$ por debajo de la cual no puede propagarse.

### Fuente (sección 2.3)

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.3 Love waves in layered media