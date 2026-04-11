# Rayleigh Waves

> [!CONCEPT] Definición
> Las **ondas de Rayleigh** son ondas superficiales que se propagan a lo largo de la superficie libre de un medio elástico, resultando del acoplamiento entre ondas P y SV bajo la condición de esfuerzo nulo en la superficie. Predichas teóricamente por Lord Rayleigh en 1885 y verificadas experimentalmente, son la señal primaria de todos los métodos de caracterización del subsuelo con ondas superficiales ([[MASW Method]], [[SASW Method]], [[ReMi Method]]).
>
> — Lord Rayleigh (1885), *Proc. London Math. Soc.*, 17, 4–11; Foti et al. (2018), §2.2, pp. 50–62.

---

## 1. Naturaleza y movimiento de partícula

Las Rayleigh Waves resultan del acoplamiento entre [[P-waves]] y [[SV-wave|ondas SV]] bajo la condición de superficie libre. El movimiento de partícula es:

- **Elíptico** en el plano vertical de propagación
- **Retrógrado** en superficie (sentido antihorario para propagación en $+x$)
- **Prograde** por debajo de la profundidad crítica $x_2^c \approx 0.2\lambda$

La amplitud vertical es ~1.5 veces la horizontal en superficie. Esta dominancia vertical hace que los **geófonos verticales** las capturen eficientemente sin necesidad de componentes horizontales.

---

## 2. Velocidad en el semiespacio homogéneo

En un [[Elastic Half Space]] homogéneo, la velocidad de Rayleigh $c_R$ se obtiene de la **ecuación secular**:

$$
\left(2 - \frac{c_R^2}{V_S^2}\right)^2 = 4\sqrt{1 - \frac{c_R^2}{V_P^2}}\sqrt{1 - \frac{c_R^2}{V_S^2}}
$$

Equivalentemente como polinomio en $\xi = c_R/V_S$:

$$
\xi^6 - 8\xi^4 + \left(24 - 16\frac{V_S^2}{V_P^2}\right)\xi^2 - 16\left(1 - \frac{V_S^2}{V_P^2}\right) = 0
$$

La solución depende únicamente de $V_S$ y del [[Poisson Ratio]]:

| $\nu$ | $c_R/V_S$ |
|--------|-----------|
| 0.00 | 0.874 |
| 0.25 | 0.919 |
| 0.33 | 0.932 |
| 0.50 | 0.955 |

Aproximación de Viktorov: $c_R/V_S \approx (0.862 + 1.14\nu)/(1 + \nu)$.

> [!NOTE] Implicación para la tesis
> Los geófonos miden $c_R$, no $V_S$ directamente. La conversión requiere conocer $\nu$. Una incertidumbre de $\pm 0.05$ en $\nu$ alrededor de 0.25 introduce un error de $\pm 1$–$2\%$ en $V_S$.

---

## 3. No-dispersividad en el semiespacio homogéneo

En el [[Elastic Half Space]] homogéneo, $c_R$ **no depende de la frecuencia** — la ecuación secular no contiene $\omega$ ni $k$ independientemente. Las Rayleigh Waves son no dispersivas.

Toda dispersión observable en campo es evidencia directa de heterogeneidad vertical del subsuelo ([[Geometric Dispersion]]). La diferencia entre la curva experimental $c_R(f)$ y la velocidad constante $c_R^{hom}$ cuantifica la estratificación.

---

## 4. Decaimiento con profundidad y atenuación geométrica

Los desplazamientos decaen exponencialmente con la profundidad — la energía queda confinada cerca de la superficie ([[Skin Depth]] $\approx 0.94\lambda_R$). Esta propiedad establece la **regla de investigación**: la profundidad máxima explorada es $\approx \lambda_R/2$ a $\lambda_R$.

Decaimiento geométrico en superficie: $A_R \propto r^{-0.5}$ (frente cilíndrico), vs. $r^{-2}$ para [[Body Waves]]. A distancias > 1–2$\lambda_R$, el campo sísmico queda **dominado por Rayleigh Waves** — fundamento de todos los métodos [[MASW Method|MASW]].

---

## 5. Dispersión en medios estratificados

En [[Layered Media]], la [[Phase Velocity]] de Rayleigh varía con la frecuencia ([[Geometric Dispersion]]): ondas de alta frecuencia (corta $\lambda$) muestrean capas superficiales; ondas de baja frecuencia (larga $\lambda$) promedian el perfil hasta mayor profundidad. Esta dependencia $c_R(f)$ — la **[[Dispersion Curve|curva de dispersión]]** — es el dato observable que se invierte para obtener Vs(z).

Cuando hay [[Surface Wave Modes|modos superiores]] activos, la [[Phase Velocity|velocidad de fase]] aparente es una superposición modal y puede diferir del modo fundamental (ver [[Wave Superposition]]).

---

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) y Xia et al. (2002) — [[MASW Method|MASW]] en Kansas
> **Paper 001 (Park, Miller & Xia 1999)** demuestra que las Rayleigh Waves dominan los sismogramas superficiales con fuente activa y que la transformada f-k extrae directamente su [[Dispersion Curve|curva de dispersión]] $c_R(f)$. Los registros en múltiples sitios de Kansas muestran que el ground-roll de Rayleigh es la señal predominante a distancias > 5 m.
>
> **Paper 009 (Xia et al. 2002)** valida los perfiles $V_S(z)$ obtenidos invirtiendo $c_R(f)$ contra 14 ensayos de borehole independientes. El error RMS promedio entre $V_S$ [[MASW Method|MASW]] y borehole es < 15%, confirmando que la [[Dispersion Curve|curva de dispersión]] de Rayleigh es una medida robusta y representativa del subsuelo real.
>
> — Research Database, entradas 001, 009 (core).

---

## 6. Relaciones con otros conceptos

- [[Elastic Half Space]] — medio más simple donde existen Rayleigh Waves (no dispersivas)
- [[Layered Media]] — condición para [[Geometric Dispersion]] de Rayleigh
- [[Phase Velocity]] — observable experimental: $c_R(f)$
- [[Skin Depth]] — profundidad de investigación por longitud de onda
- [[Surface Wave Modes]] — modos fundamental y superiores de Rayleigh
- [[Love Waves]] — otro tipo de onda superficial (SH guiada)
- [[Rayleigh Eigenproblem]] — formulación matemática del problema de valores propios
- [[Near-field Effect]] — artefacto que contamina $c_R$ medida en campo cercano
- [[Attenuation]] — amortiguamiento material medible en la curva de atenuación $\alpha_R(f)$
- [[MASW Method]], [[SASW Method]], [[ReMi Method]] — métodos que explotan Rayleigh Waves

---

## 7. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Lord Rayleigh (1885), *Proc. London Math. Soc.* | 17, 4–11 — predicción teórica original |
| Foti et al. (2018), *Surface Wave Methods* | §2.2, pp. 50–62 |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 |
| Xia et al. (2002), *J. Environ. Eng. Geophys.* | Paper 009 |
