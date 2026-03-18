# Lamb's Problem

## 1. Concepto

El **Lamb's problem** describe la generación de ondas elásticas producidas por una carga puntual aplicada sobre la superficie de un medio elástico semi-infinito. Es el problema de valor inicial y frontera fundamental de la sismología de superficie.

---

## 2. Fundamento físico

Cuando una fuerza impulsiva se aplica en la superficie, se generan simultáneamente [[P-waves]], [[S-Waves]] y [[Rayleigh Waves]]. Las ondas de cuerpo se propagan hacia el interior del medio expandiéndose en 3D. Las ondas de Rayleigh se propagan a lo largo de la superficie con atenuación geométrica $\propto 1/\sqrt{r}$.

Debido a las diferentes tasas de decaimiento, a distancias suficientemente grandes desde la fuente el campo superficial queda dominado por [[Rayleigh Waves]].

---

## 3. Formulación matemática

La solución de Lamb muestra que la amplitud de las ondas de cuerpo en superficie decae como:

$$
u_{\text{body}} \propto \frac{1}{r^2}
$$

mientras que la amplitud de las ondas de Rayleigh decae como:

$$
u_R \propto \frac{1}{\sqrt{r}}
$$

La transición al régimen dominado por Rayleigh ocurre a distancias del orden de:

$$
r \gtrsim 1 \text{–} 2\,\lambda
$$

donde $\lambda$ es la longitud de onda de Rayleigh.

---

## 4. Aplicación a geófonos

Este resultado justifica la regla práctica de que en arreglos MASW el primer geófono debe ubicarse a una distancia mínima de la fuente para evitar la zona de campo cercano, donde las ondas de cuerpo todavía contaminan significativamente el registro.

Una regla comúnmente citada es colocar el primer receptor a una distancia $\geq \lambda_{max}/2$ o $\geq 1\text{–}2\lambda_{max}$, donde $\lambda_{max}$ es la longitud de onda máxima de interés.

---

## 5. Implicaciones para el diseño experimental

- La distancia fuente-primer geófono debe definirse en función de la profundidad de investigación deseada (que determina $\lambda_{max}$).
- Usar distancias muy cortas introduce contaminación de ondas de cuerpo y puede distorsionar la curva de dispersión a bajas frecuencias.
- Usar distancias muy largas reduce la amplitud de señal por atenuación geométrica y material.
- El balance óptimo depende del sitio y debe ser parte del protocolo experimental documentado.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.2.1, 2.4