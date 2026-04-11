# Geometric Dispersion

> [!CONCEPT] Definición
> La **dispersión geométrica** es el fenómeno por el cual la [[Phase Velocity]] de una onda superficial depende de la frecuencia como consecuencia directa de la **heterogeneidad vertical del medio**. En un semiespacio homogéneo, las [[Rayleigh Waves]] no son dispersivas; la dispersión aparece cuando el subsuelo presenta [[Layered Media|estratificación]] o variación continua de propiedades con la profundidad.
>
> — Foti, S. et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §1.2.1, pp. 6–8.

---

## 1. Fundamento físico

Las ondas superficiales concentran la mayor parte de su energía en una zona superficial cuya profundidad efectiva de penetración es proporcional a la longitud de onda ([[Skin Depth]]).

- **Longitudes de onda cortas (alta frecuencia)** → la energía queda confinada en las capas más someras → la velocidad refleja las propiedades superficiales.
- **Longitudes de onda largas (baja frecuencia)** → la energía penetra más profundo → la velocidad integra propiedades de mayor profundidad.

Si las propiedades mecánicas varían con la profundidad ([[Layered Media]]), cada componente frecuencial "ve" un medio efectivo distinto. El resultado es una [[Dispersion Relation]] con [[Phase Velocity]] variable en frecuencia:

$$
c_R = c_R(\omega)
$$

Este comportamiento contrasta con la [[Material Dispersion]], donde la dependencia frecuencial de la velocidad proviene de las propiedades constitutivas del material y no de su geometría estratigráfica.

---

## 2. Formulación matemática

En el semiespacio homogéneo clásico, la [[Phase Velocity|velocidad de fase]] de Rayleigh es constante (≈ 0.919 Vs para ν = 0.25). La dispersión geométrica emerge cuando se resuelve el problema de valores propios del [[Rayleigh Eigenproblem]] para un medio estratificado:

$$
c_R = \frac{\omega}{k}
$$

y la condición de contorno por capas impone:

$$
c_R = c_R(\omega)
$$

Esta relación funcional es la **[[Dispersion Curve|curva de dispersión]]** — la firma observacional de la estratificación. Su forma depende directamente del perfil de [[Phase Velocity|velocidad de corte]] Vs(z).

> [!NOTE] Conexión con el problema inverso
> La [[Dispersion Curve|curva de dispersión]] experimental es el dato de entrada del **problema inverso** de ondas superficiales (Cap. 6–7 Foti). Recuperar Vs(z) a partir de c_R(ω) es un problema no lineal mal condicionado sujeto a [[Non-uniqueness]].

---

## 3. Aplicación a la instrumentación con geófonos

Con arreglos de geófonos se mide cómo cambia la [[Phase Velocity]] de las [[Rayleigh Waves]] con la frecuencia:

| Método | Arreglo | Extracción de c_R(ω) |
|--------|---------|----------------------|
| [[SASW Method]] | 2 receptores, separación variable | Cross-power spectrum |
| [[MASW Method]] | 24+ receptores, arreglo lineal | Transformada f-k / Phase-shift |
| [[ReMi Method]] | 12+ receptores | f-k pasivo |
| [[SPAC Method]] | Arreglo 2D circular | Bessel J₀ autocorrelación |

La explotación sistemática de la dispersión geométrica para caracterización del subsuelo fue introducida por Nazarian & Stokoe (1984) con el [[SASW Method]] y formalizada a escala multicanal por Park, Miller & Xia (1999) con el [[MASW Method]].

---

## 4. Implicaciones para el diseño experimental

- El **contenido frecuencial de la fuente** controla la profundidad investigada: fuentes impulsivas ligeras generan frecuencias altas (resolución superficial); masas de impacto más pesadas o vibradores aportan frecuencias bajas (mayor profundidad).
- La **longitud del arreglo** y la separación entre geófonos condicionan el rango útil de longitudes de onda: separación mínima → λ mínima → profundidad mínima; longitud total → λ máxima → profundidad máxima.
- Si el subsuelo es casi homogéneo, la dispersión observable será débil — la [[Dispersion Curve|curva de dispersión]] será casi plana.
- Si hay fuerte estratificación (e.g., suelo blando sobre roca), la dispersión será marcada y la curva tendrá alta pendiente a baja frecuencia.
- El [[Near-field Effect]] puede contaminar la curva a bajas frecuencias cuando el offset fuente-receptor es insuficiente.

---

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) y Xia et al. (1999) — validación [[MASW Method|MASW]] en Kansas
> **Paper 001 (Park, Miller & Xia 1999)** y **Paper 002 (Xia, Miller & Park 1999)** constituyen la demostración canónica de que la dispersión geométrica puede extraerse de manera robusta con arreglos multicanal.
>
> - Park et al. (1999) muestran que la transformada f-k del sismograma de [[Ground Roll|ground-roll]] produce imágenes de dispersión donde cada máximo espectral corresponde a un modo de [[Rayleigh Waves]] con su c_R(ω) característico — evidencia directa del fenómeno geométrico.
> - Xia et al. (1999) invierten esas curvas mediante linealización iterativa (Jacobiano ∂V_R/∂Vs por capa) y recuperan perfiles Vs(z) validados contra borehole en sitios de Kansas. El acuerdo es muy bueno, confirmando que la dispersión observada refleja fielmente la estratificación real.
> - La validación adicional de Xia et al. (2002) (**Paper 009**) con 14 sitios independientes extiende esta evidencia a condiciones variadas.
>
> — Fuente: Research Database, entradas 001, 002, 009 (core).

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — origen del método
> **Paper 003 (Nazarian & Stokoe 1984)** es el primer uso sistemático de la dispersión geométrica para caracterización in situ. Con solo dos geófonos y separaciones variables, midieron c_R(f) mediante cross-power spectrum y la invirtieron para obtener Vs(z).
>
> Esta demostración seminal (>3000 citas) estableció el principio que hoy sustentan todos los métodos de ondas superficiales: la frecuencia controla la profundidad de investigación vía dispersión geométrica.
>
> — Fuente: Research Database, entrada 003 (core).

---

## 5. Relaciones con otros conceptos

- [[Wave Dispersion]] — categoría general; la dispersión geométrica es un subtipo
- [[Material Dispersion]] — el otro subtipo: origen constitutivo, no estratigráfico
- [[Dispersion Relation]] — formalización matemática de c(ω)
- [[Phase Velocity]] — observable primario medido en campo
- [[Group Velocity]] — velocidad de paquete de ondas; difiere de c_R en medios dispersivos
- [[Skin Depth]] — profundidad efectiva de penetración por longitud de onda
- [[Layered Media]] — condición necesaria para que emerja la dispersión geométrica
- [[Rayleigh Eigenproblem]] — formulación matemática del sistema estratificado
- [[Near-field Effect]] — artefacto que puede distorsionar c_R(ω) a bajas frecuencias
- [[Non-uniqueness]] — problema en la inversión de c_R(ω) → Vs(z)

---

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.2.1, pp. 6–8 |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 40–41 |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | pp. 800–808 (Paper 001) |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | pp. 691–700 (Paper 002) |
| Nazarian & Stokoe (1984), *Proc. 8WCEE* | Vol. III, pp. 31–38 (Paper 003) |
