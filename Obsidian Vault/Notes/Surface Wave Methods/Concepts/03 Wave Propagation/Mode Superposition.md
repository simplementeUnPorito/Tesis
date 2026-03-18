# Mode Superposition

## 1. Concepto

La **superposición de modos** describe el hecho de que el campo sísmico registrado en un arreglo de geófonos es, en general, la suma de múltiples modos de propagación de [[Rayleigh Waves]] y/o [[Love Waves]].

---

## 2. Fundamento físico

En medios [[Layered Media|estratificados]], la relación de dispersión del [[Rayleigh Eigenproblem]] admite múltiples soluciones para una misma frecuencia — cada una corresponde a un modo de propagación con su propia velocidad de fase y patrón de desplazamiento vertical.

El modo fundamental tiene la mayor penetración y, generalmente, la mayor amplitud. Los modos superiores tienen frecuencias de corte mínimas y penetraciones menores.

---

## 3. Formulación matemática

El campo de desplazamiento total en superficie puede escribirse como:

$$
u(x,t) = \sum_{n=0}^{N} A_n(x) \, e^{i(k_n x - \omega t)}
$$

donde el índice $n$ identifica el modo y $k_n$ es el número de onda del modo $n$ a la frecuencia $\omega$.

---

## 4. Aplicación a geófonos

Si el procesamiento asume que el campo está dominado por el modo fundamental pero en realidad hay contribución significativa de modos superiores, la curva de dispersión estimada será una mezcla de modos. La inversión de esa curva producirá un perfil $V_S$ erróneo.

Esto es especialmente crítico cuando hay fuertes contrastes de velocidad (e.g., suelo blando sobre roca), que favorecen la excitación de modos superiores.

---

## 5. Implicaciones para el diseño experimental

- Verificar que la fuente no excite preferentemente modos superiores.
- Usar métodos de procesamiento que permitan separar modos (e.g., MASW con transformada de alta resolución, beamforming).
- Registrar con arreglos suficientemente largos para resolver las distintas velocidades de fase modales.
- Documentar si se asume modo fundamental y en qué condiciones esa hipótesis es razonable para el sitio.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.4 Surface waves in vertically inhomogeneous media