# Wave Dispersion

## 1. Concepto

La **dispersión de ondas** es el fenómeno por el cual distintas componentes espectrales de una señal se propagan con velocidades diferentes.

Como consecuencia, una señal no monocromática cambia de forma durante la propagación.

---

## 2. Fundamento físico

Una señal real puede representarse como superposición de componentes con diferentes números de onda y frecuencias.

Si la relación entre frecuencia angular y número de onda no es lineal, entonces cada componente puede propagarse con una velocidad de fase distinta. En ese caso, el paquete de ondas se deforma a medida que avanza.

Por tanto, la dispersión no es simplemente “que haya muchas frecuencias”, sino que el medio impone una relación $\omega(k)$ que hace que esas componentes no viajen todas igual.

---

## 3. Formulación matemática

Una onda dispersiva admite soluciones del tipo:

$$
\phi(x,t)=A e^{i[kx-\omega(k)t]}
$$

donde la frecuencia angular depende del número de onda.

La velocidad de fase es:

$$
c_p=\frac{\omega(k)}{k}
$$

y la velocidad de grupo es:

$$
c_g=\frac{d\omega}{dk}
$$

Si $c_p$ depende de $k$, la onda es dispersiva.

---

## 4. Aplicación a geófonos

En caracterización del subsuelo con geófonos, la dispersión es clave porque las [[Rayleigh Waves]] propagándose en medios estratificados presentan velocidades dependientes de la frecuencia.

Eso permite construir curvas de dispersión y luego inferir propiedades del subsuelo.

En near-surface geophysics, la práctica habitual se centra en la **velocidad de fase**; la velocidad de grupo existe y es físicamente relevante, pero se usa menos en inversión de sitio.

---

## 5. Implicaciones para el diseño experimental

- La dispersión observable depende del rango frecuencial excitado por la fuente.
- La geometría del arreglo condiciona el rango de longitudes de onda muestreado.
- No toda dispersión tiene el mismo origen: debe distinguirse entre [[Geometric Dispersion]] y [[Material Dispersion]].
- En métodos de ondas superficiales, la dispersión dominante suele ser la geométrica.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- capítulo o sección: 2.1.1 Two categories of wave motion
- página: 39–41

- PDF: Sebastiano Foti Chapter 2
- capítulo o sección: 2.1.2 Group velocity
- página: 41–42

- PDF: Sebastiano Foti Chapter 4
- capítulo o sección: 4.1 Phase and Group Velocity
- página: 205–206
