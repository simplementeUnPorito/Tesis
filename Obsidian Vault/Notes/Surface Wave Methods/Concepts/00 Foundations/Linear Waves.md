# Linear Waves

## 1. Concepto

Las **ondas lineales** son ondas cuya propagación puede describirse mediante ecuaciones lineales.

Esto implica que la respuesta del sistema preserva el principio de superposición: si dos soluciones son válidas por separado, su suma también lo es.

---

## 2. Fundamento físico

La linealidad aparece cuando las perturbaciones son suficientemente pequeñas como para despreciar términos no lineales.

En ese régimen:

- la amplitud no modifica la velocidad de propagación
- las ondas no se deforman por auto-interacción
- es válido descomponer la señal en componentes elementales

Esto no significa que toda onda lineal sea no dispersiva. Una onda puede ser lineal y aun así ser dispersiva, dependiendo de la relación de dispersión del medio.

---

## 3. Formulación matemática

Si $\phi_1(x,t)$ y $\phi_2(x,t)$ son soluciones de una ecuación lineal de ondas, entonces:

$$
a\,\phi_1(x,t) + b\,\phi_2(x,t)
$$

también es solución, para constantes $a$ y $b$.

La ecuación clásica de onda 1D es un ejemplo de ecuación lineal:

$$
\frac{\partial^2 \phi}{\partial x^2}
=
\frac{1}{c_0^2}
\frac{\partial^2 \phi}{\partial t^2}
$$

---

## 4. Aplicación a geófonos

En geofísica near-surface, gran parte de la teoría usada para interpretar registros de geófonos se construye bajo hipótesis de propagación lineal.

Esto permite:

- usar análisis espectral
- separar modos
- formular problemas directo e inverso
- describir la señal como suma de contribuciones de distintas ondas

---

## 5. Implicaciones para el diseño experimental

- La linealidad es una hipótesis de trabajo, no una verdad universal.
- Si la fuente induce deformaciones grandes, la aproximación lineal puede degradarse.
- La mayor parte de la instrumentación y procesamiento estándar asume régimen lineal.
- Conviene mantener fuentes y acoplamientos dentro de un rango reproducible y estable.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- capítulo o sección: 2.1.1 Two categories of wave motion
- página: 38–39
