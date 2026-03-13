# Fourier Integral

## 1. Concepto

La integral de Fourier permite representar una señal como la superposición de ondas sinusoidales de diferentes frecuencias.

Esta representación es fundamental para el análisis de ondas.

---

## 2. Fundamento físico

Una señal real no es una única frecuencia sino una combinación de muchas.

La integral de Fourier permite descomponer una señal en sus componentes espectrales.

---

## 3. Formulación matemática

La solución general de una ecuación de onda dispersiva puede escribirse como:

$$
\phi(x,t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}A(k)e^{i[kx-\omega(k)t]}dk
$$

Cada término representa una onda monocromática con:

- número de onda $k$
- frecuencia $\omega(k)$

---

## 4. Aplicación a geófonos

Muchos métodos de procesamiento sísmico se basan en transformadas de Fourier, por ejemplo:

- análisis f-k
- análisis espectral
- MASW

Estos métodos permiten identificar las velocidades de fase de las ondas superficiales.

---

## 5. Fuente

PDF: Sebastiano Foti Chapter 2  
Sección: 2.1