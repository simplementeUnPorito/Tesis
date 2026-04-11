# Water Waves

> [!CONCEPT] Definición
> Las **water waves** (ondas de agua) son ondas superficiales gravitacionales que se propagan en la interfaz agua-aire. Son el ejemplo pedagógico clásico de ondas **dispersivas**: su [[Phase Velocity]] depende fuertemente de la frecuencia y de la profundidad del agua $h$.
>
> En el contexto de ondas superficiales geofísicas, las water waves sirven como analogía intuitiva para comprender la [[Geometric Dispersion]] de las [[Rayleigh Waves]] en medios estratificados.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.2.

---

## 1. [[Dispersion Relation|relación de dispersión]]

La [[Dispersion Relation]] completa para water waves en profundidad $h$ es:

$$
\omega^2 = g k \tanh(kh)
$$

donde $g$ es la aceleración gravitacional, $k = 2\pi/\lambda$ el [[Wavenumber]] y $\omega$ la [[Angular Frequency]].

Esto da lugar a dos regímenes límite:

| Régimen | Condición | [[Dispersion Relation|relación de dispersión]] | [[Phase Velocity]] |
|---------|-----------|------------------------|-------------------|
| **Agua profunda** | $kh \gg 1$ | $\omega = \sqrt{gk}$ | $c_p = \sqrt{g/k}$ — decrece con $k$ |
| **Agua somera** | $kh \ll 1$ | $\omega = k\sqrt{gh}$ | $c_p = \sqrt{gh}$ — constante (no dispersiva) |
| **Intermedio** | — | $\omega = \sqrt{gk\tanh(kh)}$ | Variable |

---

## 2. Analogía con ondas superficiales sísmicas

La dispersión de water waves es **geométrica** — no proviene de las propiedades del agua, sino de la geometría del dominio (profundidad $h$). Esta es exactamente la misma física que la [[Geometric Dispersion]] de [[Rayleigh Waves]] en suelos estratificados:

| Water waves | Rayleigh waves |
|-------------|---------------|
| Profundidad del agua $h$ | Espesor de capas del subsuelo |
| Gravedad $g$ controla $c_p$ | Vs controla $c_R$ |
| $\lambda$ larga → agua profunda → $c_p$ mayor | $\lambda$ larga → mayor profundidad → $c_R$ mayor |
| $\tanh(kh)$ en la [[Dispersion Relation|relación de dispersión]] | Funciones de Bessel / matrices de transferencia |

Ambos sistemas son **dispersivos geométricos**: la [[Phase Velocity|velocidad de fase]] varía con la frecuencia porque diferentes longitudes de onda "ven" dominios de diferente tamaño efectivo.

---

## 3. Relaciones con otros conceptos

- [[Surface Water Waves]] — caso específico: ondas en la superficie libre del agua
- [[Dispersion Relation]] — formalización matemática de $\omega(k)$
- [[Wave Dispersion]] — categoría general que incluye water waves y Rayleigh waves
- [[Geometric Dispersion]] — mecanismo físico compartido
- [[Phase Velocity]] / [[Group Velocity]] — observables que varían con la frecuencia
- [[Rayleigh Waves]] — análogo sísmico del presente concepto

---

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — dispersión geométrica de Water Waves como modelo mental para [[MASW Method|MASW]]
> Foti et al. (2018, §2.1.2) introducen la [[Dispersion Relation|relación de dispersión]] $\omega^2 = gk\tanh(kh)$ como el caso más simple de dispersión geométrica — antes de presentar la ecuación secular de Rayleigh — precisamente porque el mecanismo físico es idéntico: **la [[Phase Velocity|velocidad de fase]] depende de cuánto dominio "ve" la onda en profundidad**. En aguas poco profundas ($kh \ll 1$), todas las frecuencias ven el fondo → no-dispersión ($c_p = \sqrt{gh}$). En aguas profundas ($kh \gg 1$), cada frecuencia ve una profundidad efectiva diferente → dispersión normal. Este marco permite explicar intuitivamente por qué la [[Dispersion Curve|curva de dispersión]] de Rayleigh a altas frecuencias (longitudes de onda cortas) refleja las capas superficiales del suelo y a bajas frecuencias refleja las capas profundas — la misma física que governa Water Waves pero ahora con el perfil $V_S(z)$ controlando la dispersión en lugar del perfil batimétrico $h$.
>
> — Foti et al. (2018), §2.1.2, pp. 41–43.

## 4. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.2, pp. 41–43 |
| Lamb, H. (1932), *Hydrodynamics*, 6th ed., Cambridge University Press | Cap. IX |
