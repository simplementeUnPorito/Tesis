# Viscoelastic Media

## 1. Concepto

Un **medio viscoelástico** es un material que combina comportamiento elástico (recuperable) y viscoso (disipativo). Bajo carga dinámica, parte de la energía mecánica se convierte en calor.

---

## 2. Fundamento físico

En medios elásticos ideales no hay pérdida de energía durante la propagación. En medios reales (suelos, rocas), la disipación es inevitable. Los modelos viscoelásticos más utilizados en geofísica son:

- **Kelvin-Voigt:** esfuerzo proporcional a deformación más velocidad de deformación.
- **Maxwell:** elemento elástico en serie con elemento viscoso.
- **Sólido estándar lineal (SLS):** combinación que reproduce mejor el comportamiento de geomateriales en el rango de frecuencias sísmicas.

---

## 3. Formulación matemática

### Módulos complejos

Las constantes de Lamé se reemplazan por módulos complejos dependientes de la frecuencia:

$$
\tilde{\mu}(\omega) = \mu_R(\omega) + i\,\mu_I(\omega)
$$

### Principio de correspondencia elástico-viscoelástico

Todas las soluciones del problema elástico son válidas en el problema viscoelástico con la sustitución $\lambda, \mu \to \tilde{\lambda}(\omega), \tilde{\mu}(\omega)$.

Esto permite extender directamente la [[Rayleigh Waves|ecuación secular de Rayleigh]] y el [[Rayleigh Eigenproblem]] a medios disipativos.

### Número de onda complejo

En un medio disipativo el número de onda se vuelve complejo:

$$
\tilde{k} = k_R + i\,k_I
$$

La solución armónica toma la forma:

$$
u \propto e^{-k_I x} \, e^{i(k_R x - \omega t)}
$$

donde $k_R$ controla la fase y $k_I$ controla la atenuación espacial.

### Factor de calidad y material damping ratio

$$
D = \frac{k_I}{2k_R} = \frac{1}{2Q}
$$

Para suelos típicos: $D \sim 1\text{–}10\%$ (amortiguamiento débil).

---

## 4. Aplicación a geófonos

En condiciones de amortiguamiento débil ($D \ll 1$), la velocidad de fase se ve afectada en orden $D^2$ — efecto pequeño. La atenuación espacial es proporcional a $D$ — efecto de primer orden y directamente medible.

Esto justifica el enfoque estándar: caracterizar primero el perfil de $V_S$ desde la curva de dispersión, y luego el perfil de $D$ desde la curva de atenuación.

---

## 5. Implicaciones para el diseño experimental

Medir amplitudes con precisión suficiente para extraer el perfil de $D$ es significativamente más exigente instrumentalmente que medir velocidades de fase. Requiere control del acoplamiento suelo-geófono, corrección de atenuación geométrica y estimación del factor de fuente. Si el objetivo de la tesis es solo el perfil $V_S$, ignorar la disipación introduce errores de segundo orden en la velocidad de fase.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.5 Wave propagation in dissipative media