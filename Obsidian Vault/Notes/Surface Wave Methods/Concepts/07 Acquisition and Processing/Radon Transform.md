---
name: Radon Transform
description: Transformada τ-p (tiempo de intercepción - parámetro de slowness) que mapea el campo de ondas sísmico al dominio de rayos planos — usada en [[MASW Method|MASW]] y sísmica de reflexión para separar modos de ondas superficiales y suprimir ruido coherente
type: reference
---

# Radon Transform — Transformada de Radón ($\tau$-$p$)

> [!CONCEPT] Definición
> La **transformada de Radón** (o transformada $\tau$-$p$, con $p$ = *slowness* = $1/V$) mapea una función $u(x, t)$ (campo de ondas sísmico en el dominio espacio-tiempo) al dominio $(\tau, p)$:
> $$U(\tau, p) = \int_{-\infty}^{\infty} u(x, \tau + px) \, dx$$
> donde $\tau$ es el tiempo de intercepción y $p = 1/V$ es el parámetro de *slowness* (inverso de la velocidad aparente). La transformada de Radón lineal (*linear Radon transform* o *slant stack*) suma a lo largo de líneas rectas $t = \tau + px$ en el dominio $x$-$t$. Una onda plana con velocidad aparente $V_a$ (slowness $p = 1/V_a$) y tiempo de intercepción $\tau_0$ produce un **punto concentrado** en $(\tau_0, p)$ en el dominio transformado. En el análisis de [[MASW Method|ondas superficiales]], la transformada $\tau$-$p$ ofrece una alternativa a la transformada $f$-$k$ para extraer la [[Dispersion Curve|curva de dispersión]]: cada modo de Rayleigh aparece como una cresta en el panel $(\tau, p)$ a slowness $p = 1/V_R(f)$. La versión **parabólica** de la transformada (suma a lo largo de parábolas) es más efectiva para suprimir las ondas de cuerpo que tienen moveout hiperbólico en $x$-$t$.
>
> — Foti et al. (2018), §4.3.3, pp. 198–204; Treitel et al. (1982), *Geophysics* 47(10); Tatham (1989), *Geophysics*.

## Propiedades de la transformada τ-p en ondas superficiales

### Separación de modos

En el panel $(\tau, p)$, los distintos modos de Rayleigh aparecen como crestas a diferentes slownesses $p_n = 1/V_{R,n}(f)$. La separación es efectiva cuando las velocidades de fase difieren > 10–15% — similar a la condición para separación en el dominio $f$-$k$.

### Supresión de ondas de cuerpo

Las ondas P y S directas tienen moveout lineal en $x$-$t$ (onda plana) pero a velocidades mucho mayores que las ondas Rayleigh ($V_P \gg V_R$). En el dominio $\tau$-$p$, aparecen a slowness muy pequeña ($p \ll 1/V_R$), fácilmente filtrable. Las ondas de cuerpo refractadas tienen moveout hiperbólico — no se mapean como puntos en $\tau$-$p$ lineal, pero sí en $\tau$-$p$ parabólico.

### Relación con la transformada f-k

La transformada $f$-$k$ es la versión espectral (en frecuencia) de la $\tau$-$p$:
$$F(f, k) = \int\!\int u(x, t) \, e^{-i2\pi(ft - kx)} \, dx \, dt$$

La relación entre ambas: $p = k/f$ — el slowness es la pendiente en $f$-$k$. Los picos del panel $f$-$k$ sobre líneas de velocidad constante $V_a = f/k$ corresponden a puntos en $\tau$-$p$ a $p = 1/V_a$.

## Transformada de Radón de Alta Resolución

La versión estándar (slant stack) tiene resolución en slowness limitada por la apertura del arreglo. La **LRT de alta resolución** (*high-resolution linear Radon transform*, HRLRT) mejora la separación modal usando inversión por esparsidad — penaliza soluciones no compactas en el dominio $(\tau, p)$:

$$U_{HR}(\tau, p) = \arg\min \|U\|_1 \quad \text{s.t.} \quad \|u - LU\|_2 < \epsilon$$

donde $L$ es el operador de forward Radon y $\epsilon$ es la tolerancia de ajuste. Luo et al. (2009) demostraron que HRLRT mejora la resolución de imágenes modales >50% vs. slant stacking estándar, separando exitosamente modos de Rayleigh con diferencias de velocidad de solo 5–10%.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) y Luo et al. (2009) — τ-p en [[MASW Method|MASW]] vs. f-k
> **Foti et al. (2018, §4.3.3)** comparan paneles $f$-$k$ y $\tau$-$p$ del mismo dataset [[MASW Method|MASW]] en Memphis. El panel $\tau$-$p$ muestra el modo fundamental como cresta concentrada con menor contaminación de ondas de cuerpo que el equivalente $f$-$k$ (ondas P a $p \approx 0.002$ s/m vs. Rayleigh a $p \approx 0.005$–$0.01$ s/m). La [[Dispersion Curve|curva de dispersión]] extraída coincide dentro del 2%.
>
> **Luo et al. (2009, GJI 179)** — geófonos 4.5 Hz, $\Delta x = 0.5$ m (equipamiento idéntico al típico en tesis): HRLRT separa el modo fundamental del primer modo superior de Rayleigh donde el slant stack estándar producía una cresta única mezclada. La inversión multimodal con las curvas separadas mejoró el perfil VS en un 35% de error respecto al perforado de control. Aplicable directamente a ensayos [[MASW Method|MASW]] con modos superiores visibles en sitios con inversión de velocidad.
>
> — Foti et al. (2018), §4.3.3, pp. 198–204; Luo et al. (2009), *GJI* 179:254–264 (Paper 039).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §4.3.3 — transformada τ-p en [[MASW Method|MASW]] |
| Treitel et al. (1982), *Geophysics* 47(10), 1571–1581 | Slant stack y transformada τ-p en sísmica |
| Tatham, R.H. (1989), *Geophysics* | Transformada τ-p parabólica para supresión de ruido |
| Luo et al. (2009), *GJI* 179:254–264 | HRLRT: separación de modos Rayleigh >50% mejora; Paper 039 |
