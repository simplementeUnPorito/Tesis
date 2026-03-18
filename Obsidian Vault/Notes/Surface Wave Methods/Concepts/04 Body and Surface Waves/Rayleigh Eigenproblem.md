# Rayleigh Eigenproblem

## 1. Concepto

El **Rayleigh Eigenproblem** es la formulación matemática que describe la propagación de [[Rayleigh Waves]] en medios verticalmente heterogéneos o disipativos como un **problema de valores propios**.

---

## 2. Fundamento físico

En un semiespacio homogéneo, la ecuación secular de Rayleigh es algebraica y tiene solución cerrada. Cuando el medio es estratificado o viscoelástico, el problema se vuelve diferencial: las condiciones de frontera en cada interfaz y en la superficie libre deben satisfacerse simultáneamente, lo que conduce a un eigenproblem.

---

## 3. Formulación matemática

Para un medio [[Layered Media|estratificado en capas]], las condiciones de continuidad de desplazamiento y esfuerzo en cada interfaz, junto con la condición de superficie libre, se formulan como un sistema matricial. Para que existan soluciones de onda superficial (que decaigan con la profundidad), el determinante del sistema debe ser cero:

$$
\det[\mathbf{M}(c_R, \omega)] = 0
$$

Esto define la **velocidad de fase** $c_R(\omega)$ como función de la frecuencia — es decir, la **curva de dispersión**.

### Extensión a medios disipativos

En [[Viscoelastic Media]], los módulos elásticos se reemplazan por módulos complejos dependientes de la frecuencia:

$$
\tilde{\mu}(\omega) = \mu_R(\omega) + i\,\mu_I(\omega)
$$

La velocidad de fase y el número de onda se vuelven complejos. Para amortiguamiento débil ($D \ll 1$), la solución se obtiene por perturbación de primer orden alrededor del caso elástico:

- la velocidad de fase se modifica en orden $D^2$ (efecto de segundo orden)
- la atenuación espacial es proporcional a $D$ (efecto de primer orden)

---

## 4. Aplicación a geófonos

El Rayleigh Eigenproblem es el núcleo del **problema directo (forward problem)** en todos los métodos de inversión de ondas superficiales. Dado un perfil de $V_S$, $V_P$ y $\rho$ (y opcionalmente $D$), se resuelve el eigenproblem para obtener la curva de dispersión teórica que se compara con la medida.

---

## 5. Implicaciones para el diseño experimental

El eigenproblem admite múltiples soluciones (modos). Si en el campo se excitan modos superiores pero el procesamiento asume modo fundamental, el perfil $V_S$ obtenido por inversión será erróneo. Identificar qué modos están presentes en el registro es una decisión de procesamiento con consecuencias directas sobre la calidad del perfil.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.4, 2.5