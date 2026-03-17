# d’Alembert Solution

## 1. Concepto

La **solución de d’Alembert** es la solución general de la ecuación clásica de onda unidimensional.

Expresa la perturbación como la suma de dos ondas que viajan en sentidos opuestos con la misma velocidad.

---

## 2. Fundamento físico

La interpretación física es directa:

- una componente se propaga hacia la derecha
- otra componente se propaga hacia la izquierda

Ambas conservan su forma durante la propagación. Esto refleja el carácter no dispersivo de la ecuación de onda 1D en este caso ideal.

---

## 3. Formulación matemática

La solución general es:

$$
\phi(x,t)=f(x-c_0 t)+g(x+c_0 t)
$$

donde:

- $f(\cdot)$ representa una onda que viaja hacia la derecha
- $g(\cdot)$ representa una onda que viaja hacia la izquierda
- $c_0$ es la velocidad de propagación

Esta expresión muestra que la solución es una [[Wave Superposition]] de dos ondas viajeras.

---

## 4. Aplicación a geófonos

En adquisición sísmica real, el campo registrado puede contener contribuciones que llegan desde distintas direcciones y con distintos tipos de onda.

La solución de d’Alembert ayuda a entender, en el caso más simple, que una señal observada puede representarse como suma de contribuciones propagativas.

---

## 5. Implicaciones para el diseño experimental

- Sirve para construir intuición sobre propagación y retardo temporal.
- Es útil como modelo base antes de estudiar superposición modal y ondas superficiales dispersivas.
- No debe extrapolarse sin cuidado a medios estratificados reales.
- Es un caso idealizado, pero muy útil pedagógicamente.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- capítulo o sección: 2.1.1 Two categories of wave motion
- página: 38–39
